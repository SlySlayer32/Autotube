"""Tests for the YouTubeUploader module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestYouTubeUploader:
    """Test cases for YouTubeUploader class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def uploader(self, temp_dir):
        """Create a YouTubeUploader instance for testing."""
        from project_name.api.youtube_uploader import YouTubeUploader

        return YouTubeUploader(
            client_secrets_file=str(temp_dir / "client_secrets.json"),
            credentials_file=str(temp_dir / "credentials.json"),
        )

    def test_init(self, uploader, temp_dir):
        """Test YouTubeUploader initialization."""
        assert "client_secrets.json" in uploader.client_secrets_file
        assert "credentials.json" in uploader.credentials_file
        assert uploader._youtube_service is None

    def test_valid_privacy_statuses(self, uploader):
        """Test that valid privacy statuses are defined."""
        assert "public" in uploader.PRIVACY_STATUSES
        assert "private" in uploader.PRIVACY_STATUSES
        assert "unlisted" in uploader.PRIVACY_STATUSES

    def test_video_categories(self, uploader):
        """Test that video categories are defined."""
        assert len(uploader.VIDEO_CATEGORIES) > 0
        assert "Entertainment" in uploader.VIDEO_CATEGORIES
        assert "Music" in uploader.VIDEO_CATEGORIES

    def test_scopes(self, uploader):
        """Test that required OAuth scopes are defined."""
        assert len(uploader.SCOPES) > 0
        assert "youtube.upload" in uploader.SCOPES[0]

    def test_upload_video_missing_file(self, uploader):
        """Test upload fails gracefully with missing video file."""
        result = uploader.upload_video(
            video_path="/nonexistent/video.mp4",
            title="Test Video",
            description="Test Description",
        )
        assert result is None

    def test_upload_video_invalid_privacy(self, uploader, temp_dir):
        """Test upload fails with invalid privacy status."""
        # Create a mock video file
        video_path = temp_dir / "test.mp4"
        video_path.touch()

        result = uploader.upload_video(
            video_path=str(video_path),
            title="Test Video",
            description="Test Description",
            privacy_status="invalid_status",
        )
        assert result is None

    @patch("project_name.api.youtube_uploader.YouTubeUploader.authenticate")
    def test_upload_video_auth_failure(self, mock_auth, uploader, temp_dir):
        """Test upload fails when authentication fails."""
        mock_auth.return_value = False

        video_path = temp_dir / "test.mp4"
        video_path.touch()

        result = uploader.upload_video(
            video_path=str(video_path),
            title="Test Video",
            description="Test Description",
        )
        assert result is None

    def test_authenticate_missing_secrets(self, uploader):
        """Test authentication fails with missing client secrets."""
        result = uploader.authenticate()
        assert result is False


class TestYouTubeUploaderMocked:
    """Test YouTubeUploader with mocked Google API."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def mock_uploader(self, temp_dir):
        """Create a mocked YouTubeUploader."""
        from project_name.api.youtube_uploader import YouTubeUploader

        uploader = YouTubeUploader(
            client_secrets_file=str(temp_dir / "secrets.json"),
            credentials_file=str(temp_dir / "creds.json"),
        )

        # Mock the YouTube service
        uploader._youtube_service = MagicMock()
        uploader._credentials = MagicMock()

        return uploader

    def test_get_video_status(self, mock_uploader):
        """Test getting video status with mocked service."""
        mock_uploader._youtube_service.videos().list().execute.return_value = {
            "items": [
                {
                    "status": {"privacyStatus": "private", "uploadStatus": "processed"},
                    "processingDetails": {"processingStatus": "succeeded"},
                }
            ]
        }

        status = mock_uploader.get_video_status("test_video_id")
        assert status is not None
        assert status["privacy_status"] == "private"

    def test_get_video_status_not_found(self, mock_uploader):
        """Test getting status for non-existent video."""
        mock_uploader._youtube_service.videos().list().execute.return_value = {
            "items": []
        }

        status = mock_uploader.get_video_status("nonexistent_id")
        assert status is None

    def test_delete_video(self, mock_uploader):
        """Test deleting a video."""
        mock_uploader._youtube_service.videos().delete().execute.return_value = None

        result = mock_uploader.delete_video("test_video_id")
        assert result is True

    def test_update_video_metadata(self, mock_uploader):
        """Test updating video metadata."""
        mock_uploader._youtube_service.videos().list().execute.return_value = {
            "items": [
                {
                    "snippet": {
                        "title": "Old Title",
                        "description": "Old Description",
                        "categoryId": "24",
                    }
                }
            ]
        }

        result = mock_uploader.update_video_metadata(
            video_id="test_id",
            title="New Title",
            description="New Description",
        )
        assert result is True
