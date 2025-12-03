"""Tests for the VideoGenerator module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestVideoGenerator:
    """Test cases for VideoGenerator class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def mock_audio_file(self, temp_dir):
        """Create a mock audio file for testing."""
        from pydub import AudioSegment

        audio_path = temp_dir / "test_audio.wav"
        # Create a short silent audio file
        silent = AudioSegment.silent(duration=1000)  # 1 second
        silent.export(audio_path, format="wav")
        return str(audio_path)

    @pytest.fixture
    def video_generator(self, temp_dir):
        """Create a VideoGenerator instance for testing."""
        with patch("subprocess.run") as mock_run:
            # Mock ffmpeg version check
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="ffmpeg version 4.0",
            )
            from project_name.core.video_generator import VideoGenerator

            return VideoGenerator(output_folder=str(temp_dir))

    def test_init(self, video_generator, temp_dir):
        """Test VideoGenerator initialization."""
        assert video_generator.output_folder == str(temp_dir)
        assert video_generator.resolution == (1920, 1080)
        assert video_generator.fps == 30

    def test_init_custom_settings(self, temp_dir):
        """Test VideoGenerator with custom settings."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="ffmpeg version")
            from project_name.core.video_generator import VideoGenerator

            generator = VideoGenerator(
                output_folder=str(temp_dir),
                resolution=(1280, 720),
                fps=24,
            )
            assert generator.resolution == (1280, 720)
            assert generator.fps == 24

    def test_create_background_image(self, video_generator, temp_dir):
        """Test background image creation."""
        image_path = video_generator.create_background_image(
            color=(100, 100, 100),
            output_path=str(temp_dir / "bg.png"),
        )
        assert os.path.exists(image_path)
        assert image_path.endswith(".png")

    def test_create_background_with_text(self, video_generator, temp_dir):
        """Test background image creation with text overlay."""
        image_path = video_generator.create_background_image(
            color=(50, 50, 50),
            text="Test Title",
            output_path=str(temp_dir / "bg_text.png"),
        )
        assert os.path.exists(image_path)

    @patch("subprocess.run")
    def test_generate_video_from_audio(
        self, mock_run, video_generator, mock_audio_file, temp_dir
    ):
        """Test video generation from audio file."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        # The video won't actually be created, but we test the flow
        result = video_generator.generate_video_from_audio(
            audio_path=mock_audio_file,
            output_filename="test_video.mp4",
        )

        # Verify ffmpeg was called
        assert mock_run.called
        call_args = mock_run.call_args[0][0]
        assert "ffmpeg" in call_args
        # With mocked subprocess, the video is generated successfully
        assert result is not None

    def test_generate_video_missing_audio(self, video_generator):
        """Test video generation with missing audio file."""
        result = video_generator.generate_video_from_audio(
            audio_path="/nonexistent/audio.mp3"
        )
        assert result is None

    @patch("subprocess.run")
    def test_get_video_info(self, mock_run, video_generator, temp_dir):
        """Test getting video information."""
        # Create a mock video file
        video_path = temp_dir / "test.mp4"
        video_path.touch()

        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"format": {"duration": "10.0", "size": "1000"}, "streams": []}',
        )

        info = video_generator.get_video_info(str(video_path))
        assert info is not None
        assert "duration" in info


class TestVideoGeneratorFFmpegCheck:
    """Test FFmpeg verification."""

    def test_ffmpeg_not_found(self):
        """Test behavior when FFmpeg is not available."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("ffmpeg not found")

            with pytest.raises(RuntimeError) as exc_info:
                from project_name.core.video_generator import VideoGenerator

                VideoGenerator()

            assert "FFmpeg" in str(exc_info.value)
