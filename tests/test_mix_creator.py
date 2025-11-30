"""Tests for mix creation functionality."""

import os
from pathlib import Path
from typing import Dict

import pytest
from pydub import AudioSegment

from project_name.core.mix_creator import MixCreator


@pytest.mark.unit
class TestMixCreator:
    @pytest.fixture
    def mix_creator(self, temp_dir: Path) -> MixCreator:
        """Create a MixCreator instance for testing."""
        return MixCreator(output_folder=str(temp_dir))

    def test_init(self, mix_creator: MixCreator, temp_dir: Path):
        """Test MixCreator initialization."""
        assert mix_creator.output_folder == str(temp_dir)
        assert os.path.exists(temp_dir)
        assert len(mix_creator.mix_profiles) > 0
        assert "sleep" in mix_creator.mix_profiles
        assert "focus" in mix_creator.mix_profiles

    def test_create_mix_basic(self, mix_creator: MixCreator, mock_audio_file: Path):
        """Test basic mix creation."""
        audio_files = {
            "rain": [str(mock_audio_file)],
            "white_noise": [str(mock_audio_file)],
        }

        output_path = mix_creator.create_mix(
            audio_files=audio_files,
            mix_type="sleep",
            duration_minutes=1,
            output_format="mp3",
            bitrate="192k",
        )

        assert output_path is not None
        assert os.path.exists(output_path)
        assert output_path.endswith(".mp3")

        # Verify mix duration
        audio = AudioSegment.from_file(output_path)
        assert abs(len(audio) - 60000) < 1000  # Within 1 second of target duration

    def test_create_mix_with_profile(
        self, mix_creator: MixCreator, mock_audio_file: Path, mock_mix_params: Dict
    ):
        """Test mix creation with specific profile parameters."""
        audio_files = {
            "rain": [str(mock_audio_file)],
            "thunder": [str(mock_audio_file)],
            "white_noise": [str(mock_audio_file)],
        }

        output_path = mix_creator.create_mix(
            audio_files=audio_files,
            mix_type=mock_mix_params["mix_type"],
            duration_minutes=mock_mix_params["duration_minutes"],
        )

        assert output_path is not None
        assert os.path.exists(output_path)

        # Verify mix duration
        audio = AudioSegment.from_file(output_path)
        expected_duration = mock_mix_params["duration_minutes"] * 60 * 1000
        assert abs(len(audio) - expected_duration) < 1000

    @pytest.mark.parametrize(
        "mix_type,duration", [("sleep", 30), ("focus", 45), ("relax", 60)]
    )
    def test_create_mix_variations(
        self,
        mix_creator: MixCreator,
        mock_audio_file: Path,
        mix_type: str,
        duration: int,
    ):
        """Test mix creation with different types and durations."""
        audio_files = {"rain": [str(mock_audio_file)], "nature": [str(mock_audio_file)]}

        output_path = mix_creator.create_mix(
            audio_files=audio_files, mix_type=mix_type, duration_minutes=duration
        )

        assert output_path is not None
        assert os.path.exists(output_path)

        # Verify mix duration
        audio = AudioSegment.from_file(output_path)
        expected_duration = duration * 60 * 1000
        assert abs(len(audio) - expected_duration) < 1000

    def test_create_category_mix(self, mix_creator: MixCreator, mock_audio_file: Path):
        """Test creation of category-specific submixes."""
        files = [str(mock_audio_file)] * 3  # Multiple files for same category
        target_duration = 60 * 1000  # 1 minute in milliseconds
        crossfade = 5000  # 5 seconds

        mix = mix_creator._create_category_mix(files, target_duration, crossfade)

        assert isinstance(mix, AudioSegment)
        assert (
            abs(len(mix) - target_duration) < crossfade
        )  # Allow small variation due to crossfade

    def test_apply_mix_effects(self, mix_creator: MixCreator, mock_audio_file: Path):
        """Test applying effects to mix."""
        # Create a base mix first
        audio = AudioSegment.from_file(str(mock_audio_file))

        # Test with sleep profile
        profile = mix_creator.mix_profiles["sleep"]
        processed = mix_creator._apply_mix_effects(audio, profile)

        assert isinstance(processed, AudioSegment)
        assert len(processed) == len(audio)  # Effects shouldn't change duration

    def test_preview_mix(self, mix_creator: MixCreator, mock_audio_file: Path):
        """Test mix preview generation."""
        audio_files = {
            "rain": [str(mock_audio_file)],
            "thunder": [str(mock_audio_file)],
        }

        preview = mix_creator.preview_mix(
            audio_files=audio_files, mix_type="sleep", preview_duration=30
        )

        assert isinstance(preview, AudioSegment)
        assert abs(len(preview) - 30000) < 1000  # Should be close to 30 seconds

    def test_save_preview(
        self, mix_creator: MixCreator, mock_audio_file: Path, temp_dir: Path
    ):
        """Test saving mix preview."""
        # Create a preview first
        audio_files = {"rain": [str(mock_audio_file)]}
        preview = mix_creator.preview_mix(audio_files, "sleep", 30)

        output_path = os.path.join(temp_dir, "preview.mp3")
        success = mix_creator.save_preview(
            preview=preview, output_path=output_path, format="mp3", bitrate="128k"
        )

        assert success
        assert os.path.exists(output_path)
        saved_audio = AudioSegment.from_file(output_path)
        assert abs(len(saved_audio) - 30000) < 1000  # Should be close to 30 seconds
