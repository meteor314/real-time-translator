#!/usr/bin/env python3
"""
Configuration Demo for Real-Time Translator
This script demonstrates different language configurations
"""

import os
import sys
sys.path.append('.')
from main import ConfigManager, RealTimeTranslator

def demo_configurations():
    print("🎯 Configuration Demo")
    print("=" * 50)
    
    # Test different configurations
    configs = [
        {
            'name': 'French to English (Default)',
            'from_lang': 'fr',
            'to_lang': 'en',
            'from_name': 'French',
            'to_name': 'English'
        },
        {
            'name': 'Spanish to English',
            'from_lang': 'es',
            'to_lang': 'en',
            'from_name': 'Spanish',
            'to_name': 'English'
        },
        {
            'name': 'English to French',
            'from_lang': 'en',
            'to_lang': 'fr',
            'from_name': 'English',
            'to_name': 'French'
        }
    ]
    
    for config_demo in configs:
        print(f"\n📋 {config_demo['name']}")
        print("-" * 30)
        
        # Create a temporary config
        config_manager = ConfigManager()
        
        # Override language settings
        config_manager.config.set('Translation', 'from_language', config_demo['from_lang'])
        config_manager.config.set('Translation', 'to_language', config_demo['to_lang'])
        config_manager.config.set('Translation', 'from_language_name', config_demo['from_name'])
        config_manager.config.set('Translation', 'to_language_name', config_demo['to_name'])
        
        # Create translator (without starting it)
        translator = RealTimeTranslator(config_manager)
        
        print(f"✅ Source Language: {translator.from_lang_name} ({translator.from_lang})")
        print(f"✅ Target Language: {translator.to_lang_name} ({translator.to_lang})")
        print(f"✅ Output File: {translator.output_file}")
        print(f"✅ Audio Timeout: {translator.listen_timeout}s")
        print(f"✅ Phrase Limit: {translator.phrase_time_limit}s")
        
        # Show example prefixes
        print(f"Console Output Format:")
        print(f"  {translator.original_prefix} [Original text in {translator.from_lang_name}]")
        print(f"  {translator.translation_prefix} [Translation in {translator.to_lang_name}]")

def show_current_config():
    print("\n🔧 Current Configuration")
    print("=" * 50)
    
    config = ConfigManager()
    
    sections = ['Translation', 'Azure', 'Audio', 'Output', 'Display']
    
    for section in sections:
        print(f"\n[{section}]")
        if config.config.has_section(section):
            for key, value in config.config.items(section):
                print(f"  {key} = {value}")
        else:
            print("  (using defaults)")

if __name__ == "__main__":
    demo_configurations()
    show_current_config()
    
    print("\n" + "=" * 50)
    print("🚀 To customize your configuration:")
    print("1. Edit config.ini for permanent settings")
    print("2. Set AZURE_TRANSLATOR_KEY in .env file")
    print("3. Run: python main.py")
    print("=" * 50)