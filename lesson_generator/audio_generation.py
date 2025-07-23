# audio_generation.py

import io
import json
import os
import uuid  # Für UUID-Generierung

# pydub zum Arbeiten mit Audios
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range  # Komprimierung importieren

# ElevenLabs (oder anderer TTS-Dienst) - hier als Beispiel
# Du musst sicherstellen, dass "client" importiert oder initialisiert ist,
# z. B. aus einem anderen Modul oder über ein globales Objekt.
from elevenlabs import VoiceSettings

# Eigene Konfiguration importieren:
# (Du brauchst in deinem Projekt eine config.py mit SEPARATOR_CONFIG,
# VOICE_CONFIG usw.)
from .config import SEPARATOR_CONFIG, VOICE_CONFIG

# Hier solltest du den ElevenLabs-Client bzw. TTS-Client definieren
# oder importieren.
# Beispiel:
# from .some_other_module import client


def convert_to_audio_segment(byte_iterator, format='mp3'):
    """
    Nimmt einen Iterator oder Bytes-Objekt für Audio (z. B. TTS-Antwort)
    entgegen und wandelt ihn in ein pydub.AudioSegment um.
    """
    audio_data = io.BytesIO()
    for chunk in byte_iterator:
        audio_data.write(chunk)
    audio_data.seek(0)
    return AudioSegment.from_file(audio_data, format=format)


def validate_json_structure(json_data: str) -> bool:
    """
    Validiert, ob die JSON-String 'json_data' die erwartete Struktur
    (lesson -> title, description, exercises -> tasks usw.) enthält.
    Gibt True zurück, wenn alles ok, sonst False.
    """
    try:
        lesson_data = json.loads(json_data)

        if "lesson" not in lesson_data:
            raise ValueError("Missing 'lesson' key in JSON data")

        # Titel prüfen
        if "title" not in lesson_data["lesson"]:
            raise ValueError("Missing 'title' key in 'lesson'")
        if not all(
            k in lesson_data["lesson"]["title"]
            for k in ["text", "language_code"]
        ):
            raise ValueError(
                "Lesson 'title' must have 'text' and 'language_code'"
            )

        # Beschreibung prüfen
        if "description" not in lesson_data["lesson"]:
            raise ValueError("Missing 'description' key in 'lesson'")
        if not all(
            k in lesson_data["lesson"]["description"]
            for k in ["text", "language_code"]
        ):
            raise ValueError(
                "Lesson 'description' must have 'text' and 'language_code'"
            )

        # Übungen prüfen
        if "exercises" not in lesson_data["lesson"]:
            raise ValueError("Missing 'exercises' key in 'lesson'")
        for exercise in lesson_data["lesson"]["exercises"]:
            if "explanation" not in exercise:
                raise ValueError("Each exercise must have an 'explanation'")
            if not all(
                k in exercise["explanation"]
                for k in ["text", "language_code"]
            ):
                raise ValueError(
                    "Exercise 'explanation' must have 'text' and "
                    "'language_code'"
                )
            if "tasks" not in exercise:
                raise ValueError("Each exercise must have a 'tasks' list")

            for task in exercise["tasks"]:
                if "teacher_speaks" not in task:
                    raise ValueError("Each task must have 'teacher_speaks'")
                if not all(
                    k in task["teacher_speaks"]
                    for k in ["text", "language_code"]
                ):
                    raise ValueError(
                        "'teacher_speaks' must have 'text' and 'language_code'"
                    )

                if "student_response_time" not in task:
                    raise ValueError(
                        "Each task must have 'student_response_time'"
                    )

                if "teacher_solution" not in task:
                    raise ValueError(
                        "Each task must have 'teacher_solution'"
                    )
                if not all(
                    k in task["teacher_solution"]
                    for k in ["text", "language_code"]
                ):
                    raise ValueError(
                        "'teacher_solution' must have 'text' and "
                        "'language_code'"
                    )

                if "play_separator_tone" not in task:
                    raise ValueError(
                        "Each task must have 'play_separator_tone'"
                    )

    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON validation error: {e}")
        return False

    return True


def normalize_segment(audio_segment, target_dBFS=-20.0):
    """
    Normalisiert ein AudioSegment auf die Ziel-Lautstärke (target_dBFS).
    """
    current_dBFS = audio_segment.dBFS
    change_in_dBFS = target_dBFS - current_dBFS
    return audio_segment.apply_gain(change_in_dBFS)


def compress_audio_segment(audio_segment, threshold=-20.0, ratio=4.0):
    """
    Komprimiert die Dynamik des AudioSegments: Reduziert Unterschiede
    zwischen leisen und lauten Passagen.

    :param audio_segment: Das zu komprimierende AudioSegment
    :param threshold: Lautheitsschwelle in dB
                      (Alles über diesem Wert wird reduziert)
    :param ratio: Verhältnis der Komprimierung. Z.B. 4.0 bedeutet, dass laute
                  Stellen um den Faktor 4 reduziert werden.
    :return: Komprimiertes AudioSegment
    """
    return compress_dynamic_range(
        audio_segment, threshold=threshold, ratio=ratio
    )


def generate_speech_segment(client, voice_id: str, text: str) -> AudioSegment:
    """
    Ruft die TTS-API (ElevenLabs oder anderen Dienst) auf,
    um 'text' mit der gewünschten Stimme 'voice_id' zu generieren
    und gibt ein AudioSegment zurück.
    """
    print(f"Generating speech for '{text}' with voice '{voice_id}'...")
    # Beispiel mit ElevenLabs:
    # (Du brauchst einen globalen 'client' oder importierten 'client')
    # Hier setzen wir beispielhaft Voice-Einstellungen.
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_22050_32",
        optimize_streaming_latency="0",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    segment = convert_to_audio_segment(response, format='mp3')
    # Normalisierung auf Ziel-Lautstärke (-20 dBFS empfohlen) ***
    segment = normalize_segment(segment, target_dBFS=-20.0)
    return segment


def generate_separator_tone(tone_type: str) -> AudioSegment:
    """
    Lädt einen definierten Trennton aus SEPARATOR_CONFIG
    (z. B. 'exercise_tone', 'task_tone')
    und fügt Pausen (vor/nach) sowie eine eventuelle Lautstärkereduktion
    hinzu.
    Gibt ein AudioSegment zurück. Falls kein File gefunden wird,
    wird 0 ms Stille erzeugt.
    """
    tone_config = SEPARATOR_CONFIG.get(tone_type)
    if tone_config:
        tone_file = tone_config["file"]
        if tone_file.exists():
            # MP3 laden
            tone = AudioSegment.from_mp3(tone_file)
            # Lautstärke anpassen
            if "volume_reduction_db" in tone_config:
                tone = tone + tone_config["volume_reduction_db"]
            # Pausen hinzufügen
            return (AudioSegment.silent(duration=tone_config["pause_before"]) +
                    tone +
                    AudioSegment.silent(duration=tone_config["pause_after"]))
        else:
            print(f"Warning: Tone file '{tone_file}' not found. "
                  "Skipping separator tone.")

    # Fallback: 0 ms Stille, falls nichts gefunden
    return AudioSegment.silent(duration=0)


def export_teacher_texts(json_data: str, output_filename: str, client=None):
    """
    Exportiert die Lehrer-Texte ('teacher_speaks' und 'teacher_solution') aller
    Aufgaben in eine Textdatei. Die Texte werden durch ein Semikolon getrennt.
    Erzeugt zusätzlich MP3-Dateien für jede Solution mit UUID als Namen.

    :param json_data: JSON-String mit den Lektionsdaten
    :param output_filename: Pfad zur Ausgabedatei
    :param client: Client für die Sprachsynthese
    """
    if not validate_json_structure(json_data):
        print("Ungültige JSON-Struktur. Export wird abgebrochen.")
        return

    lesson_data = json.loads(json_data)

    # Erstelle tmp_output Verzeichnis falls nötig
    output_dir = "tmp_output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Verzeichnis '{output_dir}' für Solution-Audio-Dateien bereit.")

    with open(output_filename, 'w', encoding='utf-8') as f:
        # Kopfzeile hinzufügen
        f.write("Lehrer-Anweisung;Lehrer-Lösung\n")

        # Über alle Übungen und deren Aufgaben iterieren
        for exercise in lesson_data["lesson"]["exercises"]:
            for task in exercise["tasks"]:
                # Semikolon ersetzen, um CSV-Format nicht zu stören
                teacher_speaks = (
                    task["teacher_speaks"]["text"].replace(";", ","))
                teacher_solution = (
                    task["teacher_solution"]["text"].replace(";", ","))

                # Generiere UUID4 für diese Solution
                # UUID4 verwendet kryptographisch starke Zufallszahlen basierend auf:
                # - System-Entropie (z.B. /dev/urandom)
                # - Aktuelle Zeit und Prozess-ID
                # Kollisionswahrscheinlichkeit: ~1 zu 5,3 × 10³⁶ 
                # (praktisch unmöglich bei normaler Verwendung)
                sound_uuid = str(uuid.uuid4())

                # Erzeuge MP3-Datei für die Solution
                solution_filename = f"{sound_uuid}.mp3"
                solution_path = os.path.join(output_dir, solution_filename)

                # Solution audio generieren (nur wenn Client vorhanden)
                if client:
                    solution_lang = task["teacher_solution"]["language_code"]
                    solution_voice = VOICE_CONFIG.get(
                        solution_lang, "default_voice")
                    solution_segment = generate_speech_segment(
                        client, solution_voice,
                        task["teacher_solution"]["text"])
                    solution_segment = normalize_segment(solution_segment)
                    solution_segment.export(solution_path, format="mp3")
                    print(f"Solution-Audio gespeichert als '{solution_path}'")

                # Anführungszeichen um die Texte herum hinzufügen
                # und Sound-Tag anfügen
                f.write(
                    f"\"{teacher_speaks}\";\"{teacher_solution}\"; "
                    f"[sound:{sound_uuid}.mp3]\n"
                )

    print(f"Lehrer-Texte wurden erfolgreich in "
          f"'{output_filename}' exportiert.")


def generate_lesson_audio(
    json_data: str,
    output_filename: str = "lesson_output.mp3",
    client=None,
    use_compression: bool = False,
    export_texts: str = None  # Neuer Parameter für den Textexport
):
    """
    Liest die Lektionsdaten aus 'json_data', validiert sie und baut eine
    zusammenhängende Audioausgabe zusammen, die als MP3 in 'output_filename'
    gespeichert wird.

    :param json_data: JSON-String mit den Lektionsdaten
    :param output_filename: Pfad zur MP3-Ausgabedatei
    :param client: Client für die Sprachsynthese
    :param use_compression: Ob Audiokompression verwendet werden soll
    :param export_texts: Wenn angegeben,
        werden die Lehrer-Texte in diese Datei exportiert
    """
    # 1) JSON validieren
    if not validate_json_structure(json_data):
        print("Ungültige JSON-Struktur. Audiogenerierung wird abgebrochen.")
        return

    # Wenn der Text-Export angefordert wurde, führe ihn aus
    if export_texts:
        export_teacher_texts(json_data, export_texts, client)
        # Client übergeben

    lesson_data = json.loads(json_data)
    combined_audio = AudioSegment.silent(duration=0)

    # 2) Titel
    title_text = lesson_data["lesson"]["title"]["text"]
    title_lang = lesson_data["lesson"]["title"]["language_code"]
    title_voice = VOICE_CONFIG.get(title_lang, "default_voice")
    title_segment = generate_speech_segment(client, title_voice, title_text)
    combined_audio += title_segment
    # kleine Pause nach dem Titel
    combined_audio += AudioSegment.silent(duration=500)

    # 3) Beschreibung
    description_text = lesson_data["lesson"]["description"]["text"]
    description_lang = lesson_data["lesson"]["description"]["language_code"]
    description_voice = VOICE_CONFIG.get(description_lang, "default_voice")
    description_segment = generate_speech_segment(
        client, description_voice, description_text
    )
    combined_audio += description_segment
    # kleine Pause nach der Beschreibung
    combined_audio += AudioSegment.silent(duration=500)

    # 4) Übungen durchgehen
    for exercise in lesson_data["lesson"]["exercises"]:
        # a) Trennton für Übung
        combined_audio += generate_separator_tone("exercise_tone")

        # b) Erklärungstext
        explanation_text = exercise["explanation"]["text"]
        explanation_lang = exercise["explanation"]["language_code"]
        explanation_voice = VOICE_CONFIG.get(explanation_lang, "default_voice")
        explanation_segment = generate_speech_segment(
            client, explanation_voice, explanation_text)
        combined_audio += explanation_segment
        # kleine Pause nach der Erklärung
        combined_audio += AudioSegment.silent(duration=500)

        # c) Aufgaben durchgehen
        for task in exercise["tasks"]:
            # (i) Trennton für Aufgabe
            combined_audio += generate_separator_tone("task_tone")

            # (ii) Lehrerstimme
            teacher_text = task["teacher_speaks"]["text"]
            teacher_lang = task["teacher_speaks"]["language_code"]
            teacher_voice = VOICE_CONFIG.get(teacher_lang, "default_voice")
            teacher_segment = generate_speech_segment(
                client, teacher_voice, teacher_text)
            combined_audio += teacher_segment

            # (iii) Stille als Wartezeit für Schülerantwort
            combined_audio += AudioSegment.silent(
                duration=task["student_response_time"]
            )

            # (iv) Lehrerlösung
            solution_text = task["teacher_solution"]["text"]
            solution_lang = task["teacher_solution"]["language_code"]
            solution_voice = VOICE_CONFIG.get(solution_lang, "default_voice")
            solution_segment = generate_speech_segment(
                client, solution_voice, solution_text)
            combined_audio += solution_segment

            # (v) Optional: weiterer Separator, falls im JSON gewünscht
            if task["play_separator_tone"]:
                combined_audio += AudioSegment.silent(duration=1000)

    # 5) Alles exportieren
    # *** Füge abschließende Normalisierung des gesamten kombinierten Audios
    # hinzu ***
    combined_audio = normalize_segment(combined_audio, target_dBFS=-20.0)
    # *** Wenn die Komprimierung aktiviert ist, wende sie an ***
    if use_compression:
        print("Applying dynamic range compression...")
        combined_audio = compress_audio_segment(
            combined_audio, threshold=-20.0, ratio=4.0
        )
    else:
        print("Skipping dynamic range compression...")
    combined_audio.export(output_filename, format="mp3")
    print(f"Audio lesson successfully saved as '{output_filename}'.")
