"""
OBS Buffer Manager for Real-Time Translator
Handles multi-line text buffer with individual line expiry (chat-like behavior)
"""

import threading
import time
from datetime import datetime
from collections import deque


class OBSBufferManager:
    """Manages OBS text buffer with individual line expiry like chat messages"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        
        # Load configuration
        self.obs_file = self.config.get('Output', 'obs_file')
        self.encoding = self.config.get('Output', 'encoding')
        self.buffer_lines = self.config.getint('Output', 'obs_buffer_lines')
        self.line_timeout = self.config.getfloat('Output', 'obs_auto_clear_timeout')
        self.line_separator = self.config.get('Output', 'obs_line_separator').replace('\\n', '\n')
        self.include_timestamp = self.config.getboolean('Output', 'include_timestamp')
        self.timestamp_format = self.config.get('Output', 'timestamp_format')
        
        # Buffer state - stores tuples of (text, timestamp)
        self.text_buffer = deque(maxlen=self.buffer_lines)
        self.lock = threading.Lock()
        self.cleanup_thread = None
        self.running = True
        
        # Initialize with empty file
        self.write_buffer_to_file()
        
        # Start background cleanup thread
        self.start_cleanup_thread()
        
    def start_cleanup_thread(self):
        """Start background thread to clean up expired lines"""
        self.cleanup_thread = threading.Thread(target=self.cleanup_expired_lines, daemon=True)
        self.cleanup_thread.start()
    
    def cleanup_expired_lines(self):
        """Continuously remove expired lines (runs in background thread)"""
        while self.running:
            time.sleep(0.5)  # Check every 500ms
            
            with self.lock:
                current_time = time.time()
                # Remove lines that have exceeded their timeout
                expired_count = 0
                
                # Create new buffer without expired lines
                new_buffer = deque(maxlen=self.buffer_lines)
                for text, timestamp in self.text_buffer:
                    if current_time - timestamp < self.line_timeout:
                        new_buffer.append((text, timestamp))
                    else:
                        expired_count += 1
                
                # Update buffer if any lines expired
                if expired_count > 0:
                    self.text_buffer = new_buffer
                    self.write_buffer_to_file()
    
    def add_text(self, text):
        """Add new text to the buffer with timestamp"""
        if not text or not text.strip():
            return
            
        with self.lock:
            # Add timestamp if configured for display
            if self.include_timestamp:
                display_timestamp = datetime.now().strftime(self.timestamp_format)
                formatted_text = f"{display_timestamp} {text}"
            else:
                formatted_text = text
            
            # Add to buffer with current time for expiry tracking
            current_time = time.time()
            self.text_buffer.append((formatted_text, current_time))
            
            # Write to file immediately
            self.write_buffer_to_file()
    
    def write_buffer_to_file(self):
        """Write current buffer to OBS file (only the text, not timestamps)"""
        try:
            # Extract only the text from (text, timestamp) tuples
            texts = [item[0] for item in self.text_buffer]
            content = self.line_separator.join(texts)
            with open(self.obs_file, 'w', encoding=self.encoding) as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing OBS buffer: {e}")
    
    def clear_buffer(self):
        """Clear the text buffer"""
        with self.lock:
            self.text_buffer.clear()
            self.write_buffer_to_file()
    
    def get_buffer_info(self):
        """Get current buffer information"""
        with self.lock:
            return {
                'lines': len(self.text_buffer),
                'max_lines': self.buffer_lines,
                'line_timeout': self.line_timeout
            }
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.cleanup_thread.join(timeout=1)
        self.clear_buffer()