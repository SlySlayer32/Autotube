"""Tests for the AutotubeOrchestrator module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestAutotubeOrchestrator:
    """Test cases for AutotubeOrchestrator class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def orchestrator(self, temp_dir):
        """Create an AutotubeOrchestrator instance for testing."""
        from project_name.core.orchestrator import AutotubeOrchestrator

        return AutotubeOrchestrator(
            input_folder=str(temp_dir / "input"),
            output_folder=str(temp_dir / "output"),
            video_folder=str(temp_dir / "videos"),
        )

    def test_init(self, orchestrator, temp_dir):
        """Test AutotubeOrchestrator initialization."""
        assert orchestrator.input_folder == str(temp_dir / "input")
        assert orchestrator.output_folder == str(temp_dir / "output")
        assert orchestrator.video_folder == str(temp_dir / "videos")
        assert orchestrator._sound_processor is None
        assert orchestrator._video_generator is None
        assert orchestrator._youtube_uploader is None
        assert orchestrator._metadata_generator is None

    def test_directories_created(self, orchestrator, temp_dir):
        """Test that directories are created on init."""
        assert os.path.exists(temp_dir / "input")
        assert os.path.exists(temp_dir / "output")
        assert os.path.exists(temp_dir / "videos")

    def test_lazy_loading_metadata_generator(self, orchestrator):
        """Test lazy loading of metadata generator."""
        assert orchestrator._metadata_generator is None
        generator = orchestrator.metadata_generator
        assert generator is not None
        assert orchestrator._metadata_generator is not None

    def test_generate_metadata(self, orchestrator):
        """Test metadata generation via orchestrator."""
        metadata = orchestrator.generate_metadata(
            sound_type="Rain",
            duration_hours=8,
            purpose="sleep",
        )
        assert "title" in metadata
        assert "description" in metadata
        assert "tags" in metadata

    def test_get_status(self, orchestrator):
        """Test status reporting."""
        status = orchestrator.get_status()
        assert "input_folder" in status
        assert "output_folder" in status
        assert "video_folder" in status
        assert "input_files" in status
        assert "components" in status

    def test_plan_content_default(self, orchestrator):
        """Test content planning with defaults."""
        plan = orchestrator.plan_content(num_videos=3)
        assert len(plan) == 3
        for item in plan:
            assert "video_number" in item
            assert "sound_type" in item
            assert "purpose" in item
            assert "scheduled_date" in item

    def test_plan_content_custom_types(self, orchestrator):
        """Test content planning with custom sound types."""
        plan = orchestrator.plan_content(
            num_videos=2,
            sound_types=["Rain", "Ocean"],
            purposes=["sleep"],
        )
        assert len(plan) == 2
        assert plan[0]["sound_type"] == "Rain"
        assert plan[1]["sound_type"] == "Ocean"

    def test_plan_content_rotation(self, orchestrator):
        """Test that sound types and purposes rotate correctly."""
        plan = orchestrator.plan_content(
            num_videos=6,
            sound_types=["A", "B"],
            purposes=["x", "y", "z"],
        )
        assert plan[0]["sound_type"] == "A"
        assert plan[1]["sound_type"] == "B"
        assert plan[2]["sound_type"] == "A"
        assert plan[0]["purpose"] == "x"
        assert plan[1]["purpose"] == "y"
        assert plan[2]["purpose"] == "z"


class TestAutotubeOrchestratorMocked:
    """Test AutotubeOrchestrator with mocked components."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def mock_orchestrator(self, temp_dir):
        """Create an orchestrator with mocked components."""
        from project_name.core.orchestrator import AutotubeOrchestrator

        orchestrator = AutotubeOrchestrator(
            input_folder=str(temp_dir / "input"),
            output_folder=str(temp_dir / "output"),
            video_folder=str(temp_dir / "videos"),
        )

        # Mock components
        orchestrator._sound_processor = MagicMock()
        orchestrator._video_generator = MagicMock()
        orchestrator._youtube_uploader = MagicMock()

        return orchestrator

    def test_create_audio_mix_success(self, mock_orchestrator, temp_dir):
        """Test successful audio mix creation."""
        # Setup mock
        mix_path = str(temp_dir / "output" / "test_mix.mp3")
        mock_orchestrator._sound_processor.create_mix.return_value = mix_path

        # Create a dummy file for the path
        Path(mix_path).parent.mkdir(parents=True, exist_ok=True)
        Path(mix_path).touch()

        result = mock_orchestrator.create_audio_mix(
            duration_minutes=60,
            mix_type="sleep",
        )

        assert result == mix_path
        mock_orchestrator._sound_processor.preprocess_audio.assert_called_once()
        mock_orchestrator._sound_processor.analyze_clips.assert_called_once()

    def test_create_audio_mix_failure(self, mock_orchestrator):
        """Test audio mix creation failure."""
        mock_orchestrator._sound_processor.create_mix.return_value = None

        result = mock_orchestrator.create_audio_mix(
            duration_minutes=60,
            mix_type="sleep",
        )

        assert result is None

    @patch("os.path.exists")
    def test_create_video_from_mix_success(
        self, mock_exists, mock_orchestrator, temp_dir
    ):
        """Test successful video creation."""
        mock_exists.return_value = True
        video_path = str(temp_dir / "videos" / "test.mp4")
        mock_orchestrator._video_generator.generate_video_from_audio.return_value = (
            video_path
        )

        result = mock_orchestrator.create_video_from_mix(
            audio_path=str(temp_dir / "audio.mp3"),
            title_text="Test",
        )

        assert result == video_path

    @patch("os.path.exists")
    def test_create_video_with_waveform(
        self, mock_exists, mock_orchestrator, temp_dir
    ):
        """Test video creation with waveform."""
        mock_exists.return_value = True
        video_path = str(temp_dir / "videos" / "test_waveform.mp4")
        mock_orchestrator._video_generator.generate_video_with_waveform.return_value = (
            video_path
        )

        result = mock_orchestrator.create_video_from_mix(
            audio_path=str(temp_dir / "audio.mp3"),
            use_waveform=True,
        )

        assert result == video_path
        mock_orchestrator._video_generator.generate_video_with_waveform.assert_called()

    def test_upload_video_success(self, mock_orchestrator, temp_dir):
        """Test successful video upload."""
        mock_orchestrator._youtube_uploader.upload_video.return_value = "abc123"

        result = mock_orchestrator.upload_video(
            video_path=str(temp_dir / "test.mp4"),
            title="Test Video",
            description="Test Description",
            tags=["test"],
        )

        assert result == "abc123"

    def test_upload_video_failure(self, mock_orchestrator, temp_dir):
        """Test video upload failure."""
        mock_orchestrator._youtube_uploader.upload_video.return_value = None

        result = mock_orchestrator.upload_video(
            video_path=str(temp_dir / "test.mp4"),
            title="Test Video",
            description="Test Description",
        )

        assert result is None


class TestAutotubeOrchestratorPipeline:
    """Test the full pipeline functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    def test_run_full_pipeline_no_upload(self, temp_dir):
        """Test pipeline without upload."""
        from project_name.core.orchestrator import AutotubeOrchestrator

        orchestrator = AutotubeOrchestrator(
            input_folder=str(temp_dir / "input"),
            output_folder=str(temp_dir / "output"),
            video_folder=str(temp_dir / "videos"),
        )

        # Mock the internal components
        orchestrator._sound_processor = MagicMock()
        orchestrator._video_generator = MagicMock()

        # Setup returns
        audio_path = str(temp_dir / "output" / "mix.mp3")
        video_path = str(temp_dir / "videos" / "video.mp4")

        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        Path(audio_path).touch()
        Path(video_path).parent.mkdir(parents=True, exist_ok=True)
        Path(video_path).touch()

        orchestrator._sound_processor.create_mix.return_value = audio_path
        orchestrator._video_generator.generate_video_from_audio.return_value = (
            video_path
        )

        results = orchestrator.run_full_pipeline(
            sound_type="Rain",
            duration_minutes=60,
            mix_type="sleep",
            upload=False,
        )

        assert results["audio_path"] == audio_path
        assert results["video_path"] == video_path
        assert results["video_id"] is None  # No upload
        assert results["metadata"] is not None
