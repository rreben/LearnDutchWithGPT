import os
import pytest
from click.testing import CliRunner
from lesson_cli import main
import tempfile


@pytest.fixture
def test_files_path():
    return os.path.join(os.path.dirname(__file__), 'testfiles')


def test_lesson_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Generates an MP3 lesson from a JSON file' in result.output


def test_lesson_cli_work(test_files_path):
    runner = CliRunner()
    result = runner.invoke(
            main, [
                '-i', os.path.join(test_files_path, 'gekuerzte_lesson.json'),
                '-o', 'test.mp3'
            ]
        )
    assert 'Heb je mijn boek al gelezen?' in result.output


def test_text_export_option(test_files_path):
    runner = CliRunner()

    # Temporäre Datei für den Textexport erstellen
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # CLI mit Export-Option aufrufen
        result = runner.invoke(
            main, [
                '-i', os.path.join(test_files_path, 'gekuerzte_lesson.json'),
                '-o', 'test.mp3',
                '-e', temp_path
            ]
        )

        # Prüfen, ob der Befehl erfolgreich war
        assert result.exit_code == 0
        assert f"Teacher texts exported to '{temp_path}'" in result.output

        # Prüfen, ob die Datei existiert und Inhalte hat
        assert os.path.exists(temp_path)

        # Inhalt der Datei prüfen
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Überprüfung der Kopfzeile
        assert "Lehrer-Anweisung;Lehrer-Lösung" in content
        # Mindestens eine Zeile mit Anweisung und Lösung sollte vorhanden sein
        assert any(";" in line for line in content.splitlines()[1:])

    finally:
        # Temporäre Datei aufräumen
        if os.path.exists(temp_path):
            os.unlink(temp_path)
