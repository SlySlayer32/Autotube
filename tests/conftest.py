"""Common test configuration and fixtures."""

import tempfile
from pathlib import Path
from typing import Dict, Generator

import pytest
from pydub import AudioSegment  # Added for creating mock audio

# Explicitly set the path to ffmpeg for pydub
AudioSegment.converter = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_audio_file(test_data_dir: Path) -> Path:
    """Create a mock audio file for testing."""
    audio_path = test_data_dir / "mock_audio.wav"
    if not audio_path.parent.exists():
        audio_path.parent.mkdir(parents=True)
    if not audio_path.exists():
        # Create a short, silent WAV file for testing
        silent_segment = AudioSegment.silent(duration=100)  # 100ms silent audio
        silent_segment.export(audio_path, format="wav")
    return audio_path


@pytest.fixture
def mock_user_profile() -> Dict:
    """Return a mock user profile for testing."""
    return {
        "name": "test_user",
        "sleep_issue": "insomnia",
        "category_weights": {
            "rain": 0.7,
            "thunder": 0.3,
            "white_noise": 0.5,
            "nature": 0.6,
            "water": 0.8,
        },
        "eq_preferences": {
            "low": 2,
            "mid-low": 0,
            "mid": -1,
            "high-mid": -2,
            "high": -3,
        },
        "volume_preferences": {"base_sounds": 0, "occasional_sounds": -3},
    }


@pytest.fixture
def mock_mix_params() -> Dict:
    """Return mock mix parameters for testing."""
    return {
        "mix_type": "sleep",
        "duration_minutes": 60,
        "crossfade": 5000,
        "fade_in": 10000,
        "fade_out": 10000,
        "category_weights": {"rain": 0.7, "thunder": 0.3, "white_noise": 0.5},
        "volume_adjustments": {"rain": 0, "thunder": -6, "white_noise": -3},
    }
