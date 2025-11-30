import hashlib
import json
from datetime import datetime

# import soundfile as sf # Not used directly in the provided snippet, but good for future
from pathlib import Path
from typing import Any, Dict, List, Optional

import librosa
import numpy as np

# Placeholder for YAMNetClassifier
# from ..api.yamnet_classifier import YAMNetClassifier
from ..api.yamnet_api import YAMNetAPI

# Placeholder for EnhancedSoundProcessor - will use SoundProcessor for now or mock
# from .enhanced_processor import EnhancedSoundProcessor
from ..core.processor import SoundProcessor  # Using existing processor for now
from .audio_metadata import AudioAnalysisData, AudioMetadata


class AudioAnalysisPipeline:
    """Comprehensive audio analysis pipeline"""

    def __init__(self):
        # self.processor = EnhancedSoundProcessor() # Placeholder
        self.processor = SoundProcessor()  # Using existing processor for some features
        self.yamnet_api: Optional[YAMNetAPI] = None
        try:
            self.yamnet_api = YAMNetAPI()
        except RuntimeError as e:
            # Logger might not be configured here yet if this is top-level script execution
            # For now, print a warning. If used as part of a larger app, logger would be available.
            print(
                f"Warning: YAMNetAPI initialization failed: {e}. YAMNet predictions will be unavailable."
            )
        except ImportError as e:
            print(
                f"Warning: TensorFlow or TensorFlow Hub not installed. YAMNet predictions will be unavailable: {e}"
            )

        # self.classifier = YAMNetClassifier() # Placeholder
        self.cache_dir = Path("data/analysis_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def analyze_audio_file(
        self, file_path: Path, force_reanalysis: bool = False
    ) -> AudioMetadata:
        """Perform comprehensive analysis of audio file"""
        file_hash = self._calculate_file_hash(file_path)
        cache_path = self.cache_dir / f"{file_hash}.json"

        # Check cache first
        if not force_reanalysis and cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    cached_data = json.load(f)
                # Need to handle datetime deserialization if it's stored as string
                if (
                    cached_data.get("analysis")
                    and "analysis_timestamp" in cached_data["analysis"]
                ):
                    cached_data["analysis"]["analysis_timestamp"] = (
                        datetime.fromisoformat(
                            cached_data["analysis"]["analysis_timestamp"]
                        )
                    )
                return AudioMetadata.from_dict(cached_data)
            except Exception:
                # logger.error(f"Error loading from cache: {e}. Re-analyzing.") # Requires logger setup
                pass  # Fall through to reanalysis

        # Perform analysis
        metadata = self._perform_full_analysis(file_path, file_hash)

        # Cache results
        with open(cache_path, "w") as f:
            # Ensure datetime is stored in ISO format
            dict_to_save = metadata.to_dict()
            if dict_to_save.get("analysis") and isinstance(
                dict_to_save["analysis"]["analysis_timestamp"], datetime
            ):
                dict_to_save["analysis"]["analysis_timestamp"] = dict_to_save[
                    "analysis"
                ]["analysis_timestamp"].isoformat()
            json.dump(dict_to_save, f, indent=2)

        return metadata

    def _perform_full_analysis(self, file_path: Path, file_hash: str) -> AudioMetadata:
        """Perform complete audio analysis"""
        y, sr = librosa.load(file_path, sr=None)  # Load with native sample rate

        basic_info = {
            "duration": librosa.get_duration(y=y, sr=sr),
            "sample_rate": sr,
            "channels": y.ndim,  # 1 for mono, 2 for stereo (librosa loads mono by default)
            "file_size": file_path.stat().st_size,
        }
        if y.ndim == 1:  # Ensure librosa's default mono loading is reflected
            basic_info["channels"] = 1

        # Use existing SoundProcessor methods where applicable
        # Note: SoundProcessor methods might expect file paths or different y, sr. Adapt as needed.
        # For now, let's call the feature extraction methods from SoundProcessor if they exist and are suitable
        # This part needs careful integration or duplication/adaptation of logic from SoundProcessor

        # Placeholder calls for features that would come from SoundProcessor or new methods
        # This assumes SoundProcessor's methods can be adapted or new ones are created here.
        sp_features = self.processor._extract_audio_features(
            y, sr
        )  # Basic spectral/tempo
        sp_psycho_features = self.processor.extract_psychoacoustic_features(y, sr)
        sp_temporal_features = self.processor.analyze_temporal_patterns(y, sr)

        analysis_data_args = {
            "duration": basic_info["duration"],
            "sample_rate": sr,
            "channels": basic_info["channels"],
            "spectral_centroid": sp_features.get("spectral_centroid", 0.0),
            "spectral_rolloff": sp_features.get("spectral_rolloff", 0.0),
            "spectral_bandwidth": sp_features.get("spectral_bandwidth", 0.0),
            "zero_crossing_rate": sp_features.get("zero_crossing_rate", 0.0),
            "rms_energy": sp_features.get(
                "loudness", 0.0
            ),  # Map loudness to rms_energy
            "dynamic_range": self._calculate_dynamic_range(y),  # Placeholder
            "loudness_lufs": self._calculate_loudness_lufs(y, sr),  # Placeholder
            "harmonic_ratio": self._extract_harmonic_features(y, sr).get(
                "harmonic_ratio", 0.0
            ),
            "noise_ratio": self._extract_harmonic_features(y, sr).get(
                "noise_ratio", 0.0
            ),
            "pitch_stability": self._extract_harmonic_features(y, sr).get(
                "pitch_stability", 0.0
            ),
            "tempo": sp_temporal_features.get("tempo"),
            "rhythm_regularity": sp_temporal_features.get(
                "cadence_regularity", 0.0
            ),  # Map
            "beat_strength": self._extract_rhythm_features(y, sr).get(
                "beat_strength", 0.0
            ),
            "sleep_induction_potential": self._calculate_sleep_metrics(y, sr).get(
                "sleep_induction_potential", 0.0
            ),
            "focus_enhancement_score": self._calculate_sleep_metrics(y, sr).get(
                "focus_enhancement_score", 0.0
            ),
            "relaxation_factor": self._calculate_sleep_metrics(y, sr).get(
                "relaxation_factor", 0.0
            ),
            "nature_sound_probability": self._calculate_advanced_features(y, sr).get(
                "nature_sound_probability", 0.0
            ),
            "ambient_score": self._calculate_advanced_features(y, sr).get(
                "ambient_score", 0.0
            ),
            "valence": self._extract_mood_features(y, sr).get("valence", 0.0),
            "arousal": self._extract_mood_features(y, sr).get("arousal", 0.0),
            "dominance": self._extract_mood_features(y, sr).get("dominance", 0.0),
            "binaural_compatibility": self._calculate_advanced_features(y, sr).get(
                "binaural_compatibility", 0.0
            ),
            "masking_potential": self._calculate_advanced_features(y, sr).get(
                "masking_potential", 0.0
            ),
            "loop_seamlessness": self._calculate_advanced_features(y, sr).get(
                "loop_seamlessness", 0.0
            ),
            "yamnet_predictions": self.yamnet_api.predict(file_path)
            if self.yamnet_api
            else [],
            "mood_predictions": self._extract_mood_features(y, sr).get(
                "mood_predictions", {}
            ),  # Placeholder
            "similarity_embedding": self._get_audio_embedding(y, sr),  # Placeholder
            "analysis_timestamp": datetime.now(),
            "analysis_version": "1.0.0-alpha",  # More specific version
        }
        analysis = AudioAnalysisData(**analysis_data_args)

        return AudioMetadata(
            file_path=file_path,
            file_hash=file_hash,
            basic_info=basic_info,
            analysis=analysis,
        )

    def _calculate_dynamic_range(self, y: np.ndarray) -> float:
        # Placeholder: A proper implementation would use LUFS or peak-to-RMS
        rms = librosa.feature.rms(y=y)[0]
        if len(rms) == 0 or np.max(rms) == 0:
            return 0.0
        peak_rms = np.max(rms)
        avg_rms = np.mean(rms)
        if avg_rms == 0:
            return 0.0
        dr = 20 * np.log10(peak_rms / avg_rms) if peak_rms > 0 and avg_rms > 0 else 0.0
        return float(dr)

    def _calculate_loudness_lufs(self, y: np.ndarray, sr: int) -> float:
        # Placeholder: LUFS calculation is complex, typically uses specialized libraries like pyloudnorm
        # This is a very rough approximation using RMS energy
        rms_energy = np.mean(librosa.feature.rms(y=y))
        # Rough conversion: 0 dBFS RMS sine wave is about -3 LUFS. This isn't accurate.
        return float(
            20 * np.log10(rms_energy + 1e-8) - 3.0 if rms_energy > 0 else -70.0
        )

    def _extract_spectral_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # This method is defined in the user's prompt, but we'll ensure it's here.
        # It's also part of SoundProcessor._extract_audio_features
        # For consistency, we can call SoundProcessor's method or reimplement.
        # Re-implementing for clarity of what AudioAnalysisPipeline itself does.
        features = self.processor._extract_audio_features(y, sr)
        return {
            "spectral_centroid": features.get("spectral_centroid", 0.0),
            "spectral_rolloff": features.get("spectral_rolloff", 0.0),
            "spectral_bandwidth": features.get("spectral_bandwidth", 0.0),
            "zero_crossing_rate": features.get("zero_crossing_rate", 0.0),
        }

    def _extract_energy_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # Placeholder for more detailed energy features
        rms = np.mean(librosa.feature.rms(y=y))
        return {"rms_energy": float(rms)}  # Already covered by sp_features['loudness']

    def _extract_harmonic_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # Placeholder
        h, p = librosa.effects.hpss(y)
        harmonic_ratio = (
            np.sum(h**2) / (np.sum(p**2) + 1e-8) if np.sum(p**2) > 0 else 0.0
        )
        return {
            "harmonic_ratio": float(harmonic_ratio),
            "noise_ratio": 1.0 - float(harmonic_ratio)
            if harmonic_ratio <= 1
            else 0.0,  # Simplified
            "pitch_stability": 0.0,  # Requires pitch tracking
        }

    def _extract_rhythm_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # Placeholder, some covered by SoundProcessor.analyze_temporal_patterns
        sp_temporal = self.processor.analyze_temporal_patterns(y, sr)
        return {
            "tempo": sp_temporal.get("tempo"),
            "rhythm_regularity": sp_temporal.get("cadence_regularity", 0.0),
            "beat_strength": 0.0,  # Requires beat analysis
        }

    def _calculate_sleep_metrics(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # This is a simplified version of the user's example.
        # It should be expanded based on the detailed logic provided in the prompt.
        # For now, using SoundProcessor's analyze_sleep_quality as a base
        # This method expects a file_path, so we'd need to save 'y' to a temp file or adapt.
        # Simplified for now:
        sp_sleep_metrics = self.processor.analyze_sleep_quality_from_data(
            y, sr
        )  # Assuming this method exists or is added

        return {
            "sleep_induction_potential": sp_sleep_metrics.get(
                "sleep_induction_potential", 0.0
            ),
            "focus_enhancement_score": self._calculate_focus_score(y, sr),
            "relaxation_factor": self._calculate_relaxation_score(y, sr),
        }

    def _calculate_focus_score(self, y: np.ndarray, sr: int) -> float:
        # Placeholder - e.g., moderate complexity, stable rhythm, not too distracting
        # Example: mid-range spectral centroid, moderate flatness, stable tempo
        sc = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        sc_score = 0.0
        if 1500 < sc < 3000:
            sc_score = 1.0  # Optimal for focus
        elif 1000 < sc < 3500:
            sc_score = 0.5

        flatness_score = 0.0
        if 0.2 < flatness < 0.6:
            flatness_score = 1.0  # Not too tonal, not too noisy

        tempo_score = 0.0
        if tempo is not None and 70 < tempo < 120:
            tempo_score = 1.0  # Typical focus tempo

        return float(np.mean([sc_score, flatness_score, tempo_score]))

    def _calculate_relaxation_score(self, y: np.ndarray, sr: int) -> float:
        # Placeholder - e.g., low spectral centroid, high tonalness, slow tempo
        # Similar to sleep_induction_potential but perhaps different weights
        sp_psycho = self.processor.extract_psychoacoustic_features(y, sr)
        return float(
            sp_psycho.get("relaxation_score", 0.0) / 10.0
        )  # Normalize if score is not 0-1

    def _extract_mood_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        # Placeholder - complex, often requires ML models
        return {
            "valence": 0.5,
            "arousal": 0.5,
            "dominance": 0.5,  # Neutral defaults
            "mood_predictions": {},
        }

    def _calculate_advanced_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # Placeholder
        return {
            "nature_sound_probability": 0.0,
            "ambient_score": 0.0,
            "binaural_compatibility": 0.0,  # e.g. if stereo and suitable for binaural overlay
            "masking_potential": 0.0,
            "loop_seamlessness": 0.0,
        }

    def _get_audio_embedding(self, y: np.ndarray, sr: int) -> Optional[List[float]]:
        # Placeholder - requires an embedding model (e.g., OpenL3)
        return None

    def _calculate_file_hash(self, file_path: Path) -> str:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


# Add a helper to SoundProcessor for direct data analysis if not present
# This is a conceptual addition; actual modification to SoundProcessor would be separate.
if not hasattr(SoundProcessor, "analyze_sleep_quality_from_data"):

    def analyze_sleep_quality_from_data(
        self_sp, y: np.ndarray, sr: int
    ) -> Dict[str, float]:
        # This is a simplified adaptation. SoundProcessor's original method uses a file path.
        # For a real implementation, adapt the logic of analyze_sleep_quality to work with y, sr.
        # Here, we'll just return placeholder values.
        # This avoids modifying SoundProcessor directly in this step but highlights the need.
        # Ideally, SoundProcessor's methods would be refactored to accept y, sr.

        # Re-using parts of SoundProcessor's logic conceptually
        features = self_sp._extract_audio_features(y, sr)
        psycho_features = self_sp.extract_psychoacoustic_features(y, sr)
        temporal_features = self_sp.analyze_temporal_patterns(y, sr)

        frequency_score = (
            1.0 - min(1.0, features.get("spectral_centroid", 2000) / 4000)
        ) * 0.5 + max(
            0.0,
            psycho_features.get("low_energy", 0)
            - psycho_features.get("very_high_energy", 0),
        ) * 0.5
        consistency_score = (
            temporal_features.get("evenness", 0) * 0.4
            + (
                1.0
                - abs(0.7 - temporal_features.get("repetitiveness_score", 0.7)) / 0.7
            )
            * 0.3
            + (1.0 - features.get("zero_crossing_rate", 0) * 20) * 0.3
        )
        naturalness_score = (
            temporal_features.get("naturalness_score", 0) * 0.5
            + psycho_features.get("relaxation_score", 0) * 0.5
        )
        sleep_induction_potential = (
            frequency_score * 0.4 + consistency_score * 0.4 + naturalness_score * 0.2
        )
        sleep_induction_potential = max(
            0, min(10, sleep_induction_potential * 10)
        )  # Original scaling

        return {
            "frequency_score": float(frequency_score),
            "consistency_score": float(consistency_score),
            "naturalness_score": float(naturalness_score),
            "sleep_induction_potential": float(
                sleep_induction_potential / 10.0
            ),  # Normalize to 0-1 for AudioAnalysisData
        }

    SoundProcessor.analyze_sleep_quality_from_data = analyze_sleep_quality_from_data
