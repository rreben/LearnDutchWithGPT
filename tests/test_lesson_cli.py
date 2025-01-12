import os
import pytest
from click.testing import CliRunner
from lesson_cli import main


@pytest.fixture
def test_files_path():
    return os.path.join(os.path.dirname(__file__), 'test_files')


def test_lesson_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Generates an MP3 lesson from a JSON file' in result.output
