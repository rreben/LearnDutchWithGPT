# README

Welcome to the **Multilingual Lesson Audio Generator**! This project provides a way to transform lesson content (structured as JSON) into a comprehensive audio lesson that you can share with learners. The program supports various languages and uses Text-to-Speech (TTS) and optional separator tones to guide students through exercises and tasks.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Developer Guide](#developer-guide)
8. [License](#license)

## Overview

The **Multilingual Lesson Audio Generator** converts a JSON description of a lesson—containing a title, a description, multiple exercises, and tasks—into an MP3 file. Each piece of text is read using a TTS service (e.g., ElevenLabs), and configurable tones are inserted between sections to structure the audio.

Typical use cases:

- Language-learning apps or websites
- Self-study audio materials
- Automated creation of audio exercises for any subject

By editing the configuration and JSON content, you can adapt this tool for any language or domain.

## Features

- **Flexible TTS**: Use any Text-to-Speech service (e.g., [ElevenLabs](https://elevenlabs.io/)), configured in the code.
- **Multilingual**: Supports any language combination by mapping each language code to a voice ID in the config.
- **Separator Tones**: Insert custom audio pings or tones between exercises and tasks.
- **JSON Validation**: Ensures your lesson JSON has the correct structure before generating the audio.
- **Command Line Interface (CLI)**: Easily generate lessons via terminal commands (using [Click](https://click.palletsprojects.com/)).

## Installation

1. **Clone the repository** or download the source code.
2. **Install requirements**:

```bash
   pip install -r requirements.txt
```

Ensure you have a Python 3.8+ environment set up.

## Usage

Prepare your lesson JSON file (e.g., lesson.json). Make sure it follows the expected structure (title, description, exercises, tasks, etc.).

### Run the CLI to convert your JSON into audio

```bash
python lesson_cli.py --input-file path/to/lesson.json --output-file lesson_output.mp3
```

Short options:

```bash
Code kopieren
python lesson_cli.py -i path/to/lesson.json -o lesson_output.mp3
```

### Check additional options

Display help

```bash
python lesson_cli.py --help
```

Display version:

```bash
python lesson_cli.py --version
```

or

```bash
python lesson_cli.py -v
```

Once the command completes, you will have an MP3 file that begins with the lesson title, follows with the description, then goes through all exercises and their tasks.

## Project Structure

Below is an example structure for the project:

```ascii
multilingual_lesson_project/
├── lesson_generator/
│   ├── __init__.py
│   ├── audio_generation.py
│   ├── config.py
│   ├── json_validation.py
│   └── ...
├── lesson_cli.py
├── requirements.txt
├── README.md
└── sounds/
    ├── next_excercise_tone.mp3
    └── next_task_ping.mp3
```

- ```lesson_generator/``` Contains all main logic:
- ```audio_generation.py``` for handling TTS, combining audio segments, etc.
- ```config.py``` for storing configurations (voice mappings, separator tones, etc.).
- ```json_validation.py``` for validating the JSON structure.
- ```lesson_cli.py```
The CLI script using Click. Provides the entry point to generate audio from your JSON.
- ```sounds/```
Stores custom tones (e.g., separator tones).

## Configuration

You can customize the behavior of the tool by editing config.py:

```python
from pathlib import Path

SEPARATOR_CONFIG = {
    "exercise_tone": {
        "file": Path("sounds") / "next_excercise_tone.mp3",
        "pause_before": 1000,
        "pause_after": 1000,
        "volume_reduction_db": 0
    },
    "task_tone": {
        "file": Path("sounds") / "next_task_ping.mp3",
        "pause_before": 1000,
        "pause_after": 1000,
        "volume_reduction_db": -10
    }
}

VOICE_CONFIG = {
    "en": "english_voice_id",
    "fr": "french_voice_id",
    "nl": "dutch_voice_id",
    # ...
    "default_voice": "fallback_voice_id"
}
```

- ```SEPARATOR_CONFIG```: Controls which MP3 file to play and how much silence to insert before/after each tone.
- ```VOICE_CONFIG```: Maps language codes to specific TTS voices. If a language code isn’t found, default_voice is used.

## Developer Guide

1. The version number can be adjusted in ```__init__.py```, and then the library can be installed using ```pip install -e .```

2. Extend or Modify Audio Logic To use a different TTS service, replace the calls in audio_generation.py with the relevant API calls.
If you want more advanced audio editing, explore pydub features (fading, overlays, etc.).
JSON Validation

3. Check out json_validation.py to see how required fields are validated. Adjust this logic if your lesson structure changes.
Testing

4. You can create unit tests (e.g., with pytest) to ensure the JSON validation and audio generation are working as expected.
CLI Customization

5. Edit ```lesson_cli.py``` to add new options (e.g., changing the TTS model, adjusting voice stability, etc.).

6. You can also create sub-commands using Click’s @click.group().
Logging and Debugging

7. Add logging statements in your code to track progress and debug issues. Python’s logging module is commonly used.
Versioning
   - In ```lesson_generator/__init__.py```, you can keep track of a version:

   ```python
   __version__ = "0.1.0"
   ```

   - This is displayed via --version in the CLI if you’ve set up @click.version_option(...).

8. Please keep the ```requirments.txt``` file up to date. You may want to use ```pip freeze > requirements.txt``` for this purpose

## License

See the licence file.

Happy coding! If you encounter any issues or want to contribute, feel free to open a pull request or create an issue in the repository.
