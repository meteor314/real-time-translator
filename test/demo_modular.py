#!/usr/bin/env python3
"""
Demo of the new modular Real-Time Translator with voice logging
This script demonstrates the new features without using the microphone
"""

import os
import sys
from datetime import datetime

# Import the modular components
from config import ConfigManager
from voice_logger import VoiceLogger
from translator import RealTimeTranslator

def demo_voice_logging():
    """Demonstrate the voice logging functionality"""
    print("🎤 Voice Logging Demo")
    print("=" * 30)
    
    # Create config and voice logger
    config = ConfigManager()
    voice_logger = VoiceLogger(config)
    
    # Test phrases
    test_phrases = [
        "Bonjour, bienvenue à ma stream",
        "Aujourd'hui nous allons jouer à un nouveau jeu",
        "N'hésitez pas à me poser des questions dans le chat",
        "Merci pour votre soutien !",
        "À bientôt pour une nouvelle session"
    ]
    
    print("Simulation d'entrées vocales:")
    for i, phrase in enumerate(test_phrases, 1):
        print(f"  {i}. FR: {phrase}")
        voice_logger.log_original_text(phrase, "FR")
    
    # Show stats
    stats = voice_logger.get_today_stats()
    print(f"\n📊 Statistiques:")
    print(f"   Phrases enregistrées: {stats['lines']}")
    print(f"   Fichier: {stats['file']}")
    print(f"   Taille: {stats['size']} bytes")
    
    # Finalize log (as if stopping the app)
    voice_logger.finalize_daily_log()
    print("\n✅ Session finalisée dans le fichier de log quotidien")

def show_modular_structure():
    """Show the new modular structure"""
    print("\n🏗️  Structure Modulaire")
    print("=" * 30)
    
    modules = [
        ("config/__init__.py", "Configuration Manager"),
        ("config/defaults.py", "Default Settings"),
        ("voice_logger.py", "Daily Voice Logging"),
        ("translator.py", "Translation Engine"),
        ("main.py", "Main Application")
    ]
    
    for module, description in modules:
        status = "✅" if os.path.exists(module) else "❌"
        print(f"{status} {module:<20} - {description}")

def demo_configuration():
    """Demonstrate configuration flexibility"""
    print("\n⚙️  Configuration Demo")
    print("=" * 30)
    
    config = ConfigManager()
    
    # Show key settings
    settings = [
        ("Translation", "from_language_name", "Source Language"),
        ("Translation", "to_language_name", "Target Language"), 
        ("Output", "obs_file", "OBS Output File"),
        ("Output", "voice_log_enabled", "Voice Logging"),
        ("Output", "voice_log_directory", "Voice Log Directory"),
        ("Audio", "listen_timeout", "Listen Timeout"),
        ("Display", "show_original", "Show Original Text")
    ]
    
    for section, key, description in settings:
        value = config.get(section, key)
        print(f"  {description:<20}: {value}")

if __name__ == "__main__":
    print("🎯 Modular Real-Time Translator Demo")
    print("=" * 50)
    
    # Show modular structure
    show_modular_structure()
    
    # Show configuration
    demo_configuration()
    
    # Demo voice logging
    demo_voice_logging()
    
    print("\n" + "=" * 50)
    print("🚀 Pour utiliser le système complet:")
    print("   python main.py")
    print("\n💡 Nouvelles fonctionnalités:")
    print("   • Structure modulaire et code organisé")
    print("   • Log quotidien automatique des paroles originales")
    print("   • Configuration séparée dans config/defaults.py")
    print("   • Statistiques de session en temps réel")
    print("=" * 50)