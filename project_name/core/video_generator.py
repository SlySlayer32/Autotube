"""
Video Generator Module for Autotube.

This module provides functionality to generate static or animated videos
from audio files using FFmpeg and Pydub.
"""

import logging
import os
import subprocess
import tempfile
from typing import Optional

from PIL import Image
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class VideoGenerator:
    """
    Generate videos from audio files with static or animated backgrounds.

    This class uses FFmpeg to combine audio with images or animations
    to create videos suitable for YouTube upload.
    """

    # Default video settings
    DEFAULT_RESOLUTION = (1920, 1080)
    DEFAULT_FPS = 30
    DEFAULT_VIDEO_CODEC = "libx264"
    DEFAULT_AUDIO_CODEC = "aac"
    DEFAULT_CRF = 23  # Constant Rate Factor for quality (lower = better)

    def __init__(
        self,
        output_folder: str = "output_videos",
        resolution: tuple = None,
        fps: int = None,
    ):
        """
        Initialize the VideoGenerator.

        Args:
            output_folder: Directory to save generated videos.
            resolution: Video resolution as (width, height) tuple.
            fps: Frames per second for the output video.
        """
        self.output_folder = output_folder
        self.resolution = resolution or self.DEFAULT_RESOLUTION
        self.fps = fps or self.DEFAULT_FPS

        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Verify FFmpeg is available
        self._verify_ffmpeg()

        logger.info(
            f"VideoGenerator initialized: resolution={self.resolution}, fps={self.fps}"
        )

    def _verify_ffmpeg(self) -> bool:
        """
        Verify that FFmpeg is available on the system.

        Returns:
            True if FFmpeg is available, raises RuntimeError otherwise.
        """
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            first_line = result.stdout.split("\n")[0]
            logger.debug(f"FFmpeg found: {first_line}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"FFmpeg not found or not working: {e}")
            raise RuntimeError(
                "FFmpeg is required but not found. Please install FFmpeg."
            ) from e

    def create_background_image(
        self,
        color: tuple = (25, 25, 35),
        text: str = None,
        output_path: str = None,
    ) -> str:
        """
        Create a simple background image for the video.

        Args:
            color: RGB tuple for background color.
            text: Optional text to overlay on the image.
            output_path: Path to save the image.

        Returns:
            Path to the created image.
        """
        width, height = self.resolution

        # Create image with solid color
        image = Image.new("RGB", (width, height), color)

        # Optionally add text
        if text:
            try:
                from PIL import ImageDraw, ImageFont

                draw = ImageDraw.Draw(image)
                # Try to use a nice font, fallback to default
                try:
                    font = ImageFont.truetype("arial.ttf", 72)
                except OSError:
                    font = ImageFont.load_default()

                # Center the text
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                draw.text((x, y), text, fill=(255, 255, 255), font=font)
            except ImportError:
                logger.warning("PIL drawing not available, skipping text overlay")

        # Save image
        if output_path is None:
            output_path = os.path.join(self.output_folder, "background.png")

        image.save(output_path, "PNG")
        logger.info(f"Created background image: {output_path}")
        return output_path

    def generate_video_from_audio(
        self,
        audio_path: str,
        background_path: str = None,
        output_filename: str = None,
        background_color: tuple = (25, 25, 35),
        title_text: str = None,
    ) -> Optional[str]:
        """
        Generate a video from an audio file with a static background.

        Args:
            audio_path: Path to the input audio file.
            background_path: Path to background image. If None, creates one.
            output_filename: Name for the output video file.
            background_color: RGB color for auto-generated background.
            title_text: Optional text to display on auto-generated background.

        Returns:
            Path to the generated video, or None if generation failed.
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None

        # Get audio duration
        try:
            audio = AudioSegment.from_file(audio_path)
            duration_seconds = len(audio) / 1000.0
            logger.info(f"Audio duration: {duration_seconds:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to read audio file: {e}")
            return None

        # Create or use background image
        temp_bg = None
        if background_path is None or not os.path.exists(background_path):
            with tempfile.NamedTemporaryFile(
                suffix=".png", delete=False
            ) as tmp:
                temp_bg = tmp.name
            background_path = self.create_background_image(
                color=background_color,
                text=title_text,
                output_path=temp_bg,
            )

        # Generate output filename
        if output_filename is None:
            audio_basename = os.path.splitext(os.path.basename(audio_path))[0]
            output_filename = f"{audio_basename}_video.mp4"

        output_path = os.path.join(self.output_folder, output_filename)

        try:
            # Build FFmpeg command
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite output
                "-loop", "1",  # Loop the image
                "-i", background_path,
                "-i", audio_path,
                "-c:v", self.DEFAULT_VIDEO_CODEC,
                "-tune", "stillimage",
                "-c:a", self.DEFAULT_AUDIO_CODEC,
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",  # End when audio ends
                "-r", str(self.fps),
                "-crf", str(self.DEFAULT_CRF),
                output_path,
            ]

            logger.info(f"Running FFmpeg: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None

            logger.info(f"Video generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            return None
        finally:
            # Clean up temporary background image
            if temp_bg and os.path.exists(temp_bg):
                os.remove(temp_bg)

    def generate_video_with_waveform(
        self,
        audio_path: str,
        output_filename: str = None,
        background_color: str = "0x191923",
        waveform_color: str = "0x4a90d9",
    ) -> Optional[str]:
        """
        Generate a video with an animated audio waveform visualization.

        Args:
            audio_path: Path to the input audio file.
            output_filename: Name for the output video file.
            background_color: Hex color for background (FFmpeg format).
            waveform_color: Hex color for waveform (FFmpeg format).

        Returns:
            Path to the generated video, or None if generation failed.
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None

        # Generate output filename
        if output_filename is None:
            audio_basename = os.path.splitext(os.path.basename(audio_path))[0]
            output_filename = f"{audio_basename}_waveform.mp4"

        output_path = os.path.join(self.output_folder, output_filename)
        width, height = self.resolution

        try:
            # Build FFmpeg command with showwaves filter
            cmd = [
                "ffmpeg",
                "-y",
                "-i", audio_path,
                "-filter_complex",
                f"[0:a]showwaves=s={width}x{height}:mode=cline:rate={self.fps}"
                f":colors={waveform_color}[v]",
                "-map", "[v]",
                "-map", "0:a",
                "-c:v", self.DEFAULT_VIDEO_CODEC,
                "-c:a", self.DEFAULT_AUDIO_CODEC,
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-crf", str(self.DEFAULT_CRF),
                output_path,
            ]

            logger.info("Generating video with waveform visualization...")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return None

            logger.info(f"Waveform video generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate waveform video: {e}")
            return None

    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Get information about a video file.

        Args:
            video_path: Path to the video file.

        Returns:
            Dictionary with video information, or None if failed.
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None

        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            import json
            info = json.loads(result.stdout)

            # Extract relevant information
            video_info = {
                "duration": float(info.get("format", {}).get("duration", 0)),
                "size": int(info.get("format", {}).get("size", 0)),
                "format": info.get("format", {}).get("format_name", ""),
            }

            # Get video stream info
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "video":
                    video_info["width"] = stream.get("width")
                    video_info["height"] = stream.get("height")
                    # Safely parse frame rate (format: "num/den")
                    frame_rate = stream.get("r_frame_rate", "0/1")
                    try:
                        if "/" in frame_rate:
                            num, den = frame_rate.split("/")
                            fps_val = float(num) / float(den) if den != "0" else 0
                            video_info["fps"] = fps_val
                        else:
                            video_info["fps"] = float(frame_rate)
                    except (ValueError, ZeroDivisionError):
                        video_info["fps"] = 0
                    video_info["video_codec"] = stream.get("codec_name")
                elif stream.get("codec_type") == "audio":
                    video_info["audio_codec"] = stream.get("codec_name")
                    video_info["sample_rate"] = stream.get("sample_rate")

            return video_info

        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            return None
