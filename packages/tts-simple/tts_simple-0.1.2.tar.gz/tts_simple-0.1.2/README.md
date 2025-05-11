# Text-to-Speech (TTS) Simple (by HMCorp)

This repository provides a simple implementation of a Text-to-Speech (TTS) system. It allows users to generate speech audio files (MP3 or WAV) from text files. The project is designed to be lightweight and easy to use.

## Features
- Convert text files into MP3 or WAV audio files
- Support for multiple languages (over 50 languages supported)
- Various voice accents for certain languages
- Cross-platform support for macOS, Windows, and Linux
- Easy setup and usage

## Requirements
- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (only for WAV file conversion)

## Installation

### Using pip
1. Install Python (if not already installed):
    - On macOS:
        ```bash
        brew install python
        ```
    - On Windows:
        Download and install Python from [python.org](https://www.python.org/). Ensure you check the box to add Python to your PATH during installation.

2. Install the package:
    ```bash
    pip install tts-simple
    ```
    This will automatically install all required Python dependencies.

3. Install FFmpeg for WAV file generation (optional):
    - On macOS:
        ```bash
        brew install ffmpeg
        ```
    - On Windows:
        Download and install FFmpeg from [FFmpeg.org](https://ffmpeg.org/). Add the FFmpeg binary to your system PATH.

## Usage

### Command Line Interface

Convert a text file to speech with default settings (English, MP3):
```bash
tts-simple input.txt
```

Specify output file:
```bash
tts-simple input.txt output
```

Convert to WAV format:
```bash
tts-simple input.txt -f wav
```

Use a different language:
```bash
tts-simple input.txt -l es  # Spanish
```

Change voice accent:
```bash
tts-simple input.txt -t co.uk  # British English
```

Use slower speech:
```bash
tts-simple input.txt -s
```

List all available languages and voices:
```bash
tts-simple --list
```

### Python API
You can also use the library in your Python code:
```bash
from tts_simple import text_to_speech

# Generate speech in English (default)
text_to_speech("input.txt", "output", language="en", output_format="mp3")

# Generate speech in Spanish with slower speed
text_to_speech("input.txt", "output_spanish", language="es", speed=True)

# Generate speech with British accent 
text_to_speech("input.txt", "output_british", tld="co.uk")
```

## Dependencies
The package automatically installs all required Python dependencies, which include:

- gTTS (Google Text-to-Speech)
- FFmpeg (is required only if you want to generate WAV files).

## Notes
- The default output format is MP3
- If no output file is specified, the input filename (with appropriate audio extension) will be used
- TLD options (voice accents) work best with English language

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## Contact
For questions or support, please contact [apavlenko@hmcorp.fund].