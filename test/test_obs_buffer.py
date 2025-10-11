"""
Test the OBS buffer with individual line expiry (chat-like behavior)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from config import ConfigManager
from obs_buffer import OBSBufferManager

def test_chat_like_buffer():
    print("Testing OBS Buffer with individual line expiry")
    print("=" * 50)
    
    # Create buffer
    config = ConfigManager()
    buffer = OBSBufferManager(config)
    
    info = buffer.get_buffer_info()
    print(f"Buffer: {info['max_lines']} lines, {info['line_timeout']}s per line\n")
    
    # Simulate chat-like messages
    messages = [
        "Hello everyone!",
        "This is the second message",
        "And here's a third one",
        "Fourth message appears",
        "Fifth message - first should be gone now"
    ]
    
    print("Adding messages with 2s delay between each:")
    for i, msg in enumerate(messages, 1):
        print(f"  [{i}] Adding: {msg}")
        buffer.add_text(msg)
        
        # Show current buffer
        with open(config.get('Output', 'obs_file'), 'r') as f:
            content = f.read()
            line_count = len([l for l in content.split('\n') if l.strip()])
            print(f"      Current lines in file: {line_count}")
        
        time.sleep(2)
    
    print("\nWaiting 6 seconds to see lines expire...")
    time.sleep(6)
    
    with open(config.get('Output', 'obs_file'), 'r') as f:
        content = f.read()
        remaining_lines = len([l for l in content.split('\n') if l.strip()])
        print(f"Lines remaining after expiry: {remaining_lines}")
        print(f"Content:\n{content if content else '(empty)'}")
    
    buffer.cleanup()
    print("\nTest complete!")

if __name__ == "__main__":
    test_chat_like_buffer()
