"""
Orchestrator Module for Autotube.

This module provides central automation control for the complete workflow:
content planning, video generation, metadata assembly, and upload scheduling.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class AutotubeOrchestrator:
    """
    Central orchestrator for the Autotube workflow.

    This class coordinates the entire process of creating and uploading
    ambient sleep sound videos to YouTube, including:
    - Content planning and scheduling
    - Audio processing and mix creation
    - Video generation
    - Metadata generation
    - YouTube upload
    """

    def __init__(
        self,
        input_folder: str = "input_clips",
        output_folder: str = "output_mixes",
        video_folder: str = "output_videos",
        client_secrets_file: str = "client_secrets.json",
    ):
        """
        Initialize the AutotubeOrchestrator.

        Args:
            input_folder: Directory containing input audio clips.
            output_folder: Directory for processed audio mixes.
            video_folder: Directory for generated videos.
            client_secrets_file: Path to YouTube API client secrets.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.video_folder = video_folder
        self.client_secrets_file = client_secrets_file

        # Create necessary directories
        for folder in [input_folder, output_folder, video_folder]:
            os.makedirs(folder, exist_ok=True)

        # Initialize components (lazy loading)
        self._sound_processor = None
        self._video_generator = None
        self._youtube_uploader = None
        self._metadata_generator = None

        logger.info("AutotubeOrchestrator initialized")

    @property
    def sound_processor(self):
        """Lazy-load the SoundProcessor."""
        if self._sound_processor is None:
            from project_name.core.processor import SoundProcessor

            self._sound_processor = SoundProcessor(
                input_folder=self.input_folder,
                output_folder=self.output_folder,
            )
        return self._sound_processor

    @property
    def video_generator(self):
        """Lazy-load the VideoGenerator."""
        if self._video_generator is None:
            from project_name.core.video_generator import VideoGenerator

            self._video_generator = VideoGenerator(output_folder=self.video_folder)
        return self._video_generator

    @property
    def youtube_uploader(self):
        """Lazy-load the YouTubeUploader."""
        if self._youtube_uploader is None:
            from project_name.api.youtube_uploader import YouTubeUploader

            self._youtube_uploader = YouTubeUploader(
                client_secrets_file=self.client_secrets_file
            )
        return self._youtube_uploader

    @property
    def metadata_generator(self):
        """Lazy-load the MetadataGenerator."""
        if self._metadata_generator is None:
            from project_name.core.metadata_generator import MetadataGenerator

            self._metadata_generator = MetadataGenerator()
        return self._metadata_generator

    def create_audio_mix(
        self,
        duration_minutes: int = 60,
        mix_type: str = "sleep",
    ) -> Optional[str]:
        """
        Create an audio mix from available clips.

        Args:
            duration_minutes: Duration of the mix in minutes.
            mix_type: Type of mix ("sleep", "focus", "relax").

        Returns:
            Path to the created mix file, or None if failed.
        """
        logger.info(f"Creating {mix_type} mix ({duration_minutes} minutes)...")

        try:
            # Preprocess any raw audio files
            self.sound_processor.preprocess_audio()

            # Analyze and categorize clips
            self.sound_processor.analyze_clips()

            # Create the mix
            mix_path = self.sound_processor.create_mix(
                target_duration_min=duration_minutes,
                mix_type=mix_type,
            )

            if mix_path and os.path.exists(mix_path):
                logger.info(f"Mix created: {mix_path}")
                return mix_path
            else:
                logger.error("Mix creation failed")
                return None

        except Exception as e:
            logger.error(f"Error creating mix: {e}")
            return None

    def create_video_from_mix(
        self,
        audio_path: str,
        title_text: str = None,
        use_waveform: bool = False,
        background_color: tuple = (25, 25, 35),
    ) -> Optional[str]:
        """
        Create a video from an audio mix.

        Args:
            audio_path: Path to the audio file.
            title_text: Optional text to display on video.
            use_waveform: Whether to create waveform visualization.
            background_color: RGB background color for static video.

        Returns:
            Path to the created video file, or None if failed.
        """
        logger.info(f"Creating video from: {audio_path}")

        try:
            if use_waveform:
                video_path = self.video_generator.generate_video_with_waveform(
                    audio_path=audio_path,
                )
            else:
                video_path = self.video_generator.generate_video_from_audio(
                    audio_path=audio_path,
                    title_text=title_text,
                    background_color=background_color,
                )

            if video_path and os.path.exists(video_path):
                logger.info(f"Video created: {video_path}")
                return video_path
            else:
                logger.error("Video creation failed")
                return None

        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None

    def generate_metadata(
        self,
        sound_type: str,
        duration_hours: int,
        purpose: str = "sleep",
        additional_info: str = "",
    ) -> dict:
        """
        Generate metadata for a video.

        Args:
            sound_type: Type of sound (e.g., "Rain", "Ocean").
            duration_hours: Duration of the video in hours.
            purpose: Purpose ("sleep", "focus", "relax").
            additional_info: Additional description text.

        Returns:
            Dictionary with title, description, and tags.
        """
        return self.metadata_generator.generate_complete_metadata(
            sound_type=sound_type,
            duration_hours=duration_hours,
            purpose=purpose,
            additional_info=additional_info,
        )

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        privacy_status: str = "private",
    ) -> Optional[str]:
        """
        Upload a video to YouTube.

        Args:
            video_path: Path to the video file.
            title: Video title.
            description: Video description.
            tags: List of tags.
            privacy_status: Privacy status ("public", "private", "unlisted").

        Returns:
            YouTube video ID if successful, None otherwise.
        """
        logger.info(f"Uploading video: {title}")

        try:
            video_id = self.youtube_uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
                privacy_status=privacy_status,
            )

            if video_id:
                logger.info(f"Upload successful! Video ID: {video_id}")
                return video_id
            else:
                logger.error("Upload failed")
                return None

        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None

    def run_full_pipeline(
        self,
        sound_type: str = "Rain",
        duration_minutes: int = 60,
        mix_type: str = "sleep",
        privacy_status: str = "private",
        use_waveform: bool = False,
        upload: bool = True,
    ) -> dict:
        """
        Run the complete Autotube pipeline.

        Args:
            sound_type: Type of sound for metadata.
            duration_minutes: Duration of the mix in minutes.
            mix_type: Type of mix ("sleep", "focus", "relax").
            privacy_status: YouTube privacy status.
            use_waveform: Whether to use waveform visualization.
            upload: Whether to upload to YouTube.

        Returns:
            Dictionary with pipeline results.
        """
        results = {
            "success": False,
            "audio_path": None,
            "video_path": None,
            "video_id": None,
            "metadata": None,
            "errors": [],
        }

        logger.info("Starting Autotube pipeline...")

        # Step 1: Create audio mix
        logger.info("Step 1: Creating audio mix...")
        audio_path = self.create_audio_mix(
            duration_minutes=duration_minutes,
            mix_type=mix_type,
        )
        if not audio_path:
            results["errors"].append("Failed to create audio mix")
            return results
        results["audio_path"] = audio_path

        # Step 2: Generate metadata
        logger.info("Step 2: Generating metadata...")
        duration_hours = duration_minutes // 60
        if duration_hours == 0:
            duration_hours = 1
        metadata = self.generate_metadata(
            sound_type=sound_type,
            duration_hours=duration_hours,
            purpose=mix_type,
        )
        results["metadata"] = metadata

        # Step 3: Create video
        logger.info("Step 3: Creating video...")
        video_path = self.create_video_from_mix(
            audio_path=audio_path,
            title_text=metadata["title"] if not use_waveform else None,
            use_waveform=use_waveform,
        )
        if not video_path:
            results["errors"].append("Failed to create video")
            return results
        results["video_path"] = video_path

        # Step 4: Upload to YouTube (optional)
        if upload:
            logger.info("Step 4: Uploading to YouTube...")
            video_id = self.upload_video(
                video_path=video_path,
                title=metadata["title"],
                description=metadata["description"],
                tags=metadata["tags"],
                privacy_status=privacy_status,
            )
            if not video_id:
                results["errors"].append("Failed to upload video")
                return results
            results["video_id"] = video_id

        results["success"] = True
        logger.info("Pipeline completed successfully!")
        return results

    def plan_content(
        self,
        num_videos: int = 7,
        sound_types: list = None,
        purposes: list = None,
        start_date: datetime = None,
    ) -> list:
        """
        Plan content for multiple videos.

        Args:
            num_videos: Number of videos to plan.
            sound_types: List of sound types to use.
            purposes: List of purposes to use.
            start_date: Start date for scheduling.

        Returns:
            List of content plan dictionaries.
        """
        if sound_types is None:
            sound_types = ["Rain", "Ocean", "Nature", "White Noise", "Ambient"]

        if purposes is None:
            purposes = ["sleep", "focus", "relax"]

        if start_date is None:
            start_date = datetime.now()

        content_plan = []

        for i in range(num_videos):
            # Rotate through sound types and purposes
            sound_type = sound_types[i % len(sound_types)]
            purpose = purposes[i % len(purposes)]

            # Schedule videos daily
            publish_date = start_date + timedelta(days=i)

            # Get optimal publish time
            optimal_times = self.metadata_generator.get_optimal_publish_time(purpose)

            plan_item = {
                "video_number": i + 1,
                "sound_type": sound_type,
                "purpose": purpose,
                "scheduled_date": publish_date.strftime("%Y-%m-%d"),
                "optimal_time": optimal_times.get("weekday", "20:00"),
                "duration_hours": 8 if purpose == "sleep" else 2,
                "status": "planned",
            }

            content_plan.append(plan_item)
            logger.info(f"Planned video {i + 1}: {sound_type} {purpose}")

        return content_plan

    def get_status(self) -> dict:
        """
        Get the current status of the orchestrator.

        Returns:
            Dictionary with status information.
        """
        return {
            "input_folder": self.input_folder,
            "output_folder": self.output_folder,
            "video_folder": self.video_folder,
            "input_files": len(os.listdir(self.input_folder))
            if os.path.exists(self.input_folder)
            else 0,
            "output_files": len(os.listdir(self.output_folder))
            if os.path.exists(self.output_folder)
            else 0,
            "video_files": len(os.listdir(self.video_folder))
            if os.path.exists(self.video_folder)
            else 0,
            "components": {
                "sound_processor": self._sound_processor is not None,
                "video_generator": self._video_generator is not None,
                "youtube_uploader": self._youtube_uploader is not None,
                "metadata_generator": self._metadata_generator is not None,
            },
        }
