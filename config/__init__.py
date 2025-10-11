"""
Configuration Manager for Real-Time Translator
Handles loading and managing configuration from config.ini and environment variables
"""

import os
import configparser
from .defaults import DEFAULT_CONFIG


class ConfigManager:
    """Manages configuration from config.ini and environment variables"""
    
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load configuration from file with defaults"""
        # Set defaults from the separate defaults file
        self.config.read_dict(DEFAULT_CONFIG)
        
        # Read from config file if it exists
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
            print(f"Configuration loaded from {self.config_file}")
        else:
            print(f"Config file {self.config_file} not found, using defaults")
    
    def get(self, section, key, fallback=None):
        """Get configuration value with fallback"""
        return self.config.get(section, key, fallback=fallback)
    
    def getboolean(self, section, key, fallback=False):
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    def getint(self, section, key, fallback=0):
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)
    
    def getfloat(self, section, key, fallback=0.0):
        """Get float configuration value"""
        return self.config.getfloat(section, key, fallback=fallback)