"""
Real-Time Translation System - Main Entry Point
Modular version with separate configuration, translation, and logging components
"""

import os
import sys
from pathlib import Path

# Add config directory to path
sys.path.append(str(Path(__file__).parent / "config"))

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, skip

from config import ConfigManager
from translator import RealTimeTranslator


def show_startup_info(config_manager):
    """Display startup information and configuration summary"""
    print("Real-Time Translation System")
    print("=" * 50)
    
    # Show key configuration
    from_lang = config_manager.get('Translation', 'from_language_name')
    to_lang = config_manager.get('Translation', 'to_language_name')
    obs_file = config_manager.get('Output', 'obs_file')
    voice_log_enabled = config_manager.getboolean('Output', 'voice_log_enabled')
    
    print(f"Translation: {from_lang} -> {to_lang}")
    print(f"OBS Output: {obs_file}")
    
    if voice_log_enabled:
        voice_dir = config_manager.get('Output', 'voice_log_directory')
        print(f"Voice Logs: {voice_dir}/ (daily files)")
    else:
        print("Voice Logs: Disabled")
    
    print()


def check_azure_key():
    """Check and display Azure API key status"""
    azure_key = os.getenv('AZURE_TRANSLATOR_KEY')
    
    if not azure_key:
        print("WARNING: AZURE_TRANSLATOR_KEY not found!")
        print("   Demo mode activated (no real translation)")
        print("   To activate Azure Translator:")
        print("   1. Create an Azure Translator service (free tier available)")
        print("   2. Add AZURE_TRANSLATOR_KEY=your_key to .env file")
        print("   3. Or set the AZURE_TRANSLATOR_KEY environment variable")
        print()
        return False
    else:
        key_preview = azure_key[:5] + "..." + azure_key[-3:] if len(azure_key) > 8 else "***"
        print(f"Azure API Key: {key_preview}")
        print()
        return True


def main():
    """Main entry point"""
    config = None
    try:
        # Load configuration
        config = ConfigManager("config.ini")
        
        # Show startup information
        show_startup_info(config)
        
        # Check Azure API key
        has_api_key = check_azure_key()
        
        # Create and start translator
        translator = RealTimeTranslator(config)
        translator.start()
        
    except KeyboardInterrupt:
        print("\nStopped by user request")
    except Exception as e:
        print(f"\nError: {e}")
        if config and config.getboolean('Advanced', 'debug_mode', fallback=False):
            import traceback
            traceback.print_exc()
    finally:
        print("Application closed")


if __name__ == '__main__':
    main()