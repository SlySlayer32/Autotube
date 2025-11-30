"""
Space-Efficient Content Gatherer

Optimized version that creates smaller files and uses intelligent storage.
"""

import logging
import json
import numpy as np
from pathlib import Path
import soundfile as sf

logger = logging.getLogger(__name__)


class EfficientBinauralGenerator:
    """Generate space-efficient binaural beats with smart looping."""
    
    def __init__(self, library_path: str = "audio_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(exist_ok=True)
        
    def generate_efficient_binaural_library(self):
        """Generate space-efficient binaural beat library."""
        logger.info("🎵 Generating SPACE-EFFICIENT binaural beat library...")
        
        binaural_path = self.library_path / "binaural_beats"
        binaural_path.mkdir(exist_ok=True)
        
        # SPACE-EFFICIENT APPROACH:
        # Create SHORT (60 second) perfect loops instead of long files
        # Total library size: ~20MB instead of 20GB!
        
        beat_frequencies = {
            'delta_sleep': [1.0, 2.0, 3.0],        # 3 files × ~10MB = 30MB
            'theta_rem': [5.0, 6.0, 7.0],          # 3 files × ~10MB = 30MB  
            'alpha_relax': [9.0, 10.0, 11.0],      # 3 files × ~10MB = 30MB
            'beta_focus': [15.0, 20.0, 25.0]       # 3 files × ~10MB = 30MB
        }
        
        base_frequency = 440  # Single frequency saves space
        duration = 60  # 60 seconds = ~10MB per file
        
        total_files = sum(len(freqs) for freqs in beat_frequencies.values())
        estimated_size = total_files * 10  # MB
        
        logger.info(f"📊 Creating {total_files} files (~{estimated_size}MB total)")
        logger.info(f"🔄 Each file: {duration}s perfect loops")
        
        for state, beat_freqs in beat_frequencies.items():
            state_path = binaural_path / state
            state_path.mkdir(exist_ok=True)
            
            for beat_freq in beat_freqs:
                self._generate_perfect_loop(base_frequency, beat_freq, state_path, duration)
        
        logger.info("✅ Space-efficient binaural library complete!")
        self._show_library_stats()
    
    def _generate_perfect_loop(self, base_freq: float, beat_freq: float, 
                              output_path: Path, duration: int = 60):
        """Generate a perfect-looping binaural beat."""
        try:
            filename = f"binaural_{base_freq}Hz_beat_{beat_freq}Hz_{duration}s.wav"
            file_path = output_path / filename
            
            if file_path.exists():
                logger.info(f"⏭️ Skipping existing: {filename}")
                return
                
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            
            # Generate left and right channels
            left_freq = base_freq
            right_freq = base_freq + beat_freq
            
            # Use lower amplitude to save space and prevent clipping
            amplitude = 0.2
            left_channel = amplitude * np.sin(2 * np.pi * left_freq * t)
            right_channel = amplitude * np.sin(2 * np.pi * right_freq * t)
            
            # PERFECT LOOP: Ensure phase alignment at loop points
            # This is crucial for seamless looping!
            loop_samples = len(left_channel)
            
            # Adjust to exact cycle boundaries for perfect looping
            left_cycles = int(left_freq * duration)
            right_cycles = int(right_freq * duration)
            
            # Recalculate time array for exact cycles
            actual_duration = max(left_cycles / left_freq, right_cycles / right_freq)
            t_exact = np.linspace(0, actual_duration, int(sample_rate * actual_duration), endpoint=False)
            
            left_channel = amplitude * np.sin(2 * np.pi * left_freq * t_exact)
            right_channel = amplitude * np.sin(2 * np.pi * right_freq * t_exact)
            
            # Add subtle fade to avoid any clicks (very short)
            fade_samples = int(sample_rate * 0.01)  # 10ms fade
            if len(left_channel) > fade_samples * 2:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                
                left_channel[:fade_samples] *= fade_in
                left_channel[-fade_samples:] *= fade_out
                right_channel[:fade_samples] *= fade_in
                right_channel[-fade_samples:] *= fade_out
            
            # Combine channels
            stereo_audio = np.column_stack((left_channel, right_channel))
            
            # Save with efficient settings
            sf.write(str(file_path), stereo_audio, sample_rate, 
                    subtype='PCM_16')  # 16-bit instead of 32-bit saves 50% space
            
            # Calculate actual file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            logger.info(f"✅ Generated: {filename} ({file_size_mb:.1f}MB)")
            
            # Save metadata
            metadata = {
                'type': 'binaural_beat',
                'base_frequency': base_freq,
                'beat_frequency': beat_freq,
                'duration': float(actual_duration),
                'sample_rate': sample_rate,
                'purpose': self._get_binaural_purpose(beat_freq),
                'loop_perfect': True,
                'file_size_mb': file_size_mb,
                'space_efficient': True
            }
            
            metadata_path = file_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Error generating {base_freq}Hz/{beat_freq}Hz: {e}")
    
    def _get_binaural_purpose(self, beat_freq: float) -> str:
        """Get the purpose/effect of a binaural beat frequency."""
        if beat_freq <= 4:
            return "deep_sleep"
        elif beat_freq <= 8:
            return "rem_sleep_creativity"
        elif beat_freq <= 12:
            return "relaxation_meditation"
        elif beat_freq <= 30:
            return "focus_concentration"
        else:
            return "high_alertness"
    
    def _show_library_stats(self):
        """Show library statistics."""
        binaural_path = self.library_path / "binaural_beats"
        
        if not binaural_path.exists():
            return
            
        total_size = 0
        file_count = 0
        
        for wav_file in binaural_path.rglob("*.wav"):
            total_size += wav_file.stat().st_size
            file_count += 1
        
        total_size_mb = total_size / (1024 * 1024)
        
        logger.info("📊 LIBRARY STATISTICS:")
        logger.info(f"   Files: {file_count}")
        logger.info(f"   Total Size: {total_size_mb:.1f}MB")
        logger.info(f"   Average per file: {total_size_mb/max(1, file_count):.1f}MB")
        logger.info(f"   🎉 Space saved vs 1-hour files: ~{(file_count * 635) - total_size_mb:.0f}MB!")


def create_smart_content_strategy():
    """
    Smart content strategy that balances quality and storage efficiency.
    """
    print("🧠 SMART CONTENT STRATEGY")
    print("=" * 50)
    
    strategies = {
        "🔄 Perfect Short Loops": {
            "approach": "60-second perfect loops that can repeat seamlessly",
            "space": "~10MB per file",
            "benefit": "Infinite playback from small files",
            "use_case": "Background ambience, binaural beats"
        },
        
        "✂️ Intelligent Clipping": {
            "approach": "Extract best segments from long recordings",
            "space": "Variable, but removes dead space",
            "benefit": "High-quality content, no filler",
            "use_case": "Rain loops, thunder claps, nature sounds"
        },
        
        "🧬 Procedural Generation": {
            "approach": "Generate variations algorithmically",
            "space": "Minimal - store parameters, not audio",
            "benefit": "Unlimited variety from small data",
            "use_case": "Binaural beats, ambient textures"
        },
        
        "📦 Compressed Originals": {
            "approach": "Keep originals compressed, decompress on use",
            "space": "~90% reduction with FLAC",
            "benefit": "High quality when needed",
            "use_case": "Master recordings, rarely-used content"
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n{strategy}")
        for key, value in details.items():
            print(f"  {key.title()}: {value}")
    
    print(f"\n💡 RECOMMENDATION:")
    print(f"  1. Generate 60s binaural loops (~120MB total)")
    print(f"  2. Use intelligent clipping for nature sounds")
    print(f"  3. Store user uploads compressed until needed")
    print(f"  4. Generate variations programmatically")


if __name__ == "__main__":
    # Show the strategy
    create_smart_content_strategy()
    
    print("\n" + "=" * 50)
    
    # Generate efficient library
    generator = EfficientBinauralGenerator()
    generator.generate_efficient_binaural_library()
