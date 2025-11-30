from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AudioAnalysisData:
    """Comprehensive audio analysis results"""

    # Basic properties
    duration: float
    sample_rate: int
    channels: int

    # Spectral features
    spectral_centroid: float
    spectral_rolloff: float
    spectral_bandwidth: float
    zero_crossing_rate: float

    # Energy and dynamics
    rms_energy: float
    dynamic_range: float
    loudness_lufs: float

    # Harmonic content
    harmonic_ratio: float
    noise_ratio: float
    pitch_stability: float

    # Rhythm and tempo
    tempo: Optional[float]
    rhythm_regularity: float
    beat_strength: float

    # Classification scores (0-1)
    sleep_induction_potential: float
    focus_enhancement_score: float
    relaxation_factor: float
    nature_sound_probability: float
    ambient_score: float

    # Mood and emotion
    valence: float  # positive/negative emotion
    arousal: float  # energy level
    dominance: float  # control/submissiveness

    # Advanced features
    binaural_compatibility: float
    masking_potential: float  # how well it masks other sounds
    loop_seamlessness: float  # how well it loops

    # ML predictions
    yamnet_predictions: List[tuple] = field(default_factory=list)
    mood_predictions: Dict[str, float] = field(default_factory=dict)
    similarity_embedding: Optional[List[float]] = None

    # Metadata
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    analysis_version: str = "1.0"


@dataclass
class AudioMetadata:
    """Complete metadata for an audio file"""

    file_path: Path
    file_hash: str
    basic_info: Dict[str, Any]
    analysis: Optional[AudioAnalysisData] = None
    user_tags: List[str] = field(default_factory=list)
    user_rating: Optional[float] = None
    processing_history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for storage"""
        return {
            "file_path": str(self.file_path),
            "file_hash": self.file_hash,
            "basic_info": self.basic_info,
            "analysis": self.analysis.__dict__ if self.analysis else None,
            "user_tags": self.user_tags,
            "user_rating": self.user_rating,
            "processing_history": self.processing_history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AudioMetadata":
        """Deserialize from dictionary"""
        analysis_data = data.get("analysis")
        analysis = AudioAnalysisData(**analysis_data) if analysis_data else None

        return cls(
            file_path=Path(data["file_path"]),
            file_hash=data["file_hash"],
            basic_info=data["basic_info"],
            analysis=analysis,
            user_tags=data.get("user_tags", []),
            user_rating=data.get("user_rating"),
            processing_history=data.get("processing_history", []),
        )
