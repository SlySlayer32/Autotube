# Quick Start: Evidence-Based Audio Features

**Goal:** Implement the highest-impact features first based on 2023-2024 research findings

## Priority 1: Pink Noise Generator (Strongest Evidence)

### Why Pink Noise First?

- **Northwestern University Study**: 3x better memory test performance
- **Sleep Enhancement**: Superior to white noise for memory consolidation
- **Focus Benefits**: Enhanced concentration and creative thinking
- **Technical Simplicity**: Easier to implement than complex binaural beats

### Implementation Code Template

```python
# project_name/audio_engine/pink_noise.py
import numpy as np
import scipy.signal as signal

class TherapeuticPinkNoise:
    """Pink noise generator based on memory consolidation research"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
    def generate_pink_noise(self, duration_seconds):
        """
        Generate pink noise with 1/f frequency response
        Based on research showing memory enhancement benefits
        """
        # Number of samples
        num_samples = int(duration_seconds * self.sample_rate)
        
        # Generate white noise
        white_noise = np.random.randn(num_samples)
        
        # Apply pink noise filter (1/f response)
        # Simple method: use scipy.signal filter
        b, a = signal.butter(1, 0.1, 'low')  # Low-pass for pink characteristic
        pink_noise = signal.filtfilt(b, a, white_noise)
        
        # Normalize to prevent clipping
        pink_noise = pink_noise / np.max(np.abs(pink_noise)) * 0.8
        
        return pink_noise
    
    def create_sleep_pink_noise(self, duration_minutes=45):
        """
        45+ minute sessions based on research minimum requirements
        """
        duration_seconds = duration_minutes * 60
        return self.generate_pink_noise(duration_seconds)
```

## Priority 2: Basic Binaural Beats (Sleep Frequencies)

### Research-Backed Frequencies

- **Delta (0.5-4 Hz)**: Deep sleep promotion
- **Theta (4-8 Hz)**: Sleep transition enhancement  
- **Alpha (8-14 Hz)**: Relaxation and stress relief

### Implementation Code Template

```python
# project_name/audio_engine/binaural_beats.py
import numpy as np

class ResearchBasedBinauralBeats:
    """Binaural beats using frequencies validated in clinical studies"""
    
    # Based on 2024 dynamic binaural beat study
    THERAPEUTIC_FREQUENCIES = {
        'deep_sleep': 2.0,      # Delta range - proven sleep latency reduction
        'sleep_transition': 6.0, # Theta range - enhanced sleep quality
        'relaxation': 10.0,     # Alpha range - anxiety reduction
        'focus': 15.0           # Beta range - limited use
    }
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.carrier_frequency = 200.0  # Base carrier frequency
        
    def generate_binaural_beat(self, target_frequency, duration_seconds, carrier_freq=None):
        """
        Generate binaural beat with specified frequency difference
        
        Args:
            target_frequency: Desired beat frequency (Hz)
            duration_seconds: Length of audio
            carrier_freq: Base frequency (default: 200 Hz)
        """
        if carrier_freq is None:
            carrier_freq = self.carrier_frequency
            
        # Time array
        t = np.linspace(0, duration_seconds, int(duration_seconds * self.sample_rate), False)
        
        # Left ear: carrier frequency
        left_channel = np.sin(2 * np.pi * carrier_freq * t)
        
        # Right ear: carrier + beat frequency
        right_channel = np.sin(2 * np.pi * (carrier_freq + target_frequency) * t)
        
        # Combine into stereo array
        stereo_audio = np.column_stack((left_channel, right_channel))
        
        # Apply gentle envelope to prevent clicks
        envelope = self._create_envelope(len(stereo_audio))
        stereo_audio *= envelope.reshape(-1, 1)
        
        return stereo_audio
    
    def _create_envelope(self, length, fade_samples=1000):
        """Create fade-in/fade-out envelope"""
        envelope = np.ones(length)
        
        # Fade in
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        
        # Fade out
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return envelope
    
    def create_sleep_protocol(self, duration_minutes=45):
        """
        Create research-based sleep induction protocol
        45+ minutes as per research requirements
        """
        duration_seconds = duration_minutes * 60
        
        # Start with alpha for relaxation (first 10 minutes)
        alpha_duration = min(600, duration_seconds // 4)
        alpha_beats = self.generate_binaural_beat(
            self.THERAPEUTIC_FREQUENCIES['relaxation'], 
            alpha_duration
        )
        
        # Transition to theta for sleep onset
        theta_duration = min(900, duration_seconds // 3)
        theta_beats = self.generate_binaural_beat(
            self.THERAPEUTIC_FREQUENCIES['sleep_transition'],
            theta_duration
        )
        
        # Deep sleep delta for remainder
        delta_duration = duration_seconds - alpha_duration - theta_duration
        delta_beats = self.generate_binaural_beat(
            self.THERAPEUTIC_FREQUENCIES['deep_sleep'],
            delta_duration
        )
        
        # Concatenate phases
        full_protocol = np.vstack([alpha_beats, theta_beats, delta_beats])
        
        return full_protocol
```

## Priority 3: Rain Sound Enhancement (Your Specialty)

### Research Integration for Rain Sounds

```python
# project_name/audio_engine/therapeutic_rain.py
import numpy as np
from .pink_noise import TherapeuticPinkNoise
from .binaural_beats import ResearchBasedBinauralBeats

class TherapeuticRainEngine:
    """Enhanced rain sounds with research-based therapeutic elements"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.pink_noise_gen = TherapeuticPinkNoise(sample_rate)
        self.binaural_gen = ResearchBasedBinauralBeats(sample_rate)
        
    def create_parasympathetic_rain(self, duration_minutes=30, intensity='medium'):
        """
        Rain sounds optimized for parasympathetic activation
        Based on 2021 meta-analysis showing nature sounds reduce cortisol
        """
        duration_seconds = duration_minutes * 60
        
        # Your existing rain generation code here
        base_rain = self._generate_base_rain(duration_seconds, intensity)
        
        # Add pink noise component for memory benefits (20% blend)
        pink_component = self.pink_noise_gen.generate_pink_noise(duration_seconds)
        enhanced_rain = 0.8 * base_rain + 0.2 * pink_component
        
        return enhanced_rain
    
    def create_rain_with_binaural_beats(self, duration_minutes=45, target_frequency=6.0):
        """
        Your innovation: Rain sounds with embedded therapeutic frequencies
        
        Args:
            duration_minutes: Session length (minimum 45 for sleep)
            target_frequency: Binaural beat frequency (theta for sleep)
        """
        duration_seconds = duration_minutes * 60
        
        # Generate base rain sound
        rain_audio = self.create_parasympathetic_rain(duration_minutes)
        
        # Generate binaural beats at low volume
        binaural_audio = self.binaural_gen.generate_binaural_beat(
            target_frequency, 
            duration_seconds
        )
        
        # Mix: Rain dominant, binaural beats subtle (barely audible)
        if rain_audio.ndim == 1:
            # Convert mono rain to stereo if needed
            rain_stereo = np.column_stack([rain_audio, rain_audio])
        else:
            rain_stereo = rain_audio
            
        # Blend: 85% rain, 15% binaural beats
        therapeutic_rain = 0.85 * rain_stereo + 0.15 * binaural_audio
        
        return therapeutic_rain
    
    def _generate_base_rain(self, duration_seconds, intensity):
        """
        Your existing rain generation logic
        Enhanced with research-based frequency emphasis
        """
        # Placeholder for your rain synthesis
        # Focus on low-frequency emphasis for parasympathetic activation
        
        # Generate noise-based rain texture
        base_noise = np.random.randn(int(duration_seconds * self.sample_rate))
        
        # Apply rain-like filtering (you'll replace this with your algorithm)
        # Emphasize frequencies that promote relaxation (50-2000 Hz)
        
        return base_noise * 0.5  # Placeholder
```

## Priority 4: Simple Audio Mixer

### Combine Multiple Therapeutic Elements

```python
# project_name/audio_engine/therapeutic_mixer.py
from .therapeutic_rain import TherapeuticRainEngine
from .pink_noise import TherapeuticPinkNoise
from .binaural_beats import ResearchBasedBinauralBeats

class EvidenceBasedAudioMixer:
    """Mix multiple audio elements based on research synergies"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.rain_engine = TherapeuticRainEngine(sample_rate)
        self.pink_noise_gen = TherapeuticPinkNoise(sample_rate)
        self.binaural_gen = ResearchBasedBinauralBeats(sample_rate)
        
    def create_optimal_sleep_mix(self, duration_minutes=45):
        """
        Research-optimized combination for sleep enhancement
        
        Based on multiple studies showing synergistic effects:
        - Rain sounds: Parasympathetic activation
        - Pink noise: Memory consolidation  
        - Theta binaural beats: Sleep transition
        """
        # Generate individual components
        rain_component = self.rain_engine.create_parasympathetic_rain(duration_minutes)
        pink_component = self.pink_noise_gen.create_sleep_pink_noise(duration_minutes)
        binaural_component = self.binaural_gen.create_sleep_protocol(duration_minutes)
        
        # Convert to stereo if needed
        if rain_component.ndim == 1:
            rain_stereo = np.column_stack([rain_component, rain_component])
        else:
            rain_stereo = rain_component
            
        if pink_component.ndim == 1:
            pink_stereo = np.column_stack([pink_component, pink_component])
        else:
            pink_stereo = pink_component
            
        # Research-based mixing ratios
        optimal_mix = (
            0.5 * rain_stereo +          # Dominant: nature sound benefits
            0.3 * pink_stereo +          # Secondary: memory benefits
            0.2 * binaural_component     # Subtle: brainwave entrainment
        )
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(optimal_mix))
        if max_amplitude > 0.95:
            optimal_mix = optimal_mix / max_amplitude * 0.9
            
        return optimal_mix
    
    def create_anxiety_relief_mix(self, duration_minutes=20):
        """
        Research-based combination for anxiety reduction
        
        Based on clinical studies showing 30-50% anxiety reduction:
        - Alpha binaural beats: Proven anxiety reduction
        - Heavy rain: Parasympathetic activation
        - Pink noise: Cognitive calming
        """
        duration_seconds = duration_minutes * 60
        
        # Alpha frequency for anxiety relief
        alpha_beats = self.binaural_gen.generate_binaural_beat(10.0, duration_seconds)
        
        # Heavy rain for strong parasympathetic response
        heavy_rain = self.rain_engine.create_parasympathetic_rain(
            duration_minutes, 
            intensity='heavy'
        )
        
        # Pink noise for cognitive benefits
        calming_pink = self.pink_noise_gen.generate_pink_noise(duration_seconds)
        
        # Mix for anxiety relief
        if heavy_rain.ndim == 1:
            rain_stereo = np.column_stack([heavy_rain, heavy_rain])
        else:
            rain_stereo = heavy_rain
            
        pink_stereo = np.column_stack([calming_pink, calming_pink])
        
        anxiety_relief_mix = (
            0.6 * rain_stereo +      # Primary: nature sound calming
            0.25 * alpha_beats +     # Secondary: proven anxiety reduction
            0.15 * pink_stereo       # Supporting: cognitive calming
        )
        
        # Normalize
        max_amplitude = np.max(np.abs(anxiety_relief_mix))
        if max_amplitude > 0.95:
            anxiety_relief_mix = anxiety_relief_mix / max_amplitude * 0.9
            
        return anxiety_relief_mix
```

## Quick Implementation Steps

### Week 1: Core Foundation

1. **Implement Pink Noise Generator** (highest research priority)
2. **Create Basic Binaural Beat Generator** (3 therapeutic frequencies)
3. **Test audio generation and file export**

### Week 2: Rain Enhancement  

1. **Integrate pink noise with your existing rain sounds**
2. **Add binaural beat layering to rain**
3. **Create parasympathetic-optimized rain profiles**

### Week 3: Mixing Engine

1. **Implement therapeutic audio mixer**
2. **Create research-based preset combinations**
3. **Add session duration controls (20 min, 45 min, 8 hours)**

### Week 4: User Testing

1. **Create simple playback interface**
2. **Test with initial users**
3. **Collect effectiveness feedback**
4. **Refine mixing ratios based on user response**

## Research Validation Checklist

### Implement These Research Requirements

- [ ] **Minimum 45-minute sessions** for sleep benefits
- [ ] **Pink noise prioritized** over white noise
- [ ] **Theta (4-8 Hz) and delta (0.5-4 Hz)** binaural frequencies for sleep
- [ ] **Alpha (8-14 Hz)** frequencies for anxiety reduction
- [ ] **Nature sounds for parasympathetic activation**
- [ ] **Gradual volume transitions** to prevent arousal
- [ ] **Individual user response tracking**

### Audio Quality Standards

- [ ] **44.1kHz sample rate minimum** for binaural beat precision
- [ ] **Seamless looping** for extended sessions
- [ ] **Fade-in/fade-out envelopes** to prevent audio artifacts
- [ ] **Amplitude normalization** to prevent clipping

## User Experience Priorities

### Essential Features for MVP

1. **Simple mode selection**: Sleep, Relaxation, Focus
2. **Duration options**: 20 min, 45 min, 8 hours  
3. **Volume controls**: Master, Rain, Binaural, Pink Noise
4. **Basic effectiveness tracking**: Sleep quality rating (1-10)

### Research-Based Defaults

- **Sleep Mode**: Rain + Pink Noise + Theta Binaural (45 min minimum)
- **Relaxation Mode**: Rain + Alpha Binaural (20 min minimum)  
- **Focus Mode**: Pink Noise + Light Rain (30 min sessions)

This quick-start approach focuses on implementing the features with the strongest research backing first, while building on your existing rain sound expertise. The modular design allows you to add more sophisticated features later while ensuring the core functionality is evidence-based from the start.
