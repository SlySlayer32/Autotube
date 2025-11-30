# Audio Processing Pipeline

This guide explains the complete audio processing pipeline in SonicSleep Pro, from raw audio files to final mixes.

## Overview

The SonicSleep Pro audio processing pipeline consists of several stages that transform raw audio inputs into optimized sleep soundscapes:

```
Raw Audio Files → Preprocessing → Analysis → Submix Creation → Effect Application → Final Mix
```

## Pipeline Stages

### 1. Audio Input Sources

The pipeline begins with raw audio from various sources:

- **User-Provided Files**: WAV, MP3, or OGG files uploaded by users
- **External APIs**: Audio clips from Freesound or other audio services
- **Built-in Library**: Pre-packaged high-quality audio samples

### 2. Preprocessing (SoundProcessor)

Raw audio files undergo several preprocessing steps to standardize quality:

```python
from project_name.core.processor import SoundProcessor

processor = SoundProcessor(
    input_folder="raw_audio",
    processed_folder="processed_audio",
    sample_rate=44100,
    channels=2
)

# Process a single file
processed_file = processor.preprocess_audio("raw_audio/rain.wav")

# Batch process all files in input folder
processed_files = processor.process_batch()
```

This preprocessing includes:

- **Format Conversion**: Converting to a standard WAV format
- **Sample Rate Normalization**: Resampling to 44.1kHz or 48kHz
- **Channel Standardization**: Converting to stereo (2 channels)
- **Silence Removal**: Trimming silence from beginning and end
- **Noise Reduction**: Applying noise reduction algorithms
- **Normalization**: Adjusting levels to standard loudness

### 3. Audio Analysis

Processed audio undergoes analysis to extract features:

```python
# Analyze audio features
features = processor.analyze_audio_features(processed_file)

print(f"Duration: {features['duration']} seconds")
print(f"RMS Energy: {features['rms_energy']}")
print(f"Spectral Centroid: {features['spectral_centroid']} Hz")
print(f"Tempo: {features['tempo']} BPM")
```

Key analysis features include:

- **Duration**: Length of the audio file
- **RMS Energy**: Overall loudness
- **Spectral Centroid**: Brightness/darkness of sound
- **Spectral Bandwidth**: Frequency spread
- **Tempo**: Detected rhythmic pattern
- **Onsets**: Significant sound events
- **Emotional Valence**: Estimated emotional quality

### 4. Submix Creation (MixCreator)

Individual sound files are organized by category and mixed together:

```python
from project_name.core.mix_creator import MixCreator

mixer = MixCreator(output_folder="output_mixes")

# Organize processed files by category
audio_files = {
    "rain": [
        "processed_audio/light_rain.wav",
        "processed_audio/medium_rain.wav"
    ],
    "thunder": [
        "processed_audio/distant_thunder.wav"
    ],
    "white_noise": [
        "processed_audio/white_noise.wav"
    ]
}

# Create individual category submixes (internal process)
rain_mix = mixer._create_category_mix(
    audio_files["rain"],
    target_duration=60*60*1000,  # 60 minutes in milliseconds
    crossfade_duration=5000      # 5 seconds crossfade
)
```

The submix creation process includes:

- **Clip Selection**: Choosing appropriate clips from each category
- **Loop Creation**: Creating seamless loops for continuous playback
- **Crossfading**: Adding smooth transitions between clips
- **Duration Management**: Ensuring proper length for the mix

### 5. Effect Application

Audio effects are applied to each submix based on mix profiles:

```python
# Define the mix profile
sleep_profile = {
    "fade_in": 10000,       # 10 seconds fade in
    "fade_out": 10000,      # 10 seconds fade out
    "low_pass": 4000,       # Low-pass filter at 4000Hz
    "binaural_frequency": 2.5,  # 2.5Hz binaural beats (delta waves)
    "compression": {
        "threshold": -20,
        "ratio": 3.0
    }
}

# Apply effects to the mix (internal process)
processed_rain_mix = mixer._apply_mix_effects(rain_mix, sleep_profile)
```

Common effects include:

- **Equalization**: Adjusting frequency balance
- **Compression**: Controlling dynamic range
- **Filtering**: Low-pass, high-pass, or band-pass filters
- **Fade-ins/Fade-outs**: Gradual volume changes
- **Binaural Processing**: Adding brainwave entrainment frequencies
- **Spatial Enhancement**: Stereo field adjustments

### 6. Final Mix Assembly

Individual submixes are combined into the final output:

```python
# Create the complete mix
output_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=60,
    output_format="mp3",
    bitrate="192k"
)

print(f"Created mix: {output_path}")
```

The final assembly includes:

- **Volume Balancing**: Adjusting relative levels of submixes
- **Layering**: Combining multiple submixes
- **Timeline Construction**: Arranging sounds over time
- **Master Processing**: Final adjustments to the complete mix
- **Format Export**: Saving in the desired output format

## Customizing the Pipeline

### Custom Preprocessing

You can customize preprocessing parameters:

```python
# Create a processor with custom settings
custom_processor = SoundProcessor(
    input_folder="raw_audio",
    processed_folder="processed_audio",
    sample_rate=48000,       # Higher sample rate
    channels=2,
    bit_depth=24,            # Higher bit depth
    normalize_to_db=-1.5,    # Less headroom
    noise_reduction_level=0.2  # Lighter noise reduction
)
```

### Custom Effect Chains

You can define custom effect profiles:

```python
# Define a custom effect profile
focus_profile = {
    "fade_in": 5000,         # 5 seconds fade in
    "fade_out": 8000,        # 8 seconds fade out
    "band_pass": {
        "low_cutoff": 500,   # Remove frequencies below 500Hz
        "high_cutoff": 6000  # Remove frequencies above 6000Hz
    },
    "volume_adjustments": {
        "rain": -6,          # Rain 6dB quieter
        "cafe": 0,           # Cafe sounds at normal level
        "white_noise": -3    # White noise 3dB quieter
    }
}

# Apply custom profile
custom_mix = mixer.create_mix(
    audio_files=audio_files,
    mix_type="custom",
    mix_profile=focus_profile,
    duration_minutes=120
)
```

### Advanced Timeline Construction

For complex mixes with evolving elements:

```python
# This is a conceptual example - actual implementation may vary
from project_name.core.processor import TimelineBuilder

timeline = TimelineBuilder(duration_minutes=60)

# Add base layer for entire duration
timeline.add_layer(
    audio_file="processed_audio/white_noise.wav",
    start_time=0,
    end_time=60*60*1000,
    volume=-3
)

# Add rain that gradually increases
timeline.add_layer(
    audio_file="processed_audio/light_rain.wav",
    start_time=5*60*1000,    # Start at 5 minutes
    end_time=55*60*1000,     # End at 55 minutes
    volume_envelope={
        "type": "linear",
        "points": [
            (0, -10),         # Start at -10dB
            (15*60*1000, -3), # Reach -3dB at 15 minutes
            (40*60*1000, -3), # Stay at -3dB until 40 minutes
            (50*60*1000, -15) # Fade to -15dB by 50 minutes
        ]
    }
)

# Add occasional thunder
timeline.add_events(
    audio_file="processed_audio/distant_thunder.wav",
    times=[12*60*1000, 25*60*1000, 38*60*1000],  # At 12, 25, and 38 minutes
    volume=-8
)

# Render the timeline
output_path = timeline.render(
    output_format="mp3",
    bitrate="320k"
)
```

## Technical Details

### Audio Representation

SonicSleep Pro uses Pydub's AudioSegment objects internally, which provides a convenient interface for audio manipulation:

```python
from pydub import AudioSegment

# Load an audio file
audio = AudioSegment.from_file("processed_audio/rain.wav")

# Basic operations
louder_audio = audio + 3                # Increase volume by 3dB
first_half = audio[:len(audio)//2]      # Get first half
reversed_audio = audio.reverse()        # Reverse the audio
stereo_channels = audio.split_to_mono() # Split to individual channels
```

### Signal Processing

For more advanced signal processing, NumPy arrays are used:

```python
import numpy as np
from pydub.utils import get_array_type
import array

# Convert AudioSegment to numpy array
samples = np.array(audio.get_array_of_samples())

# If stereo, reshape to a 2D array
if audio.channels == 2:
    samples = samples.reshape((-1, 2))

# Process the samples (e.g., apply a gain envelope)
envelope = np.linspace(0.5, 1.0, len(samples))
modified_samples = samples * envelope[:, np.newaxis]

# Convert back to AudioSegment
modified_array = array.array(get_array_type(audio.sample_width), modified_samples.flatten())
modified_audio = AudioSegment(
    modified_array.tobytes(),
    frame_rate=audio.frame_rate,
    sample_width=audio.sample_width,
    channels=audio.channels
)
```

### Audio Format Support

The system supports the following formats:

- **Input Formats**: WAV, MP3, OGG, FLAC, AAC, M4A
- **Processing Format**: WAV (PCM)
- **Output Formats**: MP3, WAV, OGG, FLAC

```python
# Format conversion example
mp3_file = "input/music.mp3"
wav_file = processor.convert_format(mp3_file, "wav")
ogg_file = processor.convert_format(mp3_file, "ogg")
```

## Performance Considerations

### Memory Management

For long mixes or limited memory environments:

```python
# Process in chunks
processor.chunk_size_ms = 60000  # Process 60-second chunks

# Enable memory-efficient processing
mixer.memory_efficient = True
mixer.max_memory_mb = 512  # Limit memory usage
```

### Parallel Processing

For faster processing on multi-core systems:

```python
# Enable parallel processing
processor.use_parallel = True
processor.max_workers = 4  # Use 4 worker processes

# Batch process with parallel processing
processed_files = processor.process_batch(parallel=True)
```

## Troubleshooting

### Common Audio Problems

**Problem**: Clicks or pops in audio transitions
**Solution**: Increase crossfade duration or apply a fade envelope

**Problem**: Audio quality loss after processing
**Solution**: Use higher bitrates or lossless formats; increase sample rate

**Problem**: Background noise in quiet sections
**Solution**: Adjust noise reduction settings or apply a noise gate

**Problem**: Distortion in loud passages
**Solution**: Apply compression or limit maximum volume

**Problem**: Muddy sound quality
**Solution**: Adjust EQ to reduce low-mid frequencies and enhance clarity

## Next Steps

- Learn about [Visualization](visualization-guide.md) to see audio representations
- Explore [A/B Testing](ab-testing-guide.md) to systematically improve sound quality
- Check out [Creating Custom Mixes](creating-custom-mixes.md) for practical applications
