#!/usr/bin/env python3
"""
Test script for Azure Translator functionality
This script tests the translation without using the microphone
"""

import os
import sys
sys.path.append('.')
from main import RealTimeTranslator

def test_translation():
    print("=== Test de traduction Azure ===")
    
    # Get API key
    azure_key = os.getenv('AZURE_TRANSLATOR_KEY')
    
    if not azure_key:
        print("⚠️  AZURE_TRANSLATOR_KEY non définie")
        print("Le test utilisera le mode démo")
        print()
    
    # Create translator
    translator = RealTimeTranslator(
        azure_key=azure_key,
        azure_region="eastus",
        output_file="test_translation.txt"
    )
    
    # Test phrases in French
    test_phrases = [
        "Bonjour tout le monde",
        "Comment allez-vous aujourd'hui?",
        "J'espère que vous passez une excellente journée",
        "Merci beaucoup pour votre attention",
        "C'est un plaisir de vous parler"
    ]
    
    print("Test des traductions:")
    print("-" * 50)
    
    for phrase in test_phrases:
        translation = translator.translate_text(phrase)
        print(f"FR: {phrase}")
        print(f"EN: {translation}")
        print()
        
        # Write to test file
        translator.write_to_file(translation)
    
    print("✅ Test terminé!")
    print(f"Dernière traduction écrite dans: test_translation.txt")

if __name__ == "__main__":
    test_translation()