import logging
import os
import time
from typing import Dict, List, Tuple

import librosa
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize

logger = logging.getLogger(__name__)


class SoundProcessor:
    """
    Main class for audio processing and mixing.
    """

    def __init__(
        self,
        input_folder: str = "input_clips",
        processed_folder: str = "processed_clips",
        output_folder: str = "output_mixes",
        sample_rate: int = 44100,
        bit_rate: str = "192k",
    ):
        """
        Initialize the sound processor with configurable paths and settings.

        Args:
            input_folder: Directory containing raw audio files.
            processed_folder: Directory for storing processed audio.
            output_folder: Directory for final mixes.
            sample_rate: Audio sample rate (Hz).
            bit_rate: Output bit rate for final mixes.
        """
        self.input_folder = input_folder
        self.processed_folder = processed_folder
        self.output_folder = output_folder
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.channels = 2  # Default to stereo

        # Create necessary directories
        for folder in [input_folder, processed_folder, output_folder]:
            os.makedirs(folder, exist_ok=True)

    def analyze_audio_features(self, file_path: str) -> Dict[str, float]:
        """
        Analyze an audio file and return core features required by tests.
        """
        try:
            y, sr = librosa.load(file_path, sr=self.sample_rate)
            features = self._extract_audio_features(y, sr)
            # Map to the expected keys
            return {
                "duration": features.get("duration", 0.0),
                "rms_energy": float(np.mean(librosa.feature.rms(y=y))),
                "spectral_centroid": features.get("spectral_centroid", 0.0),
                "spectral_bandwidth": features.get("spectral_bandwidth", 0.0),
                "tempo": features.get("tempo", 0.0),
            }
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.warning(f"analyze_audio_features failed for {file_path}: {e}")
            return {
                "duration": 0.0,
                "rms_energy": 0.0,
                "spectral_centroid": 0.0,
                "spectral_bandwidth": 0.0,
                "tempo": 0.0,
            }

    def trim_silence(
        self, file_path: str, silence_thresh: int = -40, min_silence_len: int = 500
    ) -> str:
        """
        Trim leading and trailing silence from an audio file and save processed file.
        Raises FileNotFoundError if file does not exist.
        """
        from pydub.silence import detect_nonsilent

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        audio = AudioSegment.from_file(file_path)
        nonsilent_ranges = detect_nonsilent(
            audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh
        )
        if not nonsilent_ranges:
            # Nothing but silence - return empty silent file
            trimmed = AudioSegment.silent(duration=0)
        else:
            start = nonsilent_ranges[0][0]
            end = nonsilent_ranges[-1][1]
            trimmed = audio[start:end]

        # Save trimmed file
        filename = os.path.basename(file_path)
        output_filename = f"trim_{os.path.splitext(filename)[0]}.wav"
        output_path = os.path.join(self.processed_folder, output_filename)
        trimmed.export(output_path, format="wav")
        logger.info(f"Trimmed silence saved to {output_path}")
        return output_path

    def normalize_audio(
        self, audio: AudioSegment, target_db: float = -20.0
    ) -> AudioSegment:
        """
        Normalize an AudioSegment to target dBFS.
        """
        try:
            change_dB = target_db - audio.dBFS
            return audio.apply_gain(change_dB)
        except Exception as e:
            logger.error(f"normalize_audio failed: {e}")
            return audio

    def process_batch(self) -> list:
        """
        Process all files in the input folder and return a list of processed file paths.
        """
        processed = []
        for fname in os.listdir(self.input_folder):
            src = os.path.join(self.input_folder, fname)
            result = self.preprocess_audio(src)
            if result:
                processed.append(result)
        return processed

    def apply_fade_in(self, audio: AudioSegment, duration_ms: int) -> AudioSegment:
        return audio.fade_in(duration_ms)

    def apply_fade_out(self, audio: AudioSegment, duration_ms: int) -> AudioSegment:
        return audio.fade_out(duration_ms)

    def apply_compression(
        self, audio: AudioSegment, threshold: int, ratio: float
    ) -> AudioSegment:
        return self._apply_compression(audio, threshold, ratio)

        # Initialize empty categories
        self.categories = {
            "rain": [],
            "thunder": [],
            "white_noise": [],
            "nature": [],
            "water": [],
            "other": [],
        }

        # Initialize audio similarity matcher if available
        self.similarity_matcher = None
        if SIMILARITY_AVAILABLE:
            try:
                self.similarity_matcher = create_similarity_matcher(content_type="env")
                logger.info("Audio similarity matching initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize similarity matching: {e}")
                self.similarity_matcher = None

    def preprocess_audio(self, file_path: str) -> str | None:
        """
        Load, clean, and normalize a single audio file.
        Handles MP3, WAV, FLAC, OGG, and M4A formats.

        Args:
            file_path: Path to the input audio file.

        Returns:
            Path to the processed file, or None if processing failed.
        """
        logger.info(f"Preprocessing audio file: {file_path}")

        # Define supported file extensions
        supported_extensions = (".wav", ".mp3", ".flac", ".ogg", ".m4a")

        if not file_path.lower().endswith(supported_extensions):
            logger.warning(f"Unsupported file type: {file_path}")
            return None

        try:
            audio = AudioSegment.from_file(file_path)
            # Use instance attributes for sample rate and channels
            audio = audio.set_frame_rate(self.sample_rate).set_channels(self.channels)
            audio = normalize(audio)  # Use normalize from pydub.effects

            # Create output filename
            filename = os.path.basename(file_path)
            output_filename = (
                f"proc_{os.path.splitext(filename)[0]}.wav"  # Ensure output is wav
            )
            output_path = os.path.join(self.processed_folder, output_filename)

            # Save processed audio
            audio.export(output_path, format="wav")
            logger.info(f"Processed and saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    def analyze_clips(self) -> Dict[str, List[str]]:
        """
        Analyze and categorize audio clips based on audio features.

        Returns:
            Dictionary of categories with file paths.
        """
        logger.info("Analyzing audio clips...")

        # Reset categories
        for key in self.categories:
            self.categories[key] = []

        # Process each audio file
        for filename in os.listdir(self.processed_folder):
            file_path = os.path.join(self.processed_folder, filename)
            try:
                y, sr = librosa.load(file_path, sr=self.sample_rate)

                # Extract comprehensive features
                basic_features = self._extract_audio_features(y, sr)
                psycho_features = self.extract_psychoacoustic_features(y, sr)
                temporal_features = self.analyze_temporal_patterns(y, sr)

                # Combine all features
                combined_features = {
                    **basic_features,
                    **psycho_features,
                    **temporal_features,
                }

                category = self._enhanced_classification(
                    combined_features
                )  # Use enhanced classification
                self.categories[category].append(file_path)
                logger.info(f"Analyzed and classified {filename} as {category}")
            except Exception as e:
                logger.error(f"Error analyzing {filename}: {str(e)}")
                # Optionally, add to 'other' category or handle as appropriate
                self.categories["other"].append(file_path)

        # Log results
        for category, files in self.categories.items():
            logger.info(f"Category '{category}': {len(files)} clips")

        return self.categories  # Return instance attribute

    # Placeholder for missing method
    def analyze_audio_features(self, file_path: str) -> Dict[str, float]:
        """
        Placeholder for audio feature analysis.
        """
        logger.warning(
            f"analyze_audio_features not fully implemented. Returning dummy data for {file_path}"
        )
        # In a real implementation, load the file and extract features
        # y, sr = librosa.load(file_path, sr=self.sample_rate)
        # return self._extract_audio_features(y, sr)
        return {"dummy_feature": 0.0}

    def _extract_audio_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Extract audio features for classification.

        Args:
            y: Audio time series.
            sr: Sample rate.

        Returns:
            Dictionary of audio features.
        """
        features = {
            "tempo": librosa.beat.tempo(y, sr=sr)[0],
            "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "spectral_bandwidth": np.mean(
                librosa.feature.spectral_bandwidth(y=y, sr=sr)
            ),
            "zero_crossing_rate": np.mean(librosa.feature.zero_crossing_rate(y=y)),
            "duration": librosa.get_duration(y=y, sr=sr),
            "loudness": float(np.mean(librosa.feature.rms(y=y))),
        }

        # Add more detailed features for advanced analysis
        features["spectral_contrast"] = np.mean(
            librosa.feature.spectral_contrast(y=y, sr=sr)
        )
        features["spectral_flatness"] = np.mean(librosa.feature.spectral_flatness(y=y))
        features["spectral_rolloff"] = np.mean(
            librosa.feature.spectral_rolloff(y=y, sr=sr)
        )
        features["mfccs"] = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13))

        return features

    def extract_psychoacoustic_features(
        self, y: np.ndarray, sr: int
    ) -> Dict[str, float]:
        """
        Extract psychoacoustic features related to human perception of sound.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Dictionary of psychoacoustic features
        """
        # Calculate average energy in different frequency bands
        spec = np.abs(librosa.stft(y))

        # Convert to mel scale which better represents human hearing
        mel_spec = librosa.feature.melspectrogram(S=spec**2, sr=sr)

        # Frequency bands in Hz
        bands = {
            "infrasonic": (20, 60),  # Very low rumble
            "low": (60, 250),  # Bass
            "low_mid": (250, 500),  # Lower midrange
            "mid": (500, 2000),  # Midrange
            "high_mid": (2000, 4000),  # Upper midrange
            "high": (4000, 6000),  # High frequencies
            "very_high": (6000, 20000),  # Very high frequencies / sibilance
        }

        # Calculate energy in each band
        band_energy = {}
        for name, (fmin, fmax) in bands.items():
            band_energy[f"{name}_energy"] = float(
                np.mean(
                    librosa.feature.spectral_contrast(y=y, sr=sr, fmin=fmin, fmax=fmax)
                )
            )

        # Calculate roughness (related to dissonance)
        # Simplified version - detect amplitude modulation in relevant bands
        hop_length = 512
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
        # A measure of "roughness" is how much the onset envelope varies
        roughness = float(
            np.std(onset_env) / np.mean(onset_env) if np.mean(onset_env) > 0 else 0
        )

        # Calculate tonalness vs. noisiness
        flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))
        tonalness = 1.0 - flatness  # Higher flatness = more noise-like

        # Estimate relaxation potential score (custom measure)
        # High in consistent low tones, low in jarring high frequencies with roughness
        relaxation_score = (
            band_energy["low_energy"] * 0.3
            + band_energy["mid_energy"] * 0.2
            - band_energy["high_energy"] * 0.2
            - band_energy["very_high_energy"] * 0.3
            - roughness * 5
        )

        # Extract tempo stability
        tempo, tempo_confidence = librosa.beat.beat_track(y=y, sr=sr)

        # Bundle all features
        features = {
            "roughness": roughness,
            "flatness": flatness,
            "tonalness": tonalness,
            "relaxation_score": float(relaxation_score),
            "tempo_stability": float(tempo_confidence),
        }

        # Add band energies
        features.update(band_energy)

        return features

    def analyze_temporal_patterns(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Analyze temporal patterns in the audio like repetitiveness and cadence.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Dictionary of temporal features
        """
        # Compute onset strength
        hop_length = 512
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

        # Detect beats
        tempo, beats = librosa.beat.beat_track(
            onset_envelope=onset_env, sr=sr, hop_length=hop_length
        )

        # Compute tempo stability - how consistent is the rhythm
        if len(beats) > 2:
            beat_intervals = np.diff(beats)
            tempo_consistency = 1.0 - (np.std(beat_intervals) / np.mean(beat_intervals))
        else:
            tempo_consistency = 0.0

        # Compute repetitiveness using self-similarity matrix
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
        mfccs_scaled = np.mean(mfccs, axis=1)

        # Use autocorrelation to detect repetitive patterns
        if len(mfccs_scaled) > 1:
            correlations = np.correlate(mfccs_scaled, mfccs_scaled, mode="full")
            correlations = correlations[
                len(correlations) // 2 :
            ]  # Take only second half

            # Normalize
            if correlations[0] > 0:
                correlations = correlations / correlations[0]

            # Calculate repetitiveness score (higher value = more repetitive)
            repetitiveness_score = float(
                np.mean(correlations[1 : min(50, len(correlations))])
            )
        else:
            repetitiveness_score = 0.0

        # Calculate cadence regularity - how consistent are onsets
        if len(onset_env) > 1:
            # Get peak positions
            peaks = librosa.util.peak_pick(onset_env, 3, 3, 3, 5, 0.5, 10)

            if len(peaks) > 2:
                peak_intervals = np.diff(peaks)
                cadence_regularity = 1.0 - min(
                    1.0, np.std(peak_intervals) / np.mean(peak_intervals)
                )
            else:
                cadence_regularity = 0.5  # Not enough peaks to determine
        else:
            cadence_regularity = 0.0

        # Analyze evenness of sound - does it have consistent volume or many peaks and valleys
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        if len(rms) > 0:
            evenness = 1.0 - min(1.0, np.std(rms) / np.mean(rms))
        else:
            evenness = 0.0

        # Estimate naturalness score - natural sounds tend to be less perfectly regular
        # than artificial ones, but still have some structure
        naturalness_score = (
            repetitiveness_score * 0.4  # Some repetition is natural
            + (1 - cadence_regularity) * 0.3  # Not too perfect cadence
            + tempo_consistency * 0.3
        )  # But still some consistency

        # Bundle results
        features = {
            "tempo": float(tempo),
            "tempo_consistency": float(tempo_consistency),
            "repetitiveness_score": float(repetitiveness_score),
            "cadence_regularity": float(cadence_regularity),
            "evenness": float(evenness),
            "naturalness_score": float(naturalness_score),
        }

        return features

    def analyze_sleep_quality(self, file_path: str) -> Dict[str, float]:
        """
        Analyze how suitable a sound is for sleep based on various metrics.

        Args:
            file_path: Path to audio file

        Returns:
            Dictionary of sleep quality metrics
        """
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=self.sample_rate)

            # Extract basic features
            features = self._extract_audio_features(y, sr)
            psycho_features = self.extract_psychoacoustic_features(y, sr)
            temporal_features = self.analyze_temporal_patterns(y, sr)

            # Calculate sleep induction potential
            # Research suggests sounds with these characteristics are best for sleep:
            # - Low to moderate density (not too sparse, not too busy)
            # - Consistent but not entirely predictable
            # - Low to mid frequencies dominate
            # - Minimal high frequency content
            # - Natural-sounding
            # - Gradual changes rather than sudden ones

            # Create component scores
            frequency_score = (
                (1.0 - min(1.0, features["spectral_centroid"] / 4000))
                * 0.5  # Lower center frequency is better
                + max(
                    0.0,
                    psycho_features["low_energy"] - psycho_features["very_high_energy"],
                )
                * 0.5  # More lows than highs
            )

            consistency_score = (
                temporal_features["evenness"] * 0.4  # Even volume
                + (1.0 - abs(0.7 - temporal_features["repetitiveness_score"]) / 0.7)
                * 0.3  # Moderate repetition (~0.7 is optimal)
                + (1.0 - features["zero_crossing_rate"] * 20)
                * 0.3  # Fewer zero crossings
            )

            naturalness_score = (
                temporal_features["naturalness_score"] * 0.5
                + psycho_features["relaxation_score"] * 0.5
            )

            # Combine component scores with weights
            sleep_induction_potential = (
                frequency_score * 0.4
                + consistency_score * 0.4
                + naturalness_score * 0.2
            )

            # Scale to a nice 0-10 range and ensure it's between 0-10
            sleep_induction_potential = max(0, min(10, sleep_induction_potential * 10))

            # Bundle results
            metrics = {
                "frequency_score": float(frequency_score),
                "consistency_score": float(consistency_score),
                "naturalness_score": float(naturalness_score),
                "sleep_induction_potential": float(sleep_induction_potential),
            }

            return metrics

        except Exception as e:
            logger.error(
                f"Error analyzing sleep quality for {os.path.basename(file_path)}: {str(e)}"
            )
            # Return default values
            return {
                "frequency_score": 0.0,
                "consistency_score": 0.0,
                "naturalness_score": 0.0,
                "sleep_induction_potential": 0.0,
            }

    # The _classify_by_rules method was here but has been removed as it's superseded
    # by _enhanced_classification and is no longer called.

    def create_mix(self, target_duration_min: int = 60, mix_type: str = "sleep") -> str:
        """
        Create an audio mix based on specified parameters.

        Args:
            target_duration_min: Duration in minutes.
            mix_type: Type of mix ('sleep', 'focus', 'relax').

        Returns:
            Path to created mix file.
        """
        target_duration_ms = target_duration_min * 60 * 1000
        mix = AudioSegment.silent(duration=target_duration_ms)

        # Add each category sound to the mix with appropriate volume
        for category, files in self.categories.items():
            if files:
                # Select a random file from the category
                sound_path = np.random.choice(files)
                sound = AudioSegment.from_file(sound_path)

                # Make sure sound is long enough (loop if needed)
                while len(sound) < target_duration_ms:
                    sound += sound

                # Trim to target duration
                sound = sound[:target_duration_ms]

                # Adjust volume based on mix type and category
                volume_adjustment = self._get_category_volume(category, mix_type)
                if volume_adjustment != 0:
                    sound = sound + volume_adjustment

                # Apply fade in/out
                fade_duration = min(10000, len(sound) // 10)
                sound = sound.fade_in(fade_duration).fade_out(fade_duration)

                # Overlay onto the mix
                mix = mix.overlay(sound)

        # Apply final mix processing based on mix type
        mix = self._apply_mix_processing(mix, mix_type)

        output_filename = f"{mix_type}_mix_{int(time.time())}.mp3"
        output_path = os.path.join(self.output_folder, output_filename)
        mix.export(output_path, format="mp3", bitrate=self.bit_rate)

        logger.info(f"Created {mix_type} mix: {output_path}")
        return output_path

    def _get_category_volume(self, category: str, mix_type: str) -> int:
        """Get appropriate volume adjustment for a category in a mix type."""
        # Adjust volumes based on mix type
        volume_map = {
            "sleep": {
                "rain": 0,
                "thunder": -6,
                "white_noise": -3,
                "nature": -2,
                "water": 0,
                "other": -4,
            },
            "focus": {
                "rain": -3,
                "thunder": -10,
                "white_noise": 0,
                "nature": -6,
                "water": -2,
                "other": -5,
            },
            "relax": {
                "rain": -2,
                "thunder": -8,
                "white_noise": -5,
                "nature": 0,
                "water": 0,
                "other": -3,
            },
        }

        # Get volume adjustment or default to -3 dB
        return volume_map.get(mix_type, {}).get(category, -3)

    def _apply_mix_processing(self, mix: AudioSegment, mix_type: str) -> AudioSegment:
        """Apply final processing to mix based on mix type."""
        # Normalize to ensure good volume
        mix = normalize(mix, headroom=1.0)

        # Apply gentle compression
        mix = self._apply_compression(mix, threshold=-20, ratio=2.0)

        # Apply slight EQ based on mix type
        if mix_type == "sleep":
            # Reduce high frequencies for sleep
            mix = self._apply_lowpass_filter(mix, cutoff=4000)
        elif mix_type == "focus":
            # Slight boost to mid frequencies for focus
            mix = self._apply_bandpass_filter(mix, low_cutoff=500, high_cutoff=6000)
        elif mix_type == "relax":
            # Gentle low-pass but keep more highs than sleep
            mix = self._apply_lowpass_filter(mix, cutoff=8000)

        return mix

    def _apply_lowpass_filter(self, audio: AudioSegment, cutoff: int) -> AudioSegment:
        """Simple wrapper around pydub's low_pass_filter."""
        return audio.low_pass_filter(cutoff)

    def _apply_bandpass_filter(
        self, audio: AudioSegment, low_cutoff: int, high_cutoff: int
    ) -> AudioSegment:
        """Apply bandpass filter to audio."""
        return audio.low_pass_filter(high_cutoff).high_pass_filter(low_cutoff)

    def _apply_compression(
        self, audio: AudioSegment, threshold: int, ratio: float
    ) -> AudioSegment:
        """
        Apply a simple compressor to the audio.

        Args:
            audio: Input audio
            threshold: Threshold in dB
            ratio: Compression ratio

        Returns:
            Compressed audio
        """
        # This is a simplified compressor implementation
        # In a real system, we'd use a proper audio DSP library

        # Convert to array
        samples = np.array(audio.get_array_of_samples())

        # Convert threshold to linear scale
        threshold_linear = 10 ** (threshold / 20.0)

        # Calculate gain reduction
        # Samples above threshold are reduced by the ratio
        abs_samples = np.abs(samples)
        scale = np.ones_like(abs_samples, dtype=float)

        # Find samples above threshold
        mask = abs_samples > threshold_linear

        # Apply compression
        scale[mask] = threshold_linear + (abs_samples[mask] - threshold_linear) / ratio
        scale[mask] /= abs_samples[mask]

        # Apply gain
        compressed_samples = samples * scale

        # Create new audio segment
        compressed_audio = AudioSegment(
            compressed_samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels,
        )

        return compressed_audio

    def classify_with_deep_learning(
        self, processed_folder: str = None, model_path: str = None
    ) -> Dict[str, List[str]]:
        """
        Classify sounds using basic machine learning techniques if available.

        Args:
            processed_folder: Folder containing processed audio files
            model_path: Optional path to trained model

        Returns:
            Dictionary of categories with file paths
        """
        # Use the provided folder or default to the instance's processed folder
        if processed_folder is None:
            processed_folder = self.processed_folder

        logger.info("Starting machine learning classification")

        # Initialize categories
        categories = {
            "rain": [],
            "thunder": [],
            "white_noise": [],
            "nature": [],
            "water": [],
            "other": [],
        }

        # Process each audio file
        for filename in os.listdir(processed_folder):
            file_path = os.path.join(processed_folder, filename)
            try:
                # Extract features
                y, sr = librosa.load(file_path, sr=self.sample_rate)
                features = self._extract_audio_features(y, sr)
                psycho_features = self.extract_psychoacoustic_features(y, sr)
                temporal_features = self.analyze_temporal_patterns(y, sr)

                # Combine all features
                combined_features = {**features, **psycho_features, **temporal_features}

                # Use classic machine learning approach with rules enhanced by feature extraction
                category = self._enhanced_classification(combined_features)

                # Add to appropriate category
                categories[category].append(file_path)
                logger.info(f"Classified {filename} as {category}")

            except Exception as e:
                logger.error(f"Error classifying {filename}: {str(e)}")
                categories["other"].append(file_path)

        # Log results
        for category, files in categories.items():
            logger.info(f"ML Category '{category}': {len(files)} clips")

        return categories

    def _enhanced_classification(self, features: Dict[str, float]) -> str:
        """
        Enhanced classification using multiple features.

        Args:
            features: Combined audio features

        Returns:
            Category name
        """
        # Define score bins for each category
        scores = {
            "rain": 0,
            "thunder": 0,
            "white_noise": 0,
            "nature": 0,
            "water": 0,
            "other": 0,
        }

        # Rain characteristics
        if features.get("spectral_centroid", 0) < 2000:
            scores["rain"] += 2

        if features.get("repetitiveness_score", 0) > 0.6:
            scores["rain"] += 1
            scores["white_noise"] += 1

        if features.get("cadence_regularity", 0) > 0.5:
            scores["rain"] += 2

        # Thunder characteristics
        if (
            features.get("spectral_centroid", 0) > 500
            and features.get("spectral_centroid", 0) < 4000
        ):
            scores["thunder"] += 1

        if features.get("loudness", 0) > 0.1:
            scores["thunder"] += 2

        # White noise characteristics
        if features.get("zero_crossing_rate", 0) > 0.1:
            scores["white_noise"] += 3

        if features.get("flatness", 0) > 0.3:  # High flatness indicates noise
            scores["white_noise"] += 2

        # Nature sounds characteristics
        if features.get("naturalness_score", 0) > 0.6:
            scores["nature"] += 3

        if (
            features.get("spectral_centroid", 0) > 3000
        ):  # Bird sounds often have higher spectral centroid
            scores["nature"] += 1

        # Water sounds characteristics
        if (
            features.get("spectral_centroid", 0) < 3000
            and features.get("naturalness_score", 0) > 0.5
        ):
            scores["water"] += 2

        # Find highest score
        max_score = max(scores.values())
        categories = [cat for cat, score in scores.items() if score == max_score]

        # If tie or all zero, use "other"
        if len(categories) > 1 or max_score == 0:
            return "other"

        return categories[0]

    def find_similar_clips(
        self, query_file: str, category: str = None, top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find audio clips similar to the query file.

        Args:
            query_file: Path to the query audio file
            category: Specific category to search in (optional)
            top_k: Number of similar clips to return

        Returns:
            List of (file_path, similarity_score) tuples
        """
        if not self.similarity_matcher:
            logger.warning("Audio similarity matching not available")
            return []

        try:
            if category and category in self.categories:
                # Search within specific category
                candidate_files = self.categories[category]
                similar_clips = self.similarity_matcher.find_similar_clips(
                    query_file, candidate_files, top_k
                )
            else:
                # Search all categorized files
                all_files = []
                for cat_files in self.categories.values():
                    all_files.extend(cat_files)

                similar_clips = self.similarity_matcher.find_similar_clips(
                    query_file, all_files, top_k
                )

            logger.info(f"Found {len(similar_clips)} similar clips for {query_file}")
            return similar_clips
        except Exception as e:
            logger.error(f"Error finding similar clips: {e}")
            return []

    def find_similar_in_all_categories(
        self, query_file: str, top_k_per_category: int = 3
    ) -> Dict[str, List[Tuple[str, float]]]:
        """
        Find similar clips within each category.

        Args:
            query_file: Path to the query audio file
            top_k_per_category: Number of similar clips per category

        Returns:
            Dict of category_name -> list of (file_path, similarity_score)
        """
        if not self.similarity_matcher:
            logger.warning("Audio similarity matching not available")
            return {}

        try:
            return self.similarity_matcher.find_similar_in_categories(
                query_file, self.categories, top_k_per_category
            )
        except Exception as e:
            logger.error(f"Error finding similar clips in categories: {e}")
            return {}

    def precompute_embeddings(self, save_cache: bool = True) -> None:
        """
        Precompute embeddings for all categorized audio files.

        Args:
            save_cache: Whether to save embeddings to disk
        """
        if not self.similarity_matcher:
            logger.warning("Audio similarity matching not available")
            return

        try:
            # Collect all categorized files
            all_files = []
            for category, files in self.categories.items():
                all_files.extend(files)
                logger.info(f"Category '{category}': {len(files)} files")

            if not all_files:
                logger.warning("No categorized files found for embedding computation")
                return

            logger.info(f"Computing embeddings for {len(all_files)} files...")

            # Batch extract embeddings
            embeddings = self.similarity_matcher.batch_extract_embeddings(all_files)

            logger.info(f"Successfully computed {len(embeddings)} embeddings")

            # Save cache if requested
            if save_cache:
                cache_path = os.path.join(self.processed_folder, "embeddings_cache.npz")
                self.similarity_matcher.save_embeddings_cache(cache_path)

            # Print cache statistics
            stats = self.similarity_matcher.get_cache_stats()
            logger.info(f"Embedding cache stats: {stats}")

        except Exception as e:
            logger.error(f"Error precomputing embeddings: {e}")

    def load_embeddings_cache(self) -> bool:
        """
        Load precomputed embeddings from cache.

        Returns:
            True if cache loaded successfully, False otherwise
        """
        if not self.similarity_matcher:
            return False

        try:
            cache_path = os.path.join(self.processed_folder, "embeddings_cache.npz")
            if os.path.exists(cache_path):
                self.similarity_matcher.load_embeddings_cache(cache_path)
                stats = self.similarity_matcher.get_cache_stats()
                logger.info(f"Loaded embeddings cache: {stats}")
                return True
            else:
                logger.info("No embeddings cache found")
                return False
        except Exception as e:
            logger.error(f"Error loading embeddings cache: {e}")
            return False


class QueueHandler(logging.Handler):
    """
    A logging handler that puts logs into a queue for the GUI
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
        self.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

    def emit(self, record):
        self.log_queue.put(self.format(record))


try:
    from .audio_similarity import AudioSimilarityMatcher, create_similarity_matcher

    SIMILARITY_AVAILABLE = True
except ImportError:
    SIMILARITY_AVAILABLE = False
    logger.warning(
        "Audio similarity matching not available. Install openl3 for this feature."
    )
