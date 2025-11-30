import logging
import os
import time
from typing import Dict, List, Optional

import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize

logger = logging.getLogger(__name__)


class MixCreator:
    def __init__(self, output_folder: str = "output_mixes"):
        """
        Initialize the MixCreator.

        Args:
            output_folder: Directory for output mixes
        """
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

        # Define mix profiles
        self.mix_profiles = {
            "sleep": {
                "fade_in": 10000,  # 10 seconds
                "fade_out": 10000,
                "crossfade": 5000,
                "volume_adjustments": {
                    "rain": 0,
                    "thunder": -6,
                    "white_noise": -3,
                    "nature": -2,
                },
                "low_pass": 4000,  # Frequency cutoff for sleep mix
            },
            "focus": {
                "fade_in": 5000,
                "fade_out": 5000,
                "crossfade": 3000,
                "volume_adjustments": {
                    "rain": -3,
                    "thunder": -10,
                    "white_noise": 0,
                    "nature": -4,
                },
                "band_pass": (500, 6000),  # Frequency range for focus
            },
            "relax": {
                "fade_in": 8000,
                "fade_out": 8000,
                "crossfade": 4000,
                "volume_adjustments": {
                    "rain": -2,
                    "thunder": -8,
                    "white_noise": -5,
                    "nature": 0,
                },
                "low_pass": 8000,
            },
        }

    def create_mix(
        self,
        audio_files: Dict[str, List[str]],
        mix_type: str = "sleep",
        duration_minutes: int = 60,
        output_format: str = "mp3",
        bitrate: str = "192k",
        add_binaural_beats: bool = False,
        binaural_base_freq: float = 200.0,
        binaural_beat_freq: float = 5.0,
    ) -> Optional[str]:
        """
        Create an audio mix from the provided files.

        Args:
            audio_files: Dictionary of categories with file paths
            mix_type: Type of mix to create (sleep/focus/relax)
            duration_minutes: Duration of mix in minutes
            output_format: Output file format
            bitrate: Output bitrate
            add_binaural_beats: Whether to add binaural beats to the mix.
            binaural_base_freq: Base frequency for binaural beats.
            binaural_beat_freq: Beat frequency for binaural beats.

        Returns:
            Path to the created mix file
        """
        try:
            # Convert duration to milliseconds
            target_duration = duration_minutes * 60 * 1000

            # Get mix profile
            profile = self.mix_profiles.get(mix_type, self.mix_profiles["sleep"])

            # Create base silent mix
            mix = AudioSegment.silent(duration=target_duration)

            # Add each category of sounds
            for category, files in audio_files.items():
                if not files:
                    continue

                # Create submix for this category
                category_mix = self._create_category_mix(
                    files, target_duration, profile["crossfade"]
                )

                # Apply volume adjustment
                volume_adjust = profile["volume_adjustments"].get(category, 0)
                if volume_adjust != 0:
                    category_mix = category_mix + volume_adjust

                # Layer into main mix
                mix = mix.overlay(category_mix)

            # Apply effects based on mix type
            mix = self._apply_mix_effects(mix, profile)

            # Add binaural beats if requested
            if add_binaural_beats:
                binaural_segment = self._generate_binaural_beats(
                    duration_ms=target_duration,
                    base_freq=binaural_base_freq,
                    beat_freq=binaural_beat_freq,
                )
                if binaural_segment:
                    # Ensure binaural beats are stereo if mix is mono, or convert mix to stereo
                    if mix.channels == 1 and binaural_segment.channels == 2:
                        mix = mix.set_channels(2)
                    elif mix.channels == 2 and binaural_segment.channels == 1:
                        # This case should ideally not happen with current binaural generation
                        # but as a fallback, make binaural stereo by duplicating channel
                        binaural_segment = AudioSegment.from_mono_audiosegments(
                            binaural_segment, binaural_segment
                        )

                    # Overlay with a specific volume for binaural beats, e.g., -12dB
                    # The volume is already applied in _generate_binaural_beats,
                    # but could be adjusted further here if needed.
                    mix = mix.overlay(binaural_segment)
                    logger.info("Added binaural beats to the mix.")

            # Export mix
            timestamp = int(time.time())
            output_filename = f"{mix_type}_mix_{timestamp}.{output_format}"
            output_path = os.path.join(self.output_folder, output_filename)

            mix.export(
                output_path,
                format=output_format,
                bitrate=bitrate,
                tags={
                    "title": f"Sleep Sound Mix {timestamp}",
                    "date": time.strftime("%Y-%m-%d"),
                    "genre": mix_type,
                },
            )

            logger.info(f"Created mix: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error creating mix: {str(e)}")
            return None

    def _create_category_mix(
        self, files: List[str], target_duration: int, crossfade_duration: int
    ) -> AudioSegment:
        """
        Create a continuous mix for a single category of sounds.

        Args:
            files: List of audio file paths
            target_duration: Target duration in milliseconds
            crossfade_duration: Crossfade duration in milliseconds

        Returns:
            Mixed audio segment
        """
        # Load and normalize all files
        audio_segments = []
        for file_path in files:
            try:
                audio = AudioSegment.from_file(file_path)
                audio = normalize(audio)
                audio_segments.append(audio)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")

        if not audio_segments:
            return AudioSegment.silent(duration=target_duration)

        # Create continuous mix
        mix = AudioSegment.empty()
        current_duration = 0

        while current_duration < target_duration:
            # Select random segment
            segment = np.random.choice(audio_segments)

            if current_duration == 0:
                mix = segment
            else:
                # Crossfade with previous audio
                mix = mix.append(segment, crossfade=crossfade_duration)

            current_duration = len(mix)

        # Trim to exact duration
        mix = mix[:target_duration]

        return mix

    def _apply_mix_effects(self, mix: AudioSegment, profile: dict) -> AudioSegment:
        """
        Apply effects based on mix profile.

        Args:
            mix: Audio mix to process
            profile: Mix profile containing effect parameters

        Returns:
            Processed audio mix
        """
        # Apply fade in/out
        mix = mix.fade_in(profile["fade_in"]).fade_out(profile["fade_out"])

        # Apply frequency filtering based on mix type
        if "low_pass" in profile:
            mix = mix.low_pass_filter(profile["low_pass"])
        elif "band_pass" in profile:
            low, high = profile["band_pass"]
            mix = mix.low_pass_filter(high).high_pass_filter(low)

        # Normalize final mix
        mix = normalize(mix)

        return mix

    def _generate_binaural_beats(
        self,
        duration_ms: int,
        base_freq: float = 200.0,  # Hz
        beat_freq: float = 5.0,  # Hz (e.g., for Alpha waves)
        sample_rate: int = 44100,
        volume: float = -12.0,  # dBFS, relatively quiet
    ) -> Optional[AudioSegment]:
        """
        Generate a binaural beat audio segment.

        Args:
            duration_ms: Duration of the binaural beat in milliseconds.
            base_freq: Base frequency for the tones (e.g., 200 Hz).
            beat_freq: The difference in frequency between the two tones (e.g., 5 Hz).
            sample_rate: Sample rate for the audio.
            volume: Volume of the generated tones in dBFS.

        Returns:
            An AudioSegment containing the binaural beat, or None on error.
        """
        try:
            t = np.linspace(
                0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False
            )

            # Frequencies for left and right channels
            freq_left = base_freq
            freq_right = base_freq + beat_freq

            # Generate sine waves
            note_left = np.sin(freq_left * 2 * np.pi * t)
            note_right = np.sin(freq_right * 2 * np.pi * t)

            # Convert to 16-bit PCM
            # Ensure amplitude is within 16-bit range before conversion
            max_amplitude = 2**15 - 1
            audio_left = (note_left * max_amplitude).astype(np.int16)
            audio_right = (note_right * max_amplitude).astype(np.int16)

            # Create stereo audio segment
            # For pydub, stereo data is interleaved: L, R, L, R...
            stereo_signal = np.empty((len(t) * 2,), dtype=np.int16)
            stereo_signal[0::2] = audio_left  # Left channel
            stereo_signal[1::2] = audio_right  # Right channel

            binaural_segment = AudioSegment(
                stereo_signal.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,  # 16-bit = 2 bytes
                channels=2,  # Stereo
            )

            # Apply volume adjustment
            binaural_segment = binaural_segment + volume  # Apply gain reduction

            logger.info(
                f"Generated binaural beat: base={base_freq}Hz, beat={beat_freq}Hz, duration={duration_ms}ms"
            )
            return binaural_segment

        except Exception as e:
            logger.error(f"Error generating binaural beats: {e}")
            return None

    def preview_mix(
        self,
        audio_files: Dict[str, List[str]],
        mix_type: str = "sleep",
        preview_duration: int = 30,
    ) -> Optional[AudioSegment]:
        """
        Create a short preview of the mix.

        Args:
            audio_files: Dictionary of categories with file paths
            mix_type: Type of mix to create
            preview_duration: Duration of preview in seconds

        Returns:
            Audio preview segment
        """
        try:
            # Create full mix but with shorter duration
            preview_path = self.create_mix(
                audio_files, mix_type=mix_type, duration_minutes=preview_duration / 60
            )

            if preview_path and os.path.exists(preview_path):
                preview = AudioSegment.from_file(preview_path)
                # Clean up preview file
                os.remove(preview_path)
                return preview

        except Exception as e:
            logger.error(f"Error creating preview: {str(e)}")

        return None

    def save_preview(
        self,
        preview: AudioSegment,
        output_path: str,
        format: str = "mp3",
        bitrate: str = "128k",
    ) -> bool:
        """
        Save a preview mix to file.

        Args:
            preview: Preview audio segment
            output_path: Path to save preview
            format: Output format
            bitrate: Output bitrate

        Returns:
            True if successful, False otherwise
        """
        try:
            preview.export(
                output_path,
                format=format,
                bitrate=bitrate,
                tags={"title": "Mix Preview"},
            )
            return True
        except Exception as e:
            logger.error(f"Error saving preview: {str(e)}")
            return False
