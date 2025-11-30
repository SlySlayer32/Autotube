# MixCreator API Reference

The `MixCreator` class is responsible for creating audio mixes by combining multiple audio files according to specified parameters and profiles.

## Class Overview

```python
class MixCreator:
    def __init__(self, output_folder: str = "output_mixes")
    def create_mix(self, 
                  audio_files: Dict[str, List[str]], 
                  mix_type: str = "sleep",
                  duration_minutes: int = 60,
                  output_format: str = "mp3",
                  bitrate: str = "192k") -> Optional[str]
    def _create_category_mix(self, 
                           files: List[str], 
                           target_duration: int,
                           crossfade_duration: int) -> AudioSegment
    def _apply_mix_effects(self, mix: AudioSegment, profile: dict) -> AudioSegment
    def preview_mix(self, 
                   audio_files: Dict[str, List[str]], 
                   mix_type: str = "sleep",
                   preview_duration: int = 30) -> Optional[AudioSegment]
    def save_preview(self, 
                    preview: AudioSegment,
                    output_path: str,
                    format: str = "mp3",
                    bitrate: str = "128k") -> bool
```

## Constructor

### `__init__(output_folder: str = "output_mixes")`

Initializes a new MixCreator instance.

**Parameters:**

- `output_folder` (str, optional): Directory where output mixes will be saved. Default is "output_mixes".

**Behavior:**

- Creates the output directory if it doesn't exist
- Initializes mix profiles for different types of mixes (sleep, focus, relax)

**Example:**

```python
from project_name.core.mix_creator import MixCreator

# Create with default output folder
mixer = MixCreator()

# Create with custom output folder
mixer = MixCreator(output_folder="my_custom_mixes")
```

## Methods

### `create_mix(audio_files: Dict[str, List[str]], mix_type: str = "sleep", duration_minutes: int = 60, output_format: str = "mp3", bitrate: str = "192k") -> Optional[str]`

Creates a full audio mix from the provided audio files using the specified parameters.

**Parameters:**

- `audio_files` (Dict[str, List[str]]): Dictionary mapping categories to lists of audio file paths
- `mix_type` (str, optional): Type of mix to create ("sleep", "focus", or "relax"). Default is "sleep".
- `duration_minutes` (int, optional): Target duration of the mix in minutes. Default is 60.
- `output_format` (str, optional): Output file format ("mp3", "wav", "ogg"). Default is "mp3".
- `bitrate` (str, optional): Bitrate for compression (for formats that support it). Default is "192k".

**Returns:**

- `str` or `None`: Path to the created mix file, or None if an error occurred

**Raises:**

- `ValueError`: If invalid parameters are provided
- `FileNotFoundError`: If audio files don't exist

**Example:**

```python
# Create a 30-minute sleep mix
audio_files = {
    "rain": ["path/to/rain1.wav", "path/to/rain2.wav"],
    "thunder": ["path/to/thunder1.wav"],
    "white_noise": ["path/to/white_noise.wav"]
}

output_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=30,
    output_format="mp3",
    bitrate="320k"
)

print(f"Mix created at: {output_path}")
```

### `preview_mix(audio_files: Dict[str, List[str]], mix_type: str = "sleep", preview_duration: int = 30) -> Optional[AudioSegment]`

Creates a short preview of a mix without saving it to disk.

**Parameters:**

- `audio_files` (Dict[str, List[str]]): Dictionary mapping categories to lists of audio file paths
- `mix_type` (str, optional): Type of mix to create ("sleep", "focus", or "relax"). Default is "sleep".
- `preview_duration` (int, optional): Duration of the preview in seconds. Default is 30.

**Returns:**

- `AudioSegment` or `None`: Pydub AudioSegment object containing the preview, or None if an error occurred

**Example:**

```python
# Create a 15-second preview
preview = mixer.preview_mix(
    audio_files=audio_files,
    mix_type="focus",
    preview_duration=15
)

# You can play the preview directly (if pydub playback is configured)
from pydub.playback import play
play(preview)
```

### `save_preview(preview: AudioSegment, output_path: str, format: str = "mp3", bitrate: str = "128k") -> bool`

Saves a previously generated preview to disk.

**Parameters:**

- `preview` (AudioSegment): The preview AudioSegment to save
- `output_path` (str): Path where the preview should be saved
- `format` (str, optional): Output file format ("mp3", "wav", "ogg"). Default is "mp3".
- `bitrate` (str, optional): Bitrate for compression. Default is "128k".

**Returns:**

- `bool`: True if the preview was saved successfully, False otherwise

**Example:**

```python
# Create and save a preview
preview = mixer.preview_mix(audio_files, "sleep", 30)
success = mixer.save_preview(
    preview=preview,
    output_path="path/to/save/preview.mp3",
    format="mp3",
    bitrate="128k"
)

if success:
    print("Preview saved successfully")
else:
    print("Error saving preview")
```

## Private Methods

### `_create_category_mix(files: List[str], target_duration: int, crossfade_duration: int) -> AudioSegment`

Creates a submix for a specific category of sounds.

**Parameters:**

- `files` (List[str]): List of audio file paths for this category
- `target_duration` (int): Target duration of the submix in milliseconds
- `crossfade_duration` (int): Duration of crossfades between clips in milliseconds

**Returns:**

- `AudioSegment`: Pydub AudioSegment containing the category submix

### `_apply_mix_effects(mix: AudioSegment, profile: dict) -> AudioSegment`

Applies effects to a mix according to the specified profile.

**Parameters:**

- `mix` (AudioSegment): The mix to process
- `profile` (dict): Dictionary containing effect parameters

**Returns:**

- `AudioSegment`: Processed AudioSegment with effects applied

## Mix Profiles

The MixCreator includes built-in profiles for different mix types:

### Sleep Profile

- Gradual fade-in and fade-out (10 seconds each)
- 5-second crossfades between clips
- Low-pass filter at 4000Hz
- Volume adjustments optimized for sleep

### Focus Profile

- Shorter fade-in and fade-out (5 seconds each)
- 3-second crossfades
- Band-pass filter (500-6000Hz)
- Volume profile that emphasizes clarity

### Relax Profile

- Long fade-in and fade-out (8 seconds each)
- 4-second crossfades
- Low-pass filter at 8000Hz
- Balanced volume profile

## Usage Notes

- The MixCreator expects audio files that have already been preprocessed by SoundProcessor
- For optimal results, provide multiple files for each category
- The actual duration may vary slightly from the requested duration due to crossfade optimization
