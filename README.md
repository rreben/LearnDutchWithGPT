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

The core input for the lesson generator is a structured JSON file that defines the lesson content, exercises, and tasks.

### JSON Lesson Structure

The JSON file must follow this hierarchical structure. Here's an example based on the sailing terminology lesson:

```json
{
  "lesson": {
    "title": {
      "text": "Segelbegriffe an Bord",
      "language_code": "de"
    },
    "description": {
      "text": "In dieser Lektion werden wichtige Begriffe an Bord eines Segelbootes besprochen.",
      "language_code": "de"
    },
    "exercises": [
      {
        "explanation": {
          "text": "Übersetze die Sätze ins Niederländische. Danach hör Dir die Lösung an und vergleiche.",
          "language_code": "de"
        },
        "tasks": [
          {
            "teacher_speaks": {
              "text": "Die Pinne dient zur Steuerung des Bootes.",
              "language_code": "de"
            },
            "student_response_time": 5000,
            "teacher_solution": {
              "text": "De helmstok wordt gebruikt om de boot te sturen.",
              "language_code": "nl"
            },
            "play_separator_tone": true
          }
        ]
      }
    ]
  }
}
```

### Required Fields

- **lesson.title**: Lesson title with text and language code
- **lesson.description**: Brief description of what the lesson covers
- **lesson.exercises**: Array of exercises, each containing:
  - **explanation**: What this exercise focuses on
  - **tasks**: Array of individual learning tasks with:
    - **teacher_speaks**: Instruction or question (typically in German)
    - **student_response_time**: Pause duration in milliseconds for student response
    - **teacher_solution**: Expected answer (typically in Dutch)
    - **play_separator_tone**: Whether to play a tone after this task

### Language Codes

Currently supported language codes:

- `"de"` - German (uses Daniel voice)
- `"nl"` - Dutch (uses Jamie voice)

### Example Files

You can find complete example JSON files in the `lesson_input_files/` directory:

- `001_Segeln_Begriffe.json` - Sailing terminology
- `002_Segeln_Anlegen_Ankern.json` - Docking and anchoring
- `003_Segeln_Wind_Kurs_Motor.json` - Wind, course and motor
- `004_Vokabel_und_Wortstellung.json` - Vocabulary and word order

### Generate Audio from JSON

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

### Export Anki Flashcards

You can export the lesson content as Anki flashcards using the `-e` or `--export-texts` option:

```bash
python lesson_cli.py -i lesson_input_files/001_Segeln_Begriffe.json -o lesson.mp3 -e
```

This creates an `anki_import.txt` file by default. You can specify a custom filename:

```bash
python lesson_cli.py -i lesson_input_files/001_Segeln_Begriffe.json -o lesson.mp3 -e my_anki_cards.txt
```

The export creates:

- **Anki import file**: Tab-separated text file with teacher instructions and solutions
- **Audio files**: Individual MP3 files for each solution in the `tmp_output/` directory
- **Main lesson MP3**: Complete audio lesson as usual

### Importing into Anki

1. **Import the text file**:
   - Open Anki and select your deck
   - Go to File → Import
   - Select the generated text file (e.g., `anki_import.txt`)
   - Set field separator to "Semicolon"
   - Map fields: Field 1 → Front, Field 2 → Back
   - Click Import

2. **Add audio files**:
   - Copy all MP3 files from the `tmp_output/` directory
   - Paste them into your Anki media folder:
     - **Windows**: `%APPDATA%\Anki2\[Profile]\collection.media\`
     - **Mac**: `~/Library/Application Support/Anki2/[Profile]/collection.media/`
     - **Linux**: `~/.local/share/Anki2/[Profile]/collection.media/`

3. **Verify**: The flashcards will show the teacher instruction on the front and the solution with audio on the back.

### Audio Compression

For improved listening experience, you can apply audio compression using the `-c` or `--use-compression` option:

```bash
python lesson_cli.py -i lesson_input_files/001_Segeln_Begriffe.json -o lesson.mp3 -c
```

**Why use compression?**

- **Consistent volume levels**: Ensures teacher instructions, student response times, and solutions all play at similar volumes
- **Better learning experience**: No need to constantly adjust volume during the lesson
- **Professional audio quality**: Reduces distracting volume differences between different text-to-speech segments

The compression evens out quiet and loud passages, making the entire lesson more comfortable to listen to, especially when using headphones or in varying acoustic environments.

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
