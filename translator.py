"""
Real-Time Translator Module
Handles speech recognition, translation, and file output
"""

import speech_recognition as sr
import requests
import json
import time
import threading
import os
import uuid
from datetime import datetime
from voice_logger import VoiceLogger
from obs_buffer import OBSBufferManager


class RealTimeTranslator:
    def __init__(self, config_manager):
        self.config = config_manager
        
        # Load Azure key from environment (prioritize .env, then system env)
        self.azure_key = os.getenv('AZURE_TRANSLATOR_KEY')
        
        # Load configuration
        self.azure_region = self.config.get('Azure', 'region')
        self.azure_endpoint = self.config.get('Azure', 'endpoint')
        self.api_version = self.config.get('Azure', 'api_version')
        self.timeout = self.config.getint('Azure', 'timeout')
        
        # Translation settings
        self.from_lang = self.config.get('Translation', 'from_language')
        self.to_lang = self.config.get('Translation', 'to_language')
        self.from_lang_name = self.config.get('Translation', 'from_language_name')
        self.to_lang_name = self.config.get('Translation', 'to_language_name')
        
        # Audio settings
        self.ambient_duration = self.config.getfloat('Audio', 'ambient_noise_duration')
        self.listen_timeout = self.config.getfloat('Audio', 'listen_timeout')
        self.phrase_time_limit = self.config.getfloat('Audio', 'phrase_time_limit')
        self.energy_threshold = self.config.getint('Audio', 'energy_threshold')
        self.dynamic_energy = self.config.getboolean('Audio', 'dynamic_energy_threshold')
        self.pause_threshold = self.config.getfloat('Audio', 'pause_threshold')
        
        # Output settings
        self.output_file = self.config.get('Output', 'obs_file')
        self.log_file = self.config.get('Output', 'log_file')
        self.encoding = self.config.get('Output', 'encoding')
        self.clear_on_start = self.config.getboolean('Output', 'clear_on_start')
        self.include_timestamp = self.config.getboolean('Output', 'include_timestamp')
        self.timestamp_format = self.config.get('Output', 'timestamp_format')
        
        # Display settings
        self.show_original = self.config.getboolean('Display', 'show_original')
        self.show_translation = self.config.getboolean('Display', 'show_translation')
        self.original_prefix = self.config.get('Display', 'original_prefix')
        self.translation_prefix = self.config.get('Display', 'translation_prefix')
        
        # Advanced settings
        self.debug_mode = self.config.getboolean('Advanced', 'debug_mode')
        self.fallback_mode = self.config.get('Advanced', 'fallback_mode')
        
        # Initialize voice logger
        self.voice_logger = VoiceLogger(config_manager)
        
        # Initialize OBS buffer manager
        self.obs_buffer = OBSBufferManager(config_manager)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_running = False
        self.last_translation = ""
        
        # Configure energy threshold
        if self.energy_threshold > 0:
            self.recognizer.energy_threshold = self.energy_threshold
        
        # Setup microphone
        self.setup_microphone()
        
        # Clear output buffer if configured
        if self.clear_on_start:
            self.obs_buffer.clear_buffer()
        
        # Show daily voice log stats
        self.show_voice_log_info()
        
        # Show OBS buffer info
        self.show_obs_buffer_info()
    
    def show_obs_buffer_info(self):
        """Show information about OBS buffer settings"""
        buffer_info = self.obs_buffer.get_buffer_info()
        print(f"OBS Buffer: {buffer_info['max_lines']} lines, each expires after {buffer_info['line_timeout']}s")
        
    def setup_microphone(self):
        """Setup and calibrate microphone"""
        print(f"Calibrating microphone for ambient noise ({self.ambient_duration}s)...")
        print("Please remain quiet during calibration...")
        
        with self.microphone as source:
            # Adjust for ambient noise with longer duration for better accuracy
            self.recognizer.adjust_for_ambient_noise(source, duration=self.ambient_duration)
            
            # Set manual energy threshold if configured, otherwise use auto-adjusted
            if self.energy_threshold > 0:
                self.recognizer.energy_threshold = self.energy_threshold
            
            # Enable dynamic energy threshold adjustment if configured
            self.recognizer.dynamic_energy_threshold = self.dynamic_energy
            
            # Set pause threshold for better phrase detection
            self.recognizer.pause_threshold = self.pause_threshold
            
        print("Calibration completed!")
        print(f"Energy threshold: {self.recognizer.energy_threshold}")
        print(f"Dynamic adjustment: {'enabled' if self.dynamic_energy else 'disabled'}")
        print(f"Pause threshold: {self.pause_threshold}s")
    
    def show_voice_log_info(self):
        """Show information about voice logging"""
        if self.voice_logger.voice_log_enabled:
            stats = self.voice_logger.get_today_stats()
            if stats:
                print(f"Voice logging enabled: {stats['lines']} phrases today")
                print(f"File: {stats['file']}")
            else:
                print("Voice logging enabled (new file)")
        
    def translate_text(self, text):
        """Translate text using Azure Translator API"""
        if not self.azure_key:
            if self.fallback_mode == 'show_original':
                return f"[NO API KEY] {text}"
            elif self.fallback_mode == 'show_error':
                return "[TRANSLATION ERROR: No API Key]"
            else:
                return "[NEEDS TRANSLATION]"
            
        path = '/translate'
        constructed_url = self.azure_endpoint + path

        params = {
            'api-version': self.api_version,
            'from': self.from_lang,
            'to': [self.to_lang]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.azure_key,
            'Ocp-Apim-Subscription-Region': self.azure_region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': text}]

        try:
            request = requests.post(constructed_url, params=params, headers=headers, 
                                  json=body, timeout=self.timeout)
            response = request.json()
            
            if request.status_code == 200 and response:
                return response[0]['translations'][0]['text']
            else:
                if self.debug_mode:
                    print(f"Translation error: {request.status_code} - {response}")
                return self.handle_translation_error(text, f"HTTP {request.status_code}")
                
        except Exception as e:
            if self.debug_mode:
                print(f"Azure API error: {e}")
            return self.handle_translation_error(text, str(e))
    
    def handle_translation_error(self, original_text, error):
        """Handle translation errors based on fallback mode"""
        if self.fallback_mode == 'show_original':
            return f"[ERROR] {original_text}"
        elif self.fallback_mode == 'show_error':
            return f"[TRANSLATION ERROR: {error}]"
        else:
            return "[TRANSLATION FAILED]"
    
    def write_to_file(self, text):
        """Write translation to OBS buffer and log file"""
        try:
            # Add to OBS buffer (handles multi-line display and auto-clear)
            if text.strip():
                self.obs_buffer.add_text(text)
            
            # Write to log file if configured
            if self.log_file and text.strip():
                # Add timestamp for log file
                if self.include_timestamp:
                    timestamp = datetime.now().strftime(self.timestamp_format)
                    log_text = f"{timestamp} {text}"
                else:
                    log_text = text
                    
                with open(self.log_file, 'a', encoding=self.encoding) as f:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"[{timestamp}] {log_text}\n")
                    
        except Exception as e:
            print(f"File write error: {e}")
    
    def listen_continuously(self):
        """Continuously listen for speech in a separate thread"""
        print(f"Continuous listening enabled: {self.from_lang_name} -> {self.to_lang_name}")
        print("Press Ctrl+C to stop...")
        
        while self.is_running:
            try:
                # Listen for audio with timeout
                with self.microphone as source:
                    audio = self.recognizer.listen(source, 
                                                 timeout=self.listen_timeout, 
                                                 phrase_time_limit=self.phrase_time_limit)
                
                # Process in background thread to avoid blocking
                if self.config.getboolean('Performance', 'use_background_processing'):
                    threading.Thread(target=self.process_audio, args=(audio,), daemon=True).start()
                else:
                    self.process_audio(audio)
                
            except sr.WaitTimeoutError:
                # Normal timeout, continue listening
                pass
            except Exception as e:
                if self.debug_mode:
                    print(f"Listen error: {e}")
                time.sleep(1)
    
    def process_audio(self, audio):
        """Process audio in background thread"""
        try:
            # Recognize speech with specified language
            language_code = f"{self.from_lang}-{self.from_lang.upper()}"
            original_text = self.recognizer.recognize_google(audio, language=language_code)
            
            # Log original text to daily voice log
            self.voice_logger.log_original_text(original_text, self.original_prefix.rstrip(':'))
            
            if self.show_original:
                print(f"{self.original_prefix} {original_text}")
            
            # Translate to target language
            translated_text = self.translate_text(original_text)
            
            if self.show_translation:
                print(f"{self.translation_prefix} {translated_text}")
            
            # Update file for OBS
            self.write_to_file(translated_text)
            self.last_translation = translated_text
            
        except sr.UnknownValueError:
            # No speech detected, this is normal
            pass
        except sr.RequestError as e:
            if self.debug_mode:
                print(f"Google Speech error: {e}")
        except Exception as e:
            if self.debug_mode:
                print(f"Processing error: {e}")
    
    def start(self):
        """Start the real-time translation"""
        self.is_running = True
        
        print(f"Real-time translation started!")
        print(f"Output file: {self.output_file}")
        print(f"Translation: {self.from_lang_name} -> {self.to_lang_name}")
        
        if not self.azure_key:
            print("Demo mode (no Azure API key)")
        
        try:
            self.listen_continuously()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the real-time translation"""
        self.is_running = False
        
        # Finalize daily voice log
        self.voice_logger.finalize_daily_log()
        
        # Clean up OBS buffer
        self.obs_buffer.cleanup()
        
        # Show final stats
        if self.voice_logger.voice_log_enabled:
            stats = self.voice_logger.get_today_stats()
            if stats:
                print(f"\nSession ended - {stats['lines']} phrases recorded today")
                print(f"File saved: {stats['file']}")
        
        print("\nTranslation stopped.")