# Text-to-Speech (TTS) Simple (by HMCorp)

This repository provides a simple implementation of a Text-to-Speech (TTS) system. It allows users to generate speech audio files (e.g., `.wav`) from text input. The project is designed to be lightweight and easy to use.

## Features
- Convert text input into `.wav` audio files.
- Cross-platform support for macOS and Windows.
- Easy setup and usage.

## Requirements
- Python 3.8 or higher
- pip (Python package manager)

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

3. Install FFmpeg for `.wav` file generation:
    - On macOS:
        ```bash
        brew install ffmpeg
        ```
    - On Windows:
        Download and install FFmpeg from [FFmpeg.org](https://ffmpeg.org/). Add the FFmpeg binary to your system PATH.

## Usage
1. Run the script:
    ```bash
    python tts_simple.py --text "Hello, world!" --output output.wav
    ```
    Replace `"Hello, world!"` with your desired text and `output.wav` with your desired output file name.

2. Example:
    ```bash
    python tts_simple.py --text "This is a test." --output test.wav
    ```

## Dependencies
The project uses the following Python libraries:
- `gTTS` (Google Text-to-Speech)
- `pydub` (for audio processing)
- `ffmpeg` (for `.wav` file generation)

Install these dependencies via:
```bash
pip install gTTS pydub
```

## Notes
- Ensure FFmpeg is correctly installed and added to your PATH for `.wav` file generation.
- The script is designed for educational purposes and may require additional tuning for production use.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## Contact
For questions or support, please contact [apavlenko@hmcorp.fund].