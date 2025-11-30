"""Panel modules for SonicSleep Pro dashboard interface.

This package contains specialized panels for different functional areas of the application:
- input_panel: Audio input, search, and library management
- analysis_panel: Feature extraction, classification, and audio analysis
- audio_panel: Audio processing, effects, and manipulation
- therapeutic_panel: 2024 research-based therapeutic audio generation
- settings_panel: Application settings, presets, and preferences
"""

from .analysis_panel import AnalysisPanel
from .audio_panel import AudioProcessingPanel
from .input_panel import InputProcessingPanel
from .therapeutic_panel import TherapeuticAudioPanel
from .settings_panel import SettingsPanel
# Import the enhanced therapeutic panel
from ..enhanced_therapeutic_panel import EnhancedTherapeuticPanel
