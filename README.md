# Real-Time French to English Translation for OBS

This application provides real-time speech recognition and translation from French to English, specifically designed for OBS Studio live streaming. It continuously listens to your microphone, recognizes French speech using Google Speech Recognition, translates it to English using Azure Translator, and writes the translation to a text file that OBS can display.

## Features

- 🎤 **Continuous Speech Recognition**: Real-time speech detection in any supported language
- 🌐 **Azure AI Translation**: High-quality translation using Azure Translator (free tier supported)
- 📺 **OBS Integration**: Outputs translations to a text file for OBS Text Source
- 🔄 **Real-time Updates**: Immediate translation updates as you speak
- 🛡️ **Error Handling**: Robust error handling and fallback mechanisms
- ⚙️ **Highly Configurable**: Easy customization via config.ini and .env files
- 🌍 **Multi-Language Support**: Translate between any supported language pairs
- 📝 **Logging**: Optional translation logging and timestamping

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
obs_file = obs_translation.txt    # File for OBS to read
log_file = translation_log.txt    # Optional logging file
include_timestamp = false         # Add timestamps to translations
timestamp_format = [%%H:%%M:%%S]  # Timestamp format
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

1. **Add Text Source in OBS**:
   - In OBS, add a new Source → Text (GDI+)
   - Name it "Live Translation" or similar

2. **Configure Text Source**:
   - Check "Read from file"
   - Browse and select `obs_translation.txt` from this project directory
   - Customize font, size, color as desired
   - Position the text on your stream layout

3. **Auto-Refresh**:
   - The text will automatically update as new translations are generated
   - No need to manually refresh

## Configuration Options

You can modify these settings in `main.py`:

```python
translator = RealTimeTranslator(
    azure_key=azure_key,
    azure_region="eastus",  # Change to your Azure region
    output_file="obs_translation.txt"  # Change output filename if needed
)
```

## Troubleshooting

### "AZURE_TRANSLATOR_KEY non trouvée"
- Make sure you've set the environment variable correctly
- Restart your terminal/PowerShell after setting the variable
- The app will work in demo mode without translation if no key is provided

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