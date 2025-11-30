# Visualization Guide

This guide explains how to use the SonicSleep Pro visualization tools to analyze and visualize audio data.

## Overview

SonicSleep Pro includes comprehensive visualization capabilities through the `AudioVisualizer` class, allowing you to:

1. Generate waveform displays of audio files
2. Create spectrograms for frequency analysis
3. Visualize mix compositions
4. Generate analysis reports

## Basic Usage

### Setting Up the Visualizer

```python
from project_name.core.visualizer import AudioVisualizer
import os

# Create output directory for visualizations
os.makedirs("visualizations", exist_ok=True)

# Initialize the visualizer
visualizer = AudioVisualizer(output_folder="visualizations")
```

### Creating a Simple Waveform

```python
# Generate a waveform visualization
waveform_path = visualizer.plot_waveform(
    audio_file="processed_audio/rain.wav",
    title="Rain Waveform",
    color="#3498db",  # Custom blue color
    figsize=(10, 4)   # Width, height in inches
)

print(f"Waveform saved to: {waveform_path}")
```

### Creating a Spectrogram

```python
# Generate a spectrogram visualization
spectrogram_path = visualizer.plot_spectrogram(
    audio_file="processed_audio/rain.wav",
    title="Rain Spectrogram",
    cmap="viridis",        # Colormap
    show_colorbar=True,    # Display color scale
    figsize=(10, 6)
)

print(f"Spectrogram saved to: {spectrogram_path}")
```

## Advanced Visualizations

### Frequency Spectrum Analysis

```python
# Plot frequency spectrum
spectrum_path = visualizer.plot_frequency_spectrum(
    audio_file="processed_audio/rain.wav",
    title="Frequency Content Analysis",
    log_scale=True,     # Use logarithmic frequency scale
    min_freq=20,        # Minimum frequency to display (Hz)
    max_freq=20000,     # Maximum frequency to display (Hz)
    figsize=(12, 5)
)
```

### Comparing Multiple Waveforms

```python
# Compare original and processed versions
comparison_path = visualizer.plot_multiple_waveforms(
    audio_files=[
        "raw_audio/rain_original.wav",
        "processed_audio/rain.wav"
    ],
    labels=["Original", "Processed"],
    title="Processing Comparison",
    colors=["#e74c3c", "#2ecc71"],  # Red for original, green for processed
    figsize=(12, 6)
)
```

### Visualizing Mix Composition

```python
# Visualize the composition of a mix
mix_params = {
    "category_weights": {
        "rain": 0.7,
        "thunder": 0.3,
        "white_noise": 0.5
    },
    "duration_minutes": 60,
    "fade_in": 10000,
    "fade_out": 10000
}

composition_path = visualizer.plot_mix_composition(
    mix_params=mix_params,
    title="Sleep Mix Composition",
    figsize=(10, 8)
)
```

### Time-Frequency Analysis

```python
# Create a combined time-frequency visualization
tf_analysis_path = visualizer.plot_time_frequency_analysis(
    audio_file="processed_audio/rain.wav",
    title="Time-Frequency Analysis",
    window_size=2048,   # FFT window size
    hop_length=512,     # Hop length between windows
    figsize=(12, 8)
)
```

## Comprehensive Audio Reports

### Generating an Analysis Report

```python
# Create a comprehensive audio analysis report
report_path = visualizer.generate_audio_analysis_report(
    audio_file="processed_audio/rain.wav",
    title="Rain Audio Analysis",
    format="pdf",          # Output format (pdf, html)
    include_features=True  # Include extracted audio features
)

print(f"Analysis report saved to: {report_path}")
```

### Mix Comparison Report

```python
# Compare multiple mixes
comparison_report = visualizer.generate_mix_comparison_report(
    mix_files=[
        "output_mixes/sleep_mix_1.mp3",
        "output_mixes/sleep_mix_2.mp3"
    ],
    titles=["Original Mix", "Optimized Mix"],
    format="html"
)
```

## Customizing Visualizations

### Styling Options

You can customize the appearance of visualizations:

```python
# Set global visualization style
visualizer.set_style(
    style="dark_background",  # Use dark background style
    font_family="Arial",
    title_font_size=16,
    axis_font_size=12,
    grid=True,
    dpi=300          # High resolution for print
)

# Create visualization with custom style
custom_waveform = visualizer.plot_waveform(
    audio_file="processed_audio/thunder.wav",
    style="seaborn-whitegrid",  # Override global style for this plot
    color_palette="magma",
    alpha=0.8,              # Transparency
    linewidth=1.2
)
```

### Interactive Visualizations

For web or GUI applications, you can create interactive visualizations:

```python
# Generate an interactive spectrogram (HTML output)
interactive_path = visualizer.plot_interactive_spectrogram(
    audio_file="processed_audio/thunder.wav",
    height=500,
    width=900,
    tools=["pan", "zoom", "reset", "save"],
    palette="Spectral",
    output_format="html"
)
```

## Integration with Audio Processing

### Visualizing Processing Stages

```python
from project_name.core.processor import SoundProcessor

processor = SoundProcessor()
visualizer = AudioVisualizer(output_folder="process_visualization")

# Process an audio file
input_file = "raw_audio/rain.wav"
normalized = processor.normalize_audio(
    AudioSegment.from_file(input_file), 
    target_db=-18
)
filtered = processor._apply_bandpass_filter(
    normalized, 
    low_cutoff=100, 
    high_cutoff=8000
)

# Visualize each stage
stages = [
    {"audio": AudioSegment.from_file(input_file), "label": "Original"},
    {"audio": normalized, "label": "Normalized"},
    {"audio": filtered, "label": "Filtered"}
]

# Save each stage temporarily
stage_files = []
for i, stage in enumerate(stages):
    temp_path = f"temp_stage_{i}.wav"
    stage["audio"].export(temp_path, format="wav")
    stage_files.append(temp_path)

# Create visualization of processing pipeline
pipeline_viz = visualizer.plot_processing_pipeline(
    audio_files=stage_files,
    labels=[stage["label"] for stage in stages],
    title="Audio Processing Pipeline Visualization"
)
```

### Visualizing A/B Test Results

```python
from project_name.core.ab_testing import MixLearner

learner = MixLearner()
learner.load_profiles()
learner.load_ab_tests()

# Generate visualization of learning trends
trends_viz = visualizer.plot_learning_trends(
    learning_trends=learner.analyze_learning_trends(),
    title="A/B Testing Learning Trends",
    figsize=(14, 10)
)
```

## Exporting in Different Formats

The visualizer supports multiple output formats:

```python
# Export in different formats
visualizer.plot_waveform(
    audio_file="processed_audio/rain.wav",
    format="png",
    dpi=300
)

visualizer.plot_waveform(
    audio_file="processed_audio/rain.wav",
    format="svg",   # Vector format for printing
)

visualizer.plot_waveform(
    audio_file="processed_audio/rain.wav",
    format="pdf",   # PDF output
)
```

## Best Practices

### Performance Tips

- For large audio files, use the `segment` parameter to visualize only a portion:

  ```python
  visualizer.plot_waveform(
      audio_file="long_audio.wav",
      segment=(30, 60)  # Visualize from 30s to 60s
  )
  ```

- For batch processing, use the batch visualization methods:

  ```python
  visualizer.batch_visualize(
      audio_folder="processed_audio",
      output_type="waveform",
      recursive=True
  )
  ```

### Visualization Guidelines

- **Waveforms**: Best for viewing amplitude changes over time
- **Spectrograms**: Best for frequency content analysis
- **Spectrum Plots**: Best for overall frequency balance
- **Combination Plots**: Best for comprehensive analysis

### Common Issues

**Problem**: Visualizations appear blurry or pixelated
**Solution**: Increase the DPI setting (e.g., dpi=300)

**Problem**: Text is too small to read
**Solution**: Increase font sizes or adjust figure size

**Problem**: Colors don't provide enough contrast
**Solution**: Try different colormaps like 'viridis', 'plasma', or 'inferno'

## Next Steps

- Learn about [AB Testing](ab-testing-guide.md) to use visualizations for comparing mixes
- Explore [Audio Processing Pipeline](audio-processing-pipeline.md) for technical details
- Check out [Creating Custom Mixes](creating-custom-mixes.md) for practical applications
