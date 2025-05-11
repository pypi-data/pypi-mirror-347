from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tts-simple",
    version="0.1.1",
    author="Anton Pavlenko",
    author_email="apavlenko@hmcorp.fund",  # Replace with your email
    description="Simple text-to-speech converter with multiple languages and voices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HMCorp-Fund/tts_simple",  # Replace with your repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "gTTS>=2.2.0",
    ],
    entry_points={
        "console_scripts": [
            "tts-simple=tts_simple.core:main",
        ],
    },
)