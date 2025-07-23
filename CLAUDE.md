# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LearnDutchWithGPT is a multilingual audio lesson generator that converts structured JSON lesson content into comprehensive MP3 audio files using Text-to-Speech technology. The project focuses on Dutch language learning but supports multiple languages through configurable voice mappings.

## Common Commands

### Development Setup
```bash
# Install the package in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

### Main CLI Usage
```bash
# Generate audio lesson from JSON
python lesson_cli.py -i lesson_input_files/001_example.json -o lessons_output_files/lesson.mp3

# Export teacher texts to Anki import file
python lesson_cli.py -i input.json -o output.mp3 -e anki_import.txt

# Apply audio compression
python lesson_cli.py -i input.json -o output.mp3 -c

# Show help and version
python lesson_cli.py --help
python lesson_cli.py --version
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_lesson_cli.py
```

### Web Interface
```bash
# Start Flask development server
python flask_app/app.py
```

## Code Architecture

### Core Processing Pipeline
The application follows a modular pipeline: `JSON Input → Validation → TTS Generation → Audio Segmentation → Combination → MP3 Export`

### Key Components

**lesson_generator/** - Core package containing:
- `audio_generation.py` - Main TTS integration and audio processing logic
- `config.py` - Voice mappings (`VOICE_CONFIG`) and separator tone configuration (`SEPARATOR_CONFIG`) 
- `json_validation.py` - Validates lesson JSON structure against required schema

**lesson_cli.py** - Primary CLI interface using Click framework. Entry point configured as `lesson-cli` console script.

**flask_app/** - Web interface for lesson editing with templates and data persistence.

### Configuration System

Voice mappings are defined in `lesson_generator/config.py`:
```python
VOICE_CONFIG = {
    "de": "onwK4e9ZLuTAKqWW03F9",  # German (Daniel)
    "nl": "hLnc7y4d152WGG2BQlAY"   # Dutch (Jamie)
}
```

Separator tones are configured with timing and volume controls in `SEPARATOR_CONFIG`.

### JSON Lesson Schema

Lessons must follow this hierarchical structure:
- `lesson.title` - Lesson title with text and language_code
- `lesson.description` - Lesson description  
- `lesson.exercises[]` - Array of exercises, each containing:
  - `explanation` - Exercise explanation
  - `tasks[]` - Array of tasks with teacher_speaks, student_response_time, teacher_solution, and separator controls

### TTS Integration

Primary TTS service is ElevenLabs API. The system requires `ELEVENLABS_API_KEY` environment variable. OpenAI TTS is available as secondary option via `OPENAI_API_KEY`.

### Audio Processing

Uses PyDub for audio manipulation including:
- Combining multiple audio segments
- Adding separator tones with configurable pauses
- Volume adjustment and compression options
- MP3 export with proper formatting

## Key Directories

- `lesson_input_files/` - JSON lesson definitions organized by topic
- `lessons_output_files/` - Generated MP3 audio files  
- `sounds/` - Separator tone audio assets (`next_excercise_tone.mp3`, `next_task_ping.mp3`)
- `tests/testfiles/` - Test data and fixtures
- `flask_app/templates/` - Web UI templates

## Environment Requirements

- Python 3.8+ (project uses 3.11+)
- Required API keys in environment or `.env` file:
  - `ELEVENLABS_API_KEY` (required)
  - `OPENAI_API_KEY` (optional)