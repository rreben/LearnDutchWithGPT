# lesson_cli.py
import click
import os
from dotenv import load_dotenv
import sys
from elevenlabs import ElevenLabs
from lesson_generator.audio_generation import generate_lesson_audio


@click.command(help="Generates an MP3 lesson from a JSON file.")
@click.option(
    "--input-file", "-i",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the JSON file containing lesson data."
)
@click.option(
    "--output-file", "-o",
    type=click.Path(dir_okay=False, writable=True),
    default="lesson_output.mp3",
    show_default=True,
    help="Target filename for the generated MP3."
)
@click.option(
    "--export-texts", "-e",
    is_flag=False,
    flag_value="anki_import.txt",
    default=None,
    type=click.Path(dir_okay=False),
    help="Export teacher texts to a separate text file "
         "(format: teacher_speaks;teacher_solution). "
         "Defaults to 'anki_import.txt' if no filename is specified."
)
@click.option(
    "--use-compression", "-c",
    is_flag=True,
    help="Apply dynamic range compression to the audio output"
)
def main(input_file, output_file, export_texts, use_compression):
    """
    Reads lesson data from 'input_file', validates it, and creates
    an audio lesson in MP3 format under 'output_file'.
    Optionally exports teacher texts to a separate file.
    """
    # 1) Lade die .env-Variablen
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    print('apikey:', api_key)
    if not api_key:
        click.echo(
            "ERROR: No ELEVENLABS_API_KEY found."
            "Please set it in your .env file "
            "or environment variables."
        )
        sys.exit(1)  # Abbrechen, wenn kein API-Key vorhanden ist
    else:
        click.echo(f"ELEVENLABS_API_KEY found: {api_key}")

    if not api_key:
        click.echo(
            "ERROR: No ELEVENLABS_API_KEY found."
            "Please set it in your .env file "
            "or environment variables."
        )
        sys.exit(1)  # Abbrechen, wenn kein API-Key vorhanden ist

    # 2) Initialisiere den ElevenLabs-Client
    client = ElevenLabs(api_key=api_key)

    # 3) Lese die JSON-Datei ein
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = f.read()

    # 4) Erzeuge die Audiolesung
    generate_lesson_audio(
        json_data,
        output_filename=output_file,
        client=client,
        use_compression=use_compression,
        export_texts=export_texts
    )

    click.echo(f"Audio lesson successfully saved as '{output_file}'.")
    if export_texts:
        click.echo(f"Teacher texts exported to '{export_texts}'.")


if __name__ == "__main__":
    main()
