# Autotube

## Overview

Autotube is a complete automation tool for creating and uploading ambient sleep/relaxation sound videos to YouTube. It handles the entire workflow from audio processing and mixing to video generation, SEO-optimized metadata creation, and YouTube upload.

## Features

- **Audio Processing**: Preprocessing, normalization, and mixing of ambient audio
- **Video Generation**: Create videos with static backgrounds or waveform visualizations
- **YouTube Upload**: Automated uploads with OAuth2 authentication
- **Metadata Generation**: SEO-optimized titles, descriptions, and tags
- **Content Planning**: Schedule and plan video content
- **CLI Interface**: Full command-line interface for automation
- **GUI Interface**: Graphical user interface for manual control
- **Freesound Integration**: Search and download sounds from Freesound

## Project Structure

```
project_name/
├── project_name/          # Main package
│   ├── core/              # Core logic
│   │   ├── video_generator.py      # Video creation from audio
│   │   ├── metadata_generator.py   # SEO metadata generation
│   │   ├── orchestrator.py         # Pipeline orchestration
│   │   ├── processor.py            # Audio processing
│   │   └── mix_creator.py          # Audio mixing
│   ├── api/               # API integrations
│   │   ├── youtube_uploader.py     # YouTube Data API
│   │   └── freesound_api.py        # Freesound API
│   ├── gui/               # GUI logic
│   ├── cli.py             # Click-based CLI
│   └── utils/             # Utility functions
├── tests/                 # Test directory
├── docs/                  # Documentation
├── input_clips/           # Input audio files
├── processed_clips/       # Processed audio files
├── output_mixes/          # Generated audio mixes
├── output_videos/         # Generated videos
├── pyproject.toml         # Build configuration
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.11+
- FFmpeg (for video generation)
- pip or Poetry

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or using Poetry:
```bash
poetry install
```

### YouTube API Setup (Optional - for uploads)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials and save as `client_secrets.json`

## Usage

### CLI Commands

Autotube provides a comprehensive CLI built with Click:

```bash
# View all available commands
python -m project_name.cli --help

# View help for a specific command
python -m project_name.cli <command> --help
```

#### Create Audio Mix
```bash
python -m project_name.cli mix --input input_clips --output output_mixes --duration 60 --mix-type sleep
```

#### Generate Video from Audio
```bash
python -m project_name.cli video path/to/audio.mp3 --output output_videos --title "Sleep Sounds"
```

#### Generate SEO Metadata
```bash
python -m project_name.cli metadata --sound-type Rain --duration 8 --purpose sleep
```

#### Upload Video to YouTube
```bash
python -m project_name.cli upload video.mp4 --title "Rain Sounds" --description "8 hours of rain" --privacy private
```

#### Run Full Pipeline
```bash
python -m project_name.cli pipeline --sound-type Rain --duration 60 --mix-type sleep --no-upload
```

#### Plan Content
```bash
python -m project_name.cli plan --num-videos 7
```

#### Check Status
```bash
python -m project_name.cli status
```

### GUI

Launch the graphical user interface:
```bash
python -m project_name.cli gui

# Or use the classic UI
python -m project_name.cli gui --classic
```

### Freesound Integration

Search and download sounds from Freesound:
```bash
python -m project_name.cli freesound
```

## Pipeline Overview

The complete Autotube pipeline:

1. **Audio Processing**: Load and preprocess audio clips
2. **Mix Creation**: Combine clips into ambient mixes
3. **Video Generation**: Create video with static or animated background
4. **Metadata Generation**: Generate SEO-optimized title, description, and tags
5. **YouTube Upload**: Upload video with metadata to YouTube

## Examples

### Input Example

Place audio files in the `input_clips/` folder:
```
input_clips/
├── rain_ambient.wav
├── ocean_waves.mp3
├── forest_sounds.wav
```

### Output Example

Generated content:
```
output_mixes/
├── sleep_mix_1743891573.mp3

output_videos/
├── sleep_mix_1743891573_video.mp4
```

### Content Plan Example
```
# Content Plan
======================================================================
#   Sound Type      Purpose    Date         Time     Duration
----------------------------------------------------------------------
1   Rain            sleep      2024-01-15   20:00    8h
2   Ocean           focus      2024-01-16   08:00    2h
3   Nature          relax      2024-01-17   18:00    2h
======================================================================
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```
FREESOUND_API_KEY=your_freesound_api_key
```

### YouTube Credentials

Place your `client_secrets.json` in the project root for YouTube API access.

## Testing

Run all tests:
```bash
python -m pytest tests/ -v -p no:cacheprovider -o addopts=""
```

Run specific test modules:
```bash
python -m pytest tests/test_metadata_generator.py -v -o addopts=""
python -m pytest tests/test_video_generator.py -v -o addopts=""
python -m pytest tests/test_youtube_uploader.py -v -o addopts=""
python -m pytest tests/test_orchestrator.py -v -o addopts=""
```

## Troubleshooting

- **FFmpeg Not Found**: Ensure FFmpeg is installed and in your PATH
- **YouTube API Errors**: Check that `client_secrets.json` is valid and API is enabled
- **Missing Dependencies**: Run `pip install -r requirements.txt`
- **Audio Format Errors**: Ensure files are in supported formats (WAV, MP3, FLAC, OGG, M4A)
- **Permission Issues**: Ensure write access to output folders

## License

This project is licensed under the MIT License.
