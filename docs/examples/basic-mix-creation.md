# Basic Mix Creation Example

This example demonstrates how to create a basic sleep mix using the SonicSleep Pro API.

## Overview

In this example, we'll:

1. Process raw audio files
2. Create a basic sleep mix
3. Preview the mix
4. Save the final result

## Complete Example

```python
"""
Basic Mix Creation Example for SonicSleep Pro

This script demonstrates the core workflow for creating sleep mixes,
from audio processing to final mix generation.
"""

import os
from pathlib import Path
from pydub import AudioSegment
from project_name.core.processor import SoundProcessor
from project_name.core.mix_creator import MixCreator
from project_name.core.visualizer import AudioVisualizer

def main():
    # Set up directories
    input_dir = "input_clips"
    processed_dir = "processed_clips"
    output_dir = "output_mixes"
    viz_dir = "visualizations"
    
    for directory in [input_dir, processed_dir, output_dir, viz_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Step 1: Initialize components
    processor = SoundProcessor(
        input_folder=input_dir,
        processed_folder=processed_dir
    )
    
    mixer = MixCreator(
        output_folder=output_dir
    )
    
    visualizer = AudioVisualizer(
        output_folder=viz_dir
    )
    
    # Step 2: Process audio files (will use existing processed files if available)
    print("Processing audio files...")
    processed_files = processor.process_batch()
    
    if not processed_files:
        print("No audio files found for processing. Check your input_clips directory.")
        return
    
    print(f"Processed {len(processed_files)} audio files.")
    
    # Step 3: Categorize audio files based on filename
    audio_files = {
        "rain": [f for f in processed_files if "rain" in f.lower()],
        "thunder": [f for f in processed_files if "thunder" in f.lower()]
    }
    
    # Add any other files to a generic "ambient" category
    used_files = set([f for files in audio_files.values() for f in files])
    remaining_files = [f for f in processed_files if f not in used_files]
    if remaining_files:
        audio_files["ambient"] = remaining_files
    
    # Print what we're working with
    print("\nAudio files by category:")
    for category, files in audio_files.items():
        print(f"  {category}: {len(files)} files")
    
    # Step 4: Create a preview
    print("\nCreating 30-second preview...")
    preview = mixer.preview_mix(
        audio_files=audio_files,
        mix_type="sleep",
        preview_duration=30
    )
    
    # Save the preview for listening
    preview_path = os.path.join(output_dir, "preview.mp3")
    mixer.save_preview(
        preview=preview,
        output_path=preview_path,
        format="mp3",
        bitrate="192k"
    )
    print(f"Preview saved to: {preview_path}")
    
    # Step 5: Create the full mix
    print("\nCreating full mix...")
    mix_path = mixer.create_mix(
        audio_files=audio_files,
        mix_type="sleep",
        duration_minutes=10,  # 10-minute mix for demonstration
        output_format="mp3",
        bitrate="192k"
    )
    print(f"Mix created at: {mix_path}")
    
    # Step 6: Visualize the mix
    print("\nGenerating visualizations...")
    waveform_path = visualizer.plot_waveform(
        audio_file=mix_path,
        title="Sleep Mix Waveform"
    )
    print(f"Waveform saved to: {waveform_path}")
    
    spectrogram_path = visualizer.plot_spectrogram(
        audio_file=mix_path,
        title="Sleep Mix Spectrogram"
    )
    print(f"Spectrogram saved to: {spectrogram_path}")
    
    # Step 7: Create mix composition visualization
    mix_params = {
        "category_weights": {
            category: 1.0 for category in audio_files.keys()
        },
        "duration_minutes": 10
    }
    
    composition_path = visualizer.plot_mix_composition(
        mix_params=mix_params,
        title="Mix Composition"
    )
    print(f"Composition visualization saved to: {composition_path}")
    
    print("\nCompleted all steps!")
    print(f"Listen to your mix at: {mix_path}")

if __name__ == "__main__":
    main()
```

## Running the Example

Save this code to a file (e.g., `create_basic_mix.py`) and run it:

```bash
python create_basic_mix.py
```

Make sure you have at least some audio files in the `input_clips` directory before running.

## Step-by-Step Explanation

### 1. Setting Up

We start by creating the necessary directories and initializing our core components:

- `SoundProcessor`: Handles audio preprocessing
- `MixCreator`: Creates the actual mixes
- `AudioVisualizer`: Generates visualizations

### 2. Processing Audio

The `process_batch()` method:

- Scans the input directory for audio files
- Normalizes the audio
- Trims silence
- Optimizes each file for mixing
- Saves processed files to the processed directory

### 3. Categorizing Audio

We organize audio files by category based on filenames. This is a simple approach - in a production environment, you might use:

- Neural network classification
- Manual tagging
- Metadata extraction

### 4. Creating a Preview

We create a 30-second preview to quickly check how the mix will sound before generating the full version.

### 5. Creating the Full Mix

The mix creation process:

- Combines sounds from each category
- Applies fade-ins and fade-outs
- Adds crossfades between clips
- Applies appropriate effects for sleep
- Exports to the specified format

### 6. Visualizing the Results

We generate visualizations to understand the audio characteristics:

- Waveform: Shows amplitude over time
- Spectrogram: Shows frequency content over time
- Composition: Shows the balance of sound categories

## Customization Options

### Changing the Mix Type

```python
# Create different types of mixes
focus_mix = mixer.create_mix(
    audio_files=audio_files,
    mix_type="focus",  # Options: "sleep", "focus", "relax"
    duration_minutes=45
)

relax_mix = mixer.create_mix(
    audio_files=audio_files,
    mix_type="relax",
    duration_minutes=60
)
```

### Custom Mix Parameters

```python
# Create a mix with custom parameters
custom_mix = mixer.create_mix(
    audio_files=audio_files,
    mix_profile={
        "fade_in": 15000,          # 15 second fade in
        "fade_out": 20000,         # 20 second fade out
        "crossfade": 8000,         # 8 second crossfades
        "low_pass": 5000,          # Low-pass filter at 5000Hz
        "volume_adjustments": {
            "rain": -2,            # Rain 2dB quieter
            "thunder": -10         # Thunder 10dB quieter
        }
    },
    duration_minutes=30
)
```

### Adjusting Output Quality

```python
# Higher quality output
hq_mix = mixer.create_mix(
    audio_files=audio_files,
    output_format="flac",  # Lossless format
    bitrate="320k"         # High bitrate for MP3 (ignored for FLAC)
)

# Lower quality, smaller file size
lq_mix = mixer.create_mix(
    audio_files=audio_files,
    output_format="mp3",
    bitrate="128k"         # Lower bitrate
)
```

## Next Steps

- Learn about [AB Testing](../guides/ab-testing-guide.md) to improve mixes based on feedback
- Explore [User Profiles](../examples/user-profile-management.md) for personalized mixes
- Check out [Advanced Mix Creation](creating-advanced-mix.md) for more complex examples
