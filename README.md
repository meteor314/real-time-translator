# Real-Time French to English Translation for OBS

This application provides real-time speech recognition and translation from French to English, specifically designed for OBS Studio live streaming. It continuously listens to your microphone, recognizes French speech using Google Speech Recognition, translates it to English using Azure Translator, and writes the translation to a text file that OBS can display.

## Features

- **Continuous Speech Recognition**: Real-time speech detection in any supported language
- **Azure AI Translation**: High-quality translation using Azure Translator (free tier supported)
- **Chat-Like Message Display**: Individual translations appear and disappear like Twitch chat messages
- **OBS Integration**: Outputs translations to a text file for OBS Text Source
- **Multi-Line Buffer**: Display multiple lines at once (configurable 3-4 lines)
- **Per-Line Expiry**: Each line expires independently after a configurable timeout
- **Daily Voice Logging**: Automatically logs original French speech to daily files
- **Error Handling**: Robust error handling and fallback mechanisms
- **Highly Configurable**: Easy customization via config.ini and .env files
- **Multi-Language Support**: Translate between any supported language pairs
- **Modular Architecture**: Clean, maintainable code structure

## Prerequisites

- Python 3.7 or higher
- Microphone connected to your computer
- Azure Translator service (free tier available)
- OBS Studio (for displaying translations)

## Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

### Quick Setup with .env File

1. **Copy the example environment file**:
   ```powershell
   copy .env.example .env
   ```

2. **Edit .env file** and add your Azure API key:
   ```
   AZURE_TRANSLATOR_KEY=your_azure_translator_key_here
   ```

### Advanced Configuration with config.ini

The `config.ini` file allows you to customize all aspects of the translation system:

#### **Translation Settings**
```ini
[Translation]
# Source language (language you speak)
from_language = fr          # French
to_language = en           # English
from_language_name = French
to_language_name = English
```

**Supported Language Codes:**
- `en` = English, `fr` = French, `es` = Spanish, `de` = German
- `it` = Italian, `pt` = Portuguese, `ru` = Russian, `ja` = Japanese
- `ko` = Korean, `zh` = Chinese, `ar` = Arabic, `hi` = Hindi
- And many more! See [Azure Translator Languages](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support)

#### **Audio Settings**
```ini
[Audio]
ambient_noise_duration = 2   # Microphone calibration time (seconds)
listen_timeout = 1          # How long to wait for speech
phrase_time_limit = 5       # Maximum phrase length (seconds)
energy_threshold = 0        # Microphone sensitivity (0 = auto)
```

#### **Output Settings**
```ini
[Output]
obs_file = obs_translation.txt           # File for OBS to read
log_file = translation_log.txt           # Optional logging file
include_timestamp = false                # Add timestamps to translations
timestamp_format = [%%H:%%M:%%S]         # Timestamp format

# Chat-like message buffer for OBS
obs_buffer_lines = 3                     # Number of lines visible at once
obs_auto_clear_timeout = 10              # Seconds before each line expires
obs_line_separator = \n                  # Line separator in OBS file

# Daily voice logging
enable_voice_log = true                  # Log original French speech
voice_log_dir = voice_logs               # Directory for daily logs
voice_log_prefix = voice_log_            # Prefix for log files
```

#### **Display Settings**
```ini
[Display]
show_original = true        # Show original text in console
show_translation = true     # Show translation in console
original_prefix = FR:       # Prefix for original text
translation_prefix = EN:    # Prefix for translated text
```

#### **Performance Settings**
```ini
[Performance]
use_background_processing = true  # Process audio in background
max_concurrent_requests = 3      # Maximum simultaneous translations
max_retries = 2                  # Retry failed translations
```

#### **Advanced Settings**
```ini
[Advanced]
debug_mode = false               # Enable verbose logging
fallback_mode = show_original    # What to do when translation fails
# Options: show_original, show_error, show_placeholder
```

## Azure Translator Setup (Free Tier)

1. **Create Azure Account** (if you don't have one):
   - Go to [Azure Portal](https://portal.azure.com)
   - Sign up for free account (includes $200 credit)

2. **Create Translator Service**:
   - In Azure Portal, click "Create a resource"
   - Search for "Translator"
   - Select "Translator" and click "Create"
   - Choose:
     - **Subscription**: Your subscription
     - **Resource Group**: Create new or use existing
     - **Region**: East US (or your preferred region)
     - **Name**: Choose a unique name
     - **Pricing Tier**: Free F0 (2M characters/month free)

3. **Get Your API Key**:
   - Once created, go to your Translator resource
   - In the Overview tab, find "Manage keys"
   - Copy **Key 1** (this is your API key)
   - Note the **Region** (e.g., "eastus")

4. **Set Environment Variable**:
   ```powershell
   # Windows PowerShell (temporary - for current session)
   $env:AZURE_TRANSLATOR_KEY = "your_api_key_here"
   
   # Windows PowerShell (permanent - for your user)
   [Environment]::SetEnvironmentVariable("AZURE_TRANSLATOR_KEY", "your_api_key_here", "User")
   ```

   Or create a `.env` file in the project directory:
   ```
   AZURE_TRANSLATOR_KEY=your_api_key_here
   ```

## Usage

1. **Start the translator**:
   ```powershell
   python main.py
   ```

2. **The application will**:
   - Calibrate your microphone for ambient noise
   - Start listening continuously for French speech
   - Display recognized French text in the console
   - Show English translations in the console
   - Write translations to `obs_translation.txt`

3. **Stop the application**: Press `Ctrl+C`

## OBS Studio Integration

### Setting Up Text Source

1. **Add Text Source in OBS**:
   - In OBS, add a new Source → Text (GDI+)
   - Name it "Live Translation" or similar

2. **Configure Text Source**:
   - Check "Read from file"
   - Browse and select `obs_translation.txt` from this project directory
   - Customize font, size, color as desired
   - Position the text on your stream layout (usually bottom of screen)

3. **Auto-Refresh**:
   - The text will automatically update as new translations are generated
   - No need to manually refresh

### Chat-Like Message Display

The OBS buffer system creates a chat-like experience where translation messages appear and disappear individually:

**How It Works:**
- Each translation appears as a new line in the buffer
- Multiple lines are visible at once (default: 3 lines)
- Each line expires independently after a timeout (default: 10 seconds)
- New messages push old ones up as they appear
- Lines fade away individually, like Twitch chat messages

**Example Timeline:**
```
Time 0s:  [Line 1 appears]
Time 2s:  [Line 1] [Line 2 appears]
Time 4s:  [Line 1] [Line 2] [Line 3 appears]
Time 6s:  [Line 1] [Line 2] [Line 3] [Line 4 appears - Line 1 pushed out]
Time 10s: [Line 2] [Line 3] [Line 4] (Line 1 expired)
Time 12s: [Line 3] [Line 4] (Line 2 expired)
```

**Configuration:**
```ini
obs_buffer_lines = 3           # Number of lines visible at once
obs_auto_clear_timeout = 10    # Seconds before each line expires
```

**Tips:**
- Use 3-4 lines for optimal readability
- Set timeout to 8-12 seconds for most content
- For slower speech, increase timeout to 15-20 seconds
- For fast-paced streams, decrease to 5-8 seconds

## Daily Voice Logging

The application automatically logs your original French speech to daily files:

**Features:**
- Creates one log file per day: `voice_logs/voice_log_2025-01-15.txt`
- Includes timestamps for each speech entry
- Preserves original French text for review
- Automatic session start/end markers

**Example Log File:**
```
=== Session started at 2025-01-15 14:30:45 ===
[14:30:52] Bonjour tout le monde!
[14:31:15] Aujourd'hui on va jouer à ce nouveau jeu
[14:32:03] C'est vraiment incroyable
=== Session ended at 2025-01-15 15:45:20 ===
```

**Use Cases:**
- Review what you said during streams
- Track vocabulary and phrases
- Create transcripts for content planning
- Analyze speaking patterns

## Project Structure

```
subtitle/
├── main.py                     # Application entry point
├── translator.py               # Core translation engine
├── obs_buffer.py              # Chat-like message buffer
├── voice_logger.py            # Daily voice logging
├── config/
│   ├── __init__.py           # Configuration manager
│   └── defaults.py           # Default settings
├── test/
│   ├── test_obs_buffer.py    # Buffer testing
│   ├── demo_config.py        # Configuration demo
│   └── demo_modular.py       # Modular system demo
├── voice_logs/               # Daily log files (auto-created)
├── config.ini                # User configuration
├── .env                      # API keys
└── requirements.txt          # Python dependencies
```

## Troubleshooting

### "AZURE_TRANSLATOR_KEY not found"
- Make sure you've set the environment variable correctly
- Restart your terminal/PowerShell after setting the variable
- Check your `.env` file exists and contains the key

### "ModuleNotFoundError: No module named 'pyaudio'"
- On Windows, PyAudio can be tricky to install
- Try: `pip install pipwin` then `pipwin install pyaudio`

### Microphone Issues
- Check that your microphone is working and not used by other applications
- Try speaking closer to the microphone
- Check Windows microphone permissions

### Translation Quality
- Speak clearly and at a moderate pace
- Pause briefly between sentences for better recognition
- Background noise can affect speech recognition quality

### OBS Text Not Updating
- Make sure OBS has permission to read the file
- Check that the file path in OBS matches the output file location
- Try refreshing the OBS source manually

### Lines Not Expiring
- Check `obs_auto_clear_timeout` value in config.ini
- Verify the cleanup thread is running (console should show buffer info at startup)
- Test with `test/test_obs_buffer.py` to verify buffer behavior

## Performance Tips

- **For better performance**: Close unnecessary applications that might use the microphone
- **For lower latency**: Use a good quality USB microphone
- **For better recognition**: Speak in short, clear sentences
- **For streaming**: Position the translation text in a non-distracting area of your stream

## API Usage and Costs

- **Free Tier**: 2 million characters per month
- **Typical Usage**: ~50-100 characters per sentence
- **Estimate**: Several hours of continuous translation per month for free
- **Monitoring**: Check Azure Portal for usage statistics

## Limitations

- Requires internet connection for both speech recognition and translation
- Translation quality depends on speech clarity and background noise
- Free tier has monthly character limits
- Real-time performance depends on network latency

## Support

For issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Test your microphone in other applications
4. Check Azure Translator service status

## License

This project is for educational and personal use. Make sure to comply with Azure Translator service terms and Google Speech Recognition terms of use.