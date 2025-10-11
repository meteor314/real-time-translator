"""
Default configuration settings for Real-Time Translator
This file contains all the default configuration values to keep the main code clean
"""

DEFAULT_CONFIG = {
    'Translation': {
        'from_language': 'fr',
        'to_language': 'en',
        'from_language_name': 'French',
        'to_language_name': 'English'
    },
    'Azure': {
        'region': 'eastus',
        'endpoint': 'https://api.cognitive.microsofttranslator.com',
        'api_version': '3.0',
        'timeout': '5'
    },
    'Audio': {
        'ambient_noise_duration': '3',
        'listen_timeout': '2',
        'phrase_time_limit': '10',
        'energy_threshold': '0',
        'dynamic_energy_threshold': 'true',
        'pause_threshold': '0.8'
    },
    'Output': {
        'obs_file': 'obs_translation.txt',
        'log_file': 'translation_log.txt',
        'encoding': 'utf-8',
        'clear_on_start': 'true',
        'include_timestamp': 'false',
        'timestamp_format': '[%%H:%%M:%%S]',  # Escaped % for configparser
        'voice_log_enabled': 'true',
        'voice_log_directory': 'voice_logs',
        'obs_buffer_lines': '3',
        'obs_auto_clear_timeout': '5',
        'obs_line_separator': '\\n'
    },
    'Display': {
        'show_original': 'true',
        'show_translation': 'true',
        'show_confidence': 'false',
        'original_prefix': 'FR:',
        'translation_prefix': 'EN:',
        'use_colors': 'false'
    },
    'Performance': {
        'use_background_processing': 'true',
        'max_concurrent_requests': '3',
        'max_retries': '2',
        'retry_delay': '1'
    },
    'Advanced': {
        'recognition_service': 'google',
        'skip_silence': 'true',
        'silence_threshold': '0.5',
        'debug_mode': 'false',
        'fallback_mode': 'show_original'
    }
}