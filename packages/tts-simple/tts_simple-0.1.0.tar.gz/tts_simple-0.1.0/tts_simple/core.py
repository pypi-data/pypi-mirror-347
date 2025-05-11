import os
import subprocess
from gtts import gTTS # type: ignore
from gtts.lang import tts_langs # type: ignore

def get_available_languages():
    """
    Get all available languages supported by gTTS
    
    Returns:
        dict: Dictionary of language codes and names
    """
    return tts_langs()

def get_available_tlds():
    """
    Get all available TLDs (accents) for gTTS
    
    Returns:
        dict: Dictionary of TLDs and their descriptions
    """
    return {
        'com': 'US English (default)',
        'co.uk': 'British English',
        'com.au': 'Australian English',
        'co.in': 'Indian English',
        'ca': 'Canadian English',
        'ie': 'Irish English',
        'co.za': 'South African English',
        # TLDs work mostly with English but some other languages may have regional variations
    }

def display_available_options():
    """Display all available languages and voice options"""
    languages = get_available_languages()
    tlds = get_available_tlds()
    
    print("\nAVAILABLE LANGUAGES:")
    print("===================")
    for code, name in sorted(languages.items()):
        print(f"{code}: {name}")
    
    print("\nAVAILABLE VOICE ACCENTS (TLDs):")
    print("==============================")
    for tld, description in tlds.items():
        print(f"{tld}: {description}")
    print("\nNote: TLD options work best with English language. For other languages, effects may vary.")

def text_to_speech(input_file, output_file, language='en', output_format='mp3', tld='com', speed=False):
    """
    Convert text from a file to speech and save as audio file
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output audio file (without extension)
        language (str): Language code (default: 'en')
        output_format (str): Output format, either 'mp3' or 'wav' (default: 'mp3')
        tld (str): Top level domain for accent variation (com, co.uk, etc.) (default: 'com')
        speed (bool): If True, slows down the speech (default: False)
    
    Returns:
        str: Path to the generated audio file
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read text from file
    print("Reading input file...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        # Try another common encoding if UTF-8 fails
        with open(input_file, 'r', encoding='latin-1') as f:
            text = f.read()
    
    if not text:
        raise ValueError("Input file is empty")
    
    # Generate temporary MP3 file (gTTS only outputs MP3)
    temp_mp3 = f"{output_file}.mp3"
    
    # Show voice info and convert text to speech
    print(f"Generating speech [language: {language}, accent: {tld}, slow: {speed}]...")
    tts = gTTS(text=text, lang=language, slow=speed, tld=tld)
    tts.save(temp_mp3)
    
    # Convert to WAV if needed
    if output_format.lower() == 'wav':
        final_path = f"{output_file}.wav"
        
        # Use ffmpeg directly via subprocess
        print("Converting to WAV format...")
        try:
            subprocess.run(
                ['ffmpeg', '-y', '-i', temp_mp3, final_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Remove the temporary MP3 file
            os.remove(temp_mp3)
            print("Conversion complete.")
            return final_path
        except subprocess.CalledProcessError as e:
            print(f"Error converting to WAV: {e}")
            print(f"Keeping MP3 file: {temp_mp3}")
            return temp_mp3
    else:
        print("Processing complete.")
        return temp_mp3

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert text file to speech")
    parser.add_argument("input_file", nargs="?", help="Path to the input text file")
    parser.add_argument("output_file", nargs="?", help="Path to the output audio file (without extension). If not specified, input filename will be used.")
    parser.add_argument("-l", "--language", default="en", help="Language code (default: en)")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "wav"], 
                        help="Output format (mp3 or wav)")
    parser.add_argument("-t", "--tld", default="com", 
                        help="Top level domain for accent variation (com, co.uk, com.au, etc.)")
    parser.add_argument("-s", "--slow", action="store_true", 
                        help="Use slower speech rate")
    parser.add_argument("--list", action="store_true",
                        help="List all available languages and voice options")
    
    args = parser.parse_args()
    
    # Display available options if requested
    if args.list:
        display_available_options()
        return 0
    
    # Check if input file is provided when not listing options
    if args.input_file is None:
        parser.error("input_file is required unless --list is specified")
        
    # Set output file name based on input file if not specified
    if args.output_file is None:
        # Extract the base input filename without extension
        base_filename = os.path.splitext(os.path.basename(args.input_file))[0]
        # Use the directory of the input file for output
        input_dir = os.path.dirname(args.input_file)
        if input_dir:
            output_file = os.path.join(input_dir, base_filename)
        else:
            output_file = base_filename
        print(f"No output file specified. Using input filename: {output_file}")
    else:
        output_file = args.output_file
    
    output_path = text_to_speech(
        args.input_file, 
        output_file,
        args.language,
        args.format,
        args.tld,
        args.slow
    )
    
    print(f"Speech successfully generated: {output_path}")
    return 0

if __name__ == "__main__":
    main()