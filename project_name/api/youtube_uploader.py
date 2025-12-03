"""
YouTube Upload Module for Autotube.

This module provides functionality to upload videos to YouTube using
the YouTube Data API v3 with OAuth2 authentication.
"""

import http.client
import logging
import os
import random
import time
from typing import Optional

logger = logging.getLogger(__name__)

# Retry configuration for resumable uploads
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


class YouTubeUploader:
    """
    Upload videos to YouTube using the YouTube Data API.

    This class handles OAuth2 authentication and provides methods for
    uploading videos with metadata to YouTube.
    """

    # OAuth2 scopes required for YouTube uploads
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    # Valid privacy statuses
    PRIVACY_STATUSES = ("public", "private", "unlisted")

    # Valid video categories for YouTube
    VIDEO_CATEGORIES = {
        "Film & Animation": "1",
        "Autos & Vehicles": "2",
        "Music": "10",
        "Pets & Animals": "15",
        "Sports": "17",
        "Travel & Events": "19",
        "Gaming": "20",
        "People & Blogs": "22",
        "Comedy": "23",
        "Entertainment": "24",
        "News & Politics": "25",
        "Howto & Style": "26",
        "Education": "27",
        "Science & Technology": "28",
        "Nonprofits & Activism": "29",
    }

    def __init__(
        self,
        client_secrets_file: str = "client_secrets.json",
        credentials_file: str = "youtube_credentials.json",
    ):
        """
        Initialize the YouTubeUploader.

        Args:
            client_secrets_file: Path to OAuth2 client secrets JSON file.
            credentials_file: Path to store/load user credentials.
        """
        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self._youtube_service = None
        self._credentials = None

        logger.info("YouTubeUploader initialized")

    def authenticate(self) -> bool:
        """
        Authenticate with YouTube API using OAuth2.

        Returns:
            True if authentication successful, False otherwise.
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError as e:
            logger.error(
                f"Required libraries not installed: {e}. "
                "Install with: pip install google-api-python-client "
                "google-auth-httplib2 google-auth-oauthlib"
            )
            return False

        try:
            creds = None

            # Load existing credentials if available
            if os.path.exists(self.credentials_file):
                creds = Credentials.from_authorized_user_file(
                    self.credentials_file, self.SCOPES
                )
                logger.info("Loaded existing credentials")

            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    logger.info("Refreshing expired credentials")
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.client_secrets_file):
                        logger.error(
                            f"Client secrets file not found: {self.client_secrets_file}"
                        )
                        return False

                    logger.info("Starting OAuth2 flow for new credentials")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                # Save credentials for future use with secure permissions
                fd = os.open(
                    self.credentials_file,
                    os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                    0o600
                )
                with os.fdopen(fd, "w") as token_file:
                    token_file.write(creds.to_json())
                logger.info(f"Credentials saved to {self.credentials_file}")

            self._credentials = creds
            self._youtube_service = build("youtube", "v3", credentials=creds)
            logger.info("YouTube API authentication successful")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        category: str = "Entertainment",
        privacy_status: str = "private",
        notify_subscribers: bool = True,
    ) -> Optional[str]:
        """
        Upload a video to YouTube.

        Args:
            video_path: Path to the video file to upload.
            title: Video title (max 100 characters).
            description: Video description (max 5000 characters).
            tags: List of tags for the video.
            category: Video category name.
            privacy_status: One of 'public', 'private', 'unlisted'.
            notify_subscribers: Whether to notify channel subscribers.

        Returns:
            YouTube video ID if successful, None otherwise.
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None

        if privacy_status not in self.PRIVACY_STATUSES:
            logger.error(f"Invalid privacy status: {privacy_status}")
            return None

        # Authenticate if not already done
        if not self._youtube_service:
            if not self.authenticate():
                return None

        try:
            from googleapiclient.http import MediaFileUpload
        except ImportError as e:
            logger.error(f"Required library not installed: {e}")
            return None

        # Get category ID (defaults to Entertainment if not found)
        category_id = self.VIDEO_CATEGORIES.get(category, "24")

        # Prepare video metadata
        body = {
            "snippet": {
                "title": title[:100],  # YouTube limit
                "description": description[:5000],  # YouTube limit
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
                "notifySubscribers": notify_subscribers,
            },
        }

        # Prepare media file for upload
        media = MediaFileUpload(
            video_path,
            mimetype="video/*",
            resumable=True,
            chunksize=1024 * 1024,  # 1MB chunks
        )

        try:
            # Create upload request
            request = self._youtube_service.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )

            # Execute resumable upload with retry logic
            video_id = self._resumable_upload(request)

            if video_id:
                logger.info(f"Video uploaded successfully! ID: {video_id}")
                logger.info(f"Video URL: https://www.youtube.com/watch?v={video_id}")
                return video_id
            return None

        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return None

    def _resumable_upload(self, request) -> Optional[str]:
        """
        Execute a resumable upload with retry logic.

        Args:
            request: YouTube API upload request object.

        Returns:
            Video ID if successful, None otherwise.
        """
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                logger.info("Uploading video...")
                status, response = request.next_chunk()

                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")

            except http.client.HTTPException as e:
                error = f"HTTP error: {e}"
                logger.warning(error)

            except Exception as e:
                from googleapiclient.errors import HttpError

                if isinstance(e, HttpError):
                    if e.resp.status in RETRIABLE_STATUS_CODES:
                        error = f"Retriable HTTP error {e.resp.status}: {e.content}"
                        logger.warning(error)
                    else:
                        raise
                else:
                    raise

            if error is not None:
                retry += 1
                if retry > MAX_RETRIES:
                    logger.error(f"Max retries exceeded: {error}")
                    return None

                # Exponential backoff with jitter, capped at 60 seconds
                sleep_time = min(random.random() * (2**retry), 60)
                logger.info(f"Retry {retry}/{MAX_RETRIES} in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                error = None

        if response:
            return response.get("id")
        return None

    def update_video_metadata(
        self,
        video_id: str,
        title: str = None,
        description: str = None,
        tags: list = None,
    ) -> bool:
        """
        Update metadata for an existing video.

        Args:
            video_id: YouTube video ID.
            title: New title (optional).
            description: New description (optional).
            tags: New tags list (optional).

        Returns:
            True if update successful, False otherwise.
        """
        if not self._youtube_service:
            if not self.authenticate():
                return False

        try:
            # First, get current video details
            video_response = (
                self._youtube_service.videos()
                .list(part="snippet", id=video_id)
                .execute()
            )

            if not video_response.get("items"):
                logger.error(f"Video not found: {video_id}")
                return False

            snippet = video_response["items"][0]["snippet"]

            # Update only provided fields
            if title:
                snippet["title"] = title[:100]
            if description:
                snippet["description"] = description[:5000]
            if tags:
                snippet["tags"] = tags

            # Execute update
            self._youtube_service.videos().update(
                part="snippet",
                body={
                    "id": video_id,
                    "snippet": snippet,
                },
            ).execute()

            logger.info(f"Video metadata updated: {video_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update video metadata: {e}")
            return False

    def get_video_status(self, video_id: str) -> Optional[dict]:
        """
        Get the processing status of an uploaded video.

        Args:
            video_id: YouTube video ID.

        Returns:
            Dictionary with video status information, or None if failed.
        """
        if not self._youtube_service:
            if not self.authenticate():
                return None

        try:
            response = (
                self._youtube_service.videos()
                .list(part="status,processingDetails", id=video_id)
                .execute()
            )

            if not response.get("items"):
                logger.error(f"Video not found: {video_id}")
                return None

            item = response["items"][0]
            return {
                "privacy_status": item.get("status", {}).get("privacyStatus"),
                "upload_status": item.get("status", {}).get("uploadStatus"),
                "processing_status": item.get("processingDetails", {}).get(
                    "processingStatus"
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get video status: {e}")
            return None

    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video from YouTube.

        Args:
            video_id: YouTube video ID to delete.

        Returns:
            True if deletion successful, False otherwise.
        """
        if not self._youtube_service:
            if not self.authenticate():
                return False

        try:
            self._youtube_service.videos().delete(id=video_id).execute()
            logger.info(f"Video deleted: {video_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete video: {e}")
            return False
