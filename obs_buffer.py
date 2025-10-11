"""
OBS Buffer Manager for Real-Time Translator
Handles multi-line text buffer and auto-clear functionality for OBS
"""

import threading
import time
from datetime import datetime
from collections import deque


class OBSBufferManager:
    """Manages OBS text buffer with multi-line support and auto-clear"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        
        # Load configuration
        self.obs_file = self.config.get('Output', 'obs_file')
        self.encoding = self.config.get('Output', 'encoding')
        self.buffer_lines = self.config.getint('Output', 'obs_buffer_lines')
        self.auto_clear_timeout = self.config.getfloat('Output', 'obs_auto_clear_timeout')
        self.line_separator = self.config.get('Output', 'obs_line_separator').replace('\\n', '\n')
        self.include_timestamp = self.config.getboolean('Output', 'include_timestamp')
        self.timestamp_format = self.config.get('Output', 'timestamp_format')
        
        # Buffer state
        self.text_buffer = deque(maxlen=self.buffer_lines)
        self.last_update_time = None
        self.clear_timer = None
        self.lock = threading.Lock()
        
        # Initialize with empty file
        self.write_buffer_to_file()
        
    def add_text(self, text):
        """Add new text to the buffer"""
        if not text or not text.strip():
            return
            
        with self.lock:
            # Add timestamp if configured
            if self.include_timestamp:
                timestamp = datetime.now().strftime(self.timestamp_format)
                formatted_text = f"{timestamp} {text}"
            else:
                formatted_text = text
            
            # Add to buffer (automatically removes oldest if at max capacity)
            self.text_buffer.append(formatted_text)
            self.last_update_time = time.time()
            
            # Write to file immediately
            self.write_buffer_to_file()
            
            # Reset auto-clear timer
            self.reset_clear_timer()
    
    def write_buffer_to_file(self):
        """Write current buffer to OBS file"""
        try:
            content = self.line_separator.join(self.text_buffer)
            with open(self.obs_file, 'w', encoding=self.encoding) as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing OBS buffer: {e}")
    
    def clear_buffer(self):
        """Clear the text buffer"""
        with self.lock:
            self.text_buffer.clear()
            self.write_buffer_to_file()
            self.last_update_time = None
            
            # Cancel any pending clear timer
            if self.clear_timer:
                self.clear_timer.cancel()
                self.clear_timer = None
    
    def reset_clear_timer(self):
        """Reset the auto-clear timer"""
        # Cancel existing timer
        if self.clear_timer:
            self.clear_timer.cancel()
        
        # Set new timer if timeout is configured
        if self.auto_clear_timeout > 0:
            self.clear_timer = threading.Timer(self.auto_clear_timeout, self.auto_clear)
            self.clear_timer.daemon = True
            self.clear_timer.start()
    
    def auto_clear(self):
        """Auto-clear function called by timer"""
        with self.lock:
            if self.last_update_time and (time.time() - self.last_update_time) >= self.auto_clear_timeout:
                self.text_buffer.clear()
                self.write_buffer_to_file()
                print(f"OBS buffer auto-cleared after {self.auto_clear_timeout}s timeout")
    
    def get_buffer_info(self):
        """Get current buffer information"""
        with self.lock:
            return {
                'lines': len(self.text_buffer),
                'max_lines': self.buffer_lines,
                'timeout': self.auto_clear_timeout,
                'last_update': self.last_update_time
            }
    
    def cleanup(self):
        """Clean up resources"""
        if self.clear_timer:
            self.clear_timer.cancel()
        self.clear_buffer()