# lesson_generator/config.py

from pathlib import Path

SEPARATOR_CONFIG = {
    "exercise_tone": {
        "file": Path("sounds") / "next_excercise_tone.mp3",
        "pause_before": 1000,
        "pause_after": 1000,
        "volume_reduction_db": 0,
    },
    "task_tone": {
        "file": Path("sounds") / "next_task_ping.mp3",
        "pause_before": 1000,
        "pause_after": 1000,
        "volume_reduction_db": -10,
    },
}

# Beispiel: Stimmen pro Sprache (Beliebige Kombinationen möglich)
VOICE_CONFIG = {
    "en": "english_voice_id",
    "fr": "french_voice_id",
    "es": "spanish_voice_id",
    "de": "onwK4e9ZLuTAKqWW03F9",  # Daniel pre-made voice
    "nl": "9BWtsMINqrJLrRacOk9x"  # Aria pre-made voice
    # etc.
    # Falls Sprache nicht definiert, nutze "default_voice" oder Standardstimme
}
