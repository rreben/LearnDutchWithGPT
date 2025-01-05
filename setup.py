# setup.py
import re
from pathlib import Path
from setuptools import setup, find_packages


def get_version():
    """
    Reads the version string from lesson_generator/__init__.py
    and returns it (e.g., '0.1.0').
    """
    init_path = Path(__file__).parent / "lesson_generator" / "__init__.py"
    init_text = init_path.read_text(encoding="utf-8")

    # Look for a line that starts with __version__ = "..."
    version_pattern = r'^__version__ = ["\']([^"\']+)["\']'
    version_match = re.search(version_pattern, init_text, re.MULTILINE)

    if not version_match:
        raise RuntimeError(
            "No __version__ found in lesson_generator/__init__.py"
        )

    return version_match.group(1)


setup(
    name="lesson_generator",  # Package name (adjust as needed)
    version=get_version(),    # Dynamically read from __init__.py
    packages=find_packages(),
    include_package_data=True,
    # Allows including non-Python files via MANIFEST.in or similar
    install_requires=[
        "click>=8.0",
        "pydub>=0.25",
        "python-dotenv>=0.21",
        "elevenlabs>=0.2.18",
        "requests>=2.28",
        # add or adjust as needed
    ],
    entry_points={
        "console_scripts": [
            "lesson-cli = lesson_cli:main",
            # Replace with your actual CLI module and function
        ],
    },
    author="Your Name",
    author_email="you@example.com",
    description=(
        "A tool to generate multilingual audio lessons from JSON content."
    ),
    long_description=(
        Path(__file__).parent / "README.md"
    ).read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    # Adjust to your repo link
    url="https://github.com/youruser/lesson_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
