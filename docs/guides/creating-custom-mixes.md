# Creating Custom Mixes

This guide explains how to create custom audio mixes using the SonicSleep Pro API.

## Overview

Creating a custom mix involves several steps:

1. Processing source audio files
2. Configuring mix parameters
3. Creating and exporting the mix
4. (Optional) Adjusting based on user feedback

## Prerequisites

- Processed audio files in supported formats (WAV, MP3, OGG)
- Basic understanding of audio categories (rain, thunder, white noise, etc.)
- Python environment with project_name installed

## Step 1: Set Up the Environment

First, import the necessary components and set up the basic infrastructure:

```python
from project_name.core.processor import SoundProcessor
from project_name.core.mix_creator import MixCreator
from project_name.core.user_profile import UserProfile
import os

# Set up output directories
output_dir = "my_mixes"
os.makedirs(output_dir, exist_ok=True)

# Initialize core components
processor = SoundProcessor(input_folder="my_audio", processed_folder="processed_audio")
mixer = MixCreator(output_folder=output_dir)
```

## Step 2: Process Audio Files

Before creating a mix, you should process your audio files to ensure they're normalized and optimized:

```python
# Process individual files
processed_rain = processor.preprocess_audio("path/to/rain.wav")
processed_thunder = processor.preprocess_audio("path/to/thunder.mp3")
processed_whitenoise = processor.preprocess_audio("path/to/white_noise.wav")

# Or process a batch of files
processed_files = processor.process_batch()
```

## Step 3: Create a Basic Mix

For a simple mix, organize your audio files by category and create the mix:

```python
# Organize audio files by category
audio_files = {
    "rain": [processed_rain],
    "thunder": [processed_thunder],
    "white_noise": [processed_whitenoise]
}

# Create a 60-minute sleep mix
output_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=60,
    output_format="mp3",
    bitrate="192k"
)

print(f"Mix created at: {output_path}")
```

## Step 4: Create a Profile-Based Mix

For more personalized mixes, you can use user profiles to adjust parameters:

```python
# Create or load a user profile
profile = UserProfile(name="user1", sleep_issue="insomnia")

# Get optimized parameters from the profile
from project_name.core.ab_testing import MixLearner
learner = MixLearner()
learner.profiles[profile.name] = profile  # Add profile to learner

# Get optimized parameters
optimized_params = learner.optimize_mix_parameters(profile.name)

# Extract parameters for mix creation
category_weights = optimized_params["category_weights"]

# Adjust the ratio of sounds based on category weights
weighted_audio_files = {}
for category, files in audio_files.items():
    if category in category_weights and category_weights[category] > 0.2:
        weighted_audio_files[category] = files

# Create the personalized mix
personalized_mix = mixer.create_mix(
    audio_files=weighted_audio_files,
    mix_type="sleep",  # Base type
    duration_minutes=profile.preferred_duration  # Use profile's preferred duration
)
```

## Step 5: Creating a Preview

Before generating a full-length mix, you can create a preview to check the result:

```python
# Generate a 30-second preview
preview = mixer.preview_mix(
    audio_files=audio_files,
    mix_type="sleep",
    preview_duration=30
)

# Save the preview for sharing or review
mixer.save_preview(
    preview=preview,
    output_path=os.path.join(output_dir, "preview.mp3")
)
```

## Step 6: Advanced Mix Customization

For advanced users, you can customize the mix by creating your own mix profiles:

```python
# Define a custom mix profile
custom_profile = {
    "fade_in": 15000,  # 15 seconds
    "fade_out": 20000,  # 20 seconds
    "crossfade": 6000,  # 6 seconds
    "volume_adjustments": {
        "rain": -2,      # Slightly quieter rain
        "thunder": -10,  # Much quieter thunder
        "white_noise": 0 # Normal white noise volume
    },
    "low_pass": 3500    # More aggressive low-pass filter
}

# Apply custom profile to a mix
audio = mixer._create_category_mix(audio_files["rain"], 60*60*1000, 6000)  # 60 minutes
processed_audio = mixer._apply_mix_effects(audio, custom_profile)

# Export the manually processed mix
from pydub.export import export
processed_audio.export(
    os.path.join(output_dir, "custom_mix.mp3"),
    format="mp3",
    bitrate="320k"
)
```

## Step 7: Collecting and Applying Feedback

Improve future mixes by collecting and applying user feedback:

```python
# Record feedback for a mix
mix_id = os.path.basename(output_path)  # Get mix ID from filename
feedback_score = 8  # 1-10 rating
mix_params = {
    "category_weights": category_weights,
    "primary_sounds": ["rain", "white_noise"]
}

# Update profile with feedback
profile.update_from_feedback(mix_id, feedback_score, mix_params)
profile.save()  # Save updated profile
```

## Best Practices

- **Diverse Audio Sources**: For each category, provide multiple files for more variation
- **Appropriate Durations**: Longer mixes benefit from more source material
- **Audio Quality**: Use high-quality source files (at least 256kbps MP3 or lossless)
- **Testing**: Always create previews before generating long mixes
- **Iterative Improvement**: Use the feedback mechanism to continuously improve mix quality

## Troubleshooting

**Problem**: Mix contains audible transitions or "seams"
**Solution**: Increase the crossfade duration or provide longer audio files

**Problem**: Certain sounds are too prominent or too quiet
**Solution**: Adjust the volume_adjustments in the mix profile

**Problem**: Mix is too short or too long
**Solution**: Check that your source files are long enough and properly looped

## Next Steps

- Learn about [A/B Testing](ab-testing-guide.md) to systematically improve mixes
- Explore [Audio Processing Pipeline](audio-processing-pipeline.md) for more control
- Check [Visualization Guide](visualization-guide.md) to add visual representations
