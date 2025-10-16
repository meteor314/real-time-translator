import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ConfigManager

cm = ConfigManager()
print('Config loaded successfully')
print(f'Pause threshold: {cm.getfloat("Audio", "pause_threshold")}s')
print(f'Non-speaking duration: {cm.getfloat("Audio", "non_speaking_duration")}s')
print(f'Phrase time limit: {cm.getfloat("Audio", "phrase_time_limit")}s')
print(f'Listen timeout: {cm.getfloat("Audio", "listen_timeout")}s')
