"""Tests for audio processing functionality."""

import os
from pathlib import Path
from typing import Dict

import numpy as np
import pytest
from pydub import AudioSegment

from project_name.core.processor import SoundProcessor


@pytest.mark.unit
class TestSoundProcessor:
    @pytest.fixture
    def processor(self, temp_dir: Path) -> SoundProcessor:
        """Create a SoundProcessor instance for testing."""
        return SoundProcessor(
            input_folder=str(temp_dir / "input"),
            processed_folder=str(temp_dir / "processed"),
        )

    def test_init(self, processor: SoundProcessor, temp_dir: Path):
        """Test SoundProcessor initialization."""
        assert os.path.exists(temp_dir / "input")
        assert os.path.exists(temp_dir / "processed")
        assert processor.sample_rate == 44100
        assert processor.channels == 2

    def test_preprocess_audio(self, processor: SoundProcessor, mock_audio_file: Path):
        """Test audio preprocessing."""
        output_path = processor.preprocess_audio(str(mock_audio_file))

        assert output_path is not None
        assert os.path.exists(output_path)

        # Verify processed audio properties
        audio = AudioSegment.from_file(output_path)
        assert audio.channels == processor.channels
        assert audio.frame_rate == processor.sample_rate

    def test_trim_silence(self, processor: SoundProcessor, mock_audio_file: Path):
        """Test silence trimming from audio."""
        # Create audio with silence
        silence = AudioSegment.silent(duration=1000)
        audio = AudioSegment.from_file(str(mock_audio_file))
        padded_audio = silence + audio + silence

        # Save padded audio
        temp_path = str(mock_audio_file.parent / "padded_audio.wav")
        padded_audio.export(temp_path, format="wav")

        # Process
        trimmed_path = processor.trim_silence(temp_path)
        trimmed_audio = AudioSegment.from_file(trimmed_path)

        # Verify trimming
        assert len(trimmed_audio) < len(padded_audio)
        assert abs(len(trimmed_audio) - len(audio)) < 100  # Allow small variation

    def test_apply_bandpass_filter(
        self, processor: SoundProcessor, mock_audio_file: Path
    ):
        """Test bandpass filter application."""
        low_cutoff = 200
        high_cutoff = 5000

        filtered_audio = processor._apply_bandpass_filter(
            AudioSegment.from_file(str(mock_audio_file)), low_cutoff, high_cutoff
        )

        assert isinstance(filtered_audio, AudioSegment)
        assert len(filtered_audio) > 0

        # Convert to numpy array for frequency analysis
        samples = np.array(filtered_audio.get_array_of_samples())

        # Perform FFT to check frequency content
        fft = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(samples), 1 / filtered_audio.frame_rate)

        # Verify frequency content is mostly within the bandpass range
        magnitude = np.abs(fft)
        freq_mask = (freqs > low_cutoff) & (freqs < high_cutoff)
        assert np.sum(magnitude[freq_mask]) > np.sum(magnitude[~freq_mask])

    def test_analyze_audio_features(
        self, processor: SoundProcessor, mock_audio_file: Path
    ):
        """Test audio feature extraction."""
        features = processor.analyze_audio_features(str(mock_audio_file))

        required_features = {
            "duration",
            "rms_energy",
            "spectral_centroid",
            "spectral_bandwidth",
            "tempo",
        }

        assert isinstance(features, dict)
        assert all(feature in features for feature in required_features)
        assert features["duration"] > 0
        assert features["rms_energy"] >= 0
        assert features["spectral_centroid"] > 0
        assert features["spectral_bandwidth"] > 0
        assert features["tempo"] > 0

    def test_normalize_audio(self, processor: SoundProcessor, mock_audio_file: Path):
        """Test audio normalization."""
        target_db = -20
        audio = AudioSegment.from_file(str(mock_audio_file))
        normalized = processor.normalize_audio(audio, target_db)

        assert isinstance(normalized, AudioSegment)
        assert abs(normalized.dBFS - target_db) < 1.0  # Allow 1dB tolerance

    def test_process_batch(
        self, processor: SoundProcessor, temp_dir: Path, mock_audio_file: Path
    ):
        """Test batch processing of multiple files."""
        # Create multiple test files
        input_dir = temp_dir / "input"
        for i in range(3):
            dest = input_dir / f"test_{i}.wav"
            AudioSegment.from_file(str(mock_audio_file)).export(str(dest), format="wav")

        # Process batch
        processed_files = processor.process_batch()

        assert len(processed_files) == 3
        assert all(os.path.exists(f) for f in processed_files)
        assert all(f.startswith(str(temp_dir / "processed")) for f in processed_files)

    @pytest.mark.parametrize(
        "effect,params",
        [
            ("fade_in", {"duration": 5000}),
            ("fade_out", {"duration": 5000}),
            ("low_pass_filter", {"cutoff": 4000}),
            ("compress", {"threshold": -20, "ratio": 4.0}),
        ],
    )
    def test_audio_effects(
        self,
        processor: SoundProcessor,
        mock_audio_file: Path,
        effect: str,
        params: Dict,
    ):
        """Test various audio effects."""
        audio = AudioSegment.from_file(str(mock_audio_file))

        if effect == "fade_in":
            processed = processor.apply_fade_in(audio, params["duration"])
        elif effect == "fade_out":
            processed = processor.apply_fade_out(audio, params["duration"])
        elif effect == "low_pass_filter":
            processed = processor._apply_lowpass_filter(audio, params["cutoff"])
        elif effect == "compress":
            processed = processor.apply_compression(
                audio, params["threshold"], params["ratio"]
            )

        assert isinstance(processed, AudioSegment)
        assert len(processed) == len(audio)  # Effects shouldn't change duration

    def test_error_handling(self, processor: SoundProcessor, temp_dir: Path):
        """Test error handling for invalid files and operations."""
        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            processor.preprocess_audio(str(temp_dir / "nonexistent.wav"))

        # Test with invalid file
        invalid_file = temp_dir / "invalid.wav"
        invalid_file.touch()  # Create empty file
        with pytest.raises(Exception):
            processor.preprocess_audio(str(invalid_file))

        # Test with invalid parameters
        audio = AudioSegment.silent(duration=1000)
        with pytest.raises(ValueError):
            processor._apply_bandpass_filter(audio, -100, 5000)  # Invalid low cutoff
        with pytest.raises(ValueError):
            processor.normalize_audio(audio, 20)  # Invalid target dB (too high)
