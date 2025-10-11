"""
Voice Logger for Real-Time Translator
Handles logging of original voice recordings to daily files
"""

import os
from datetime import datetime
from pathlib import Path


class VoiceLogger:
    """Manages daily voice logging functionality"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.voice_log_enabled = self.config.getboolean('Output', 'voice_log_enabled')
        self.voice_log_directory = self.config.get('Output', 'voice_log_directory')
        self.encoding = self.config.get('Output', 'encoding')
        
        # Create voice log directory if it doesn't exist
        if self.voice_log_enabled:
            Path(self.voice_log_directory).mkdir(exist_ok=True)
        
        self.current_date = None
        self.current_log_file = ""
        
    def _get_current_log_file(self):
        """Get the current log file path based on today's date"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if we need to create a new log file (date changed)
        if self.current_date != today:
            self.current_date = today
            self.current_log_file = os.path.join(
                self.voice_log_directory, 
                f"voice_log_{today}.txt"
            )
            
            # Create header for new daily file
            if not os.path.exists(self.current_log_file):
                self._create_daily_header()
        
        return self.current_log_file
    
    def _create_daily_header(self):
        """Create header for new daily voice log file"""
        try:
            with open(self.current_log_file, 'w', encoding=self.encoding) as f:
                f.write(f"=== Voice Log - {self.current_date} ===\n")
                f.write(f"Started at: {datetime.now().strftime('%H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
        except Exception as e:
            print(f"Error creating voice log file: {e}")
    
    def log_original_text(self, original_text, language_prefix="FR"):
        """Log original text to daily voice log file"""
        if not self.voice_log_enabled or not original_text.strip():
            return
        
        try:
            log_file = self._get_current_log_file()
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            with open(log_file, 'a', encoding=self.encoding) as f:
                f.write(f"[{timestamp}] {language_prefix}: {original_text}\n")
                
        except Exception as e:
            print(f"Error writing voice log: {e}")
    
    def finalize_daily_log(self):
        """Add end timestamp when stopping the application"""
        if not self.voice_log_enabled or not self.current_log_file:
            return
        
        try:
            with open(self.current_log_file, 'a', encoding=self.encoding) as f:
                f.write(f"\n=== Session ended at: {datetime.now().strftime('%H:%M:%S')} ===\n")
        except Exception as e:
            print(f"Error finalizing voice log: {e}")
    
    def get_today_stats(self):
        """Get statistics for today's voice log"""
        if not self.voice_log_enabled:
            return None
        
        log_file = self._get_current_log_file()
        
        if not os.path.exists(log_file):
            return {"lines": 0, "file": log_file}
        
        try:
            with open(log_file, 'r', encoding=self.encoding) as f:
                lines = f.readlines()
                # Count lines that contain actual voice logs (with timestamps)
                voice_lines = [line for line in lines if line.startswith('[') and ']:' in line]
                
            return {
                "lines": len(voice_lines),
                "file": log_file,
                "size": os.path.getsize(log_file)
            }
        except Exception as e:
            print(f"Error reading voice log stats: {e}")
            return None