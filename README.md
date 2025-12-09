# Autotube

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Autotube is a complete automation tool for creating and uploading ambient sleep/relaxation sound videos to YouTube. It handles the entire workflow from audio processing and mixing to video generation, SEO-optimized metadata creation, and YouTube upload.

## Features

### Core Functionality
- **Audio Processing**: Preprocessing, normalization, and intelligent mixing of ambient audio
- **Video Generation**: Create videos with static backgrounds or waveform visualizations using FFmpeg
- **YouTube Upload**: Automated uploads with OAuth2 authentication and resumable uploads
- **Metadata Generation**: SEO-optimized titles, descriptions, and tags with templates
- **Content Planning**: Schedule and plan video content with optimal publish times

### User Interfaces
- **CLI Interface**: Full command-line interface built with Click for automation and scripting
- **GUI Interface**: Modern graphical user interface with dashboard and classic modes

### Integrations
- **Freesound Integration**: Search and download sounds from Freesound with therapeutic sound filters
- **YouTube Data API v3**: Upload, manage, and track video performance

### Advanced Features
- **Audio Similarity Matching**: Find similar audio clips using OpenL3 embeddings
- **Psychoacoustic Analysis**: Extract features related to human perception of sound
- **A/B Testing System**: Test and optimize audio mixes based on user feedback
- **User Profiles**: Personalized preference tracking for mix optimization
- **Binaural Beat Generation**: Generate binaural beats for enhanced relaxation

## Project Structure

```
autotube/
├── project_name/              # Main package
│   ├── core/                  # Core logic
│   │   ├── processor.py           # Audio preprocessing and categorization
│   │   ├── mix_creator.py         # Audio mixing with profiles
│   │   ├── video_generator.py     # Video creation from audio
│   │   ├── metadata_generator.py  # SEO metadata generation
│   │   ├── orchestrator.py        # Pipeline orchestration
│   │   ├── audio_similarity.py    # Audio similarity matching
│   │   ├── ab_testing.py          # A/B testing system
│   │   ├── user_profile.py        # User preference management
│   │   ├── visualizer.py          # Audio visualization
│   │   └── deep_learning.py       # ML-based classification
│   ├── api/                   # API integrations
│   │   ├── youtube_uploader.py    # YouTube Data API v3
│   │   └── freesound_api.py       # Freesound API client
│   ├── gui/                   # GUI components
│   │   ├── main.py                # GUI entry point
│   │   ├── dashboard_app.py       # Modern dashboard UI
│   │   ├── gui.py                 # Classic GUI
│   │   ├── panels/                # UI panel components
│   │   └── widgets/               # Reusable UI widgets
│   ├── cli.py                 # Click-based CLI commands
│   └── utils/                 # Utility functions
├── tests/                     # Test suite
│   ├── test_processor.py
│   ├── test_mix_creator.py
│   ├── test_video_generator.py
│   ├── test_metadata_generator.py
│   ├── test_youtube_uploader.py
│   └── ...
├── docs/                      # Documentation
│   ├── guides/                    # User guides
│   ├── api/                       # API reference
│   ├── architecture/              # System design docs
│   └── examples/                  # Code examples
├── scripts/                   # Utility scripts
├── pyproject.toml             # Build configuration
├── requirements.txt           # Dependencies
├── TODO.md                    # Development tasks
└── README.md                  # This file
```

## Quick Start

### One-Click Installation ⚡

The easiest way to install and run Autotube:

**Windows:**
1. Double-click `install.bat` to install
2. Double-click `autotube.bat` to run

**macOS/Linux:**
1. Run `./install.sh` to install
2. Run `./autotube.sh` to run

That's it! See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

---

## Installation

### Prerequisites

- **Python 3.11** (required - see [Python Setup Guide](docs/guides/PYTHON_SETUP_GUIDE.md) for details)
- **FFmpeg** (for video generation)
- **pip** or **Poetry** (for dependency management)

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

### Automated Installation (Recommended)

**Windows:**
```batch
# Run the one-click installer
install.bat
```

**macOS/Linux:**
```bash
# Run the one-click installer
chmod +x install.sh
./install.sh
```

### Manual Installation

**Using pip:**
```bash
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

**Using Poetry:**
```bash
poetry install
```

**Windows Quick Setup:**
```batch
# Run the development setup script
.\dev_setup.bat
```

### Freesound API Setup (Optional - for sound downloads)

1. Create an account at [Freesound.org](https://freesound.org/)
2. Apply for an API key at [Freesound API](https://freesound.org/apiv2/apply/)
3. Create a `.env` file in the project root:
   ```
   FREESOUND_API_KEY=your_api_key_here
   ```

### YouTube API Setup (Optional - for uploads)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials and save as `client_secrets.json`

## Usage

### Quick Start

```bash
# Check system status
python -m project_name.cli status

# Create a sleep mix from audio clips (60 minutes)
python -m project_name.cli mix --input input_clips --output output_mixes --duration 60 --mix-type sleep

# Generate a video from the mix
python -m project_name.cli video output_mixes/sleep_mix_*.mp3 --output output_videos

# Generate metadata for the video
python -m project_name.cli metadata --sound-type Rain --duration 1 --purpose sleep
```

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

Options:
- `--input, -i`: Input folder containing raw audio files (default: `input_clips`)
- `--output, -o`: Output folder for final mixes (default: `output_mixes`)
- `--duration, -d`: Duration of mix in minutes (default: 60)
- `--mix-type, -t`: Type of mix: `sleep`, `focus`, or `relax` (default: `sleep`)

#### Generate Video from Audio
```bash
python -m project_name.cli video path/to/audio.mp3 --output output_videos --title "Sleep Sounds"
```

Options:
- `--output, -o`: Output folder for generated videos (default: `output_videos`)
- `--title, -t`: Title text to display on video background
- `--waveform, -w`: Create video with waveform visualization

#### Generate SEO Metadata
```bash
python -m project_name.cli metadata --sound-type Rain --duration 8 --purpose sleep --format json
```

Options:
- `--sound-type, -s`: Type of sound (e.g., Rain, Ocean, Nature)
- `--duration, -d`: Duration in hours (default: 8)
- `--purpose, -p`: Purpose: `sleep`, `focus`, or `relax`
- `--format, -f`: Output format: `text` or `json`

#### Upload Video to YouTube
```bash
python -m project_name.cli upload video.mp4 --title "Rain Sounds" --description "8 hours of rain" --privacy private
```

Options:
- `--title, -t`: Video title (required)
- `--description, -d`: Video description
- `--tags`: Comma-separated list of tags
- `--privacy`: Privacy status: `public`, `private`, or `unlisted`
- `--credentials, -c`: Path to YouTube API client secrets file

#### Run Full Pipeline
```bash
python -m project_name.cli pipeline --sound-type Rain --duration 60 --mix-type sleep --no-upload
```

Options:
- `--sound-type, -s`: Type of sound for metadata
- `--duration, -d`: Duration in minutes
- `--mix-type, -t`: Type of mix
- `--privacy`: YouTube privacy status
- `--waveform, -w`: Use waveform visualization
- `--no-upload`: Skip YouTube upload

#### Plan Content
```bash
python -m project_name.cli plan --num-videos 7 --format table
```

#### Check Status
```bash
python -m project_name.cli status
```

### GUI

Launch the graphical user interface:
```bash
# Modern dashboard UI (recommended)
python -m project_name.cli gui

# Classic UI
python -m project_name.cli gui --classic
```

#### GUI Features

The GUI provides complete feature parity with the CLI, exposing all workflow steps and configuration options:

**Dashboard Mode** (Modern Interface):
- **🚀 Pipeline Control Panel**: Complete workflow automation
  - Full pipeline mode: One-click automation from audio to upload
  - Step-by-step mode: Granular control over each stage (Mix → Metadata → Video → Upload)
  - Progress tracking and results display
  - All configuration options (folders, duration, sound type, mix type, waveform, privacy)
  - Status and folder information display
  
- **📅 Content Planning Panel**: Video content scheduling
  - Generate content plans for multiple videos
  - Display in organized table view
  - Export to JSON, CSV, or text formats
  - Plan statistics and analytics
  
- **📁 Input Processing Panel**: Audio file management
  - Load local audio files
  - Freesound integration for sound search and download
  - File preview and organization
  
- **🎵 Audio Processing Panel**: Audio manipulation
  - Process and normalize audio files
  - Apply effects and filters
  - Audio analysis and categorization
  
- **📊 Analysis Panel**: Visualization and metrics
  - Waveform visualization
  - Frequency spectrum analysis
  - A/B testing interface
  - Sleep quality metrics
  
- **🧠 Therapeutic Audio Panel**: Advanced audio generation
  - 2024 research-based therapeutic audio features
  - Psychoacoustic optimization
  - Binaural beat generation
  
- **⚙️ Settings Panel**: Complete configuration
  - Folder paths (input, output, video)
  - YouTube API credentials and privacy settings
  - Video options (waveform, background color)
  - Freesound API key configuration
  - Audio processing parameters
  - Mix presets and AI recommendations

**Classic Mode** (Traditional Interface):
- **Enhanced Toolbar**: Quick access to all major functions
  - 📁 Load Files
  - ⚙️ Process Audio
  - 🎵 Create Mix
  - 🎬 Generate Video
  - ☁️ Upload to YouTube
  - 🚀 Full Pipeline
  - 📅 Plan Content
  
- **Complete Menu Bar**:
  - File: Load files, Freesound search, Settings, Exit
  - Edit: Preferences, Clear log
  - View: Refresh, Toggle toolbar, Toggle status bar
  - Help: About
  
- **Dialog-Based Workflows**:
  - Video generation with full options
  - YouTube upload with metadata fields
  - Pipeline configuration and execution
  - Content planning and scheduling

**Key GUI Features**:
- ✅ Complete CLI feature parity
- ✅ Thread-based execution (non-blocking UI)
- ✅ Real-time progress tracking
- ✅ Error handling and validation
- ✅ Configuration persistence
- ✅ Both one-click and step-by-step workflows
- ✅ Comprehensive status displays

### Freesound Integration

Search and download sounds from Freesound interactively:
```bash
python -m project_name.cli freesound
```

### Python API

You can also use Autotube programmatically:

```python
from project_name.core.processor import SoundProcessor
from project_name.core.mix_creator import MixCreator
from project_name.core.video_generator import VideoGenerator
from project_name.core.metadata_generator import MetadataGenerator

# Process audio files
processor = SoundProcessor(input_folder="input_clips")
for file in os.listdir("input_clips"):
    processor.preprocess_audio(os.path.join("input_clips", file))
categories = processor.analyze_clips()

# Create a mix
mixer = MixCreator(output_folder="output_mixes")
mix_path = mixer.create_mix(
    audio_files=categories,
    mix_type="sleep",
    duration_minutes=60
)

# Generate video
video_gen = VideoGenerator(output_folder="output_videos")
video_path = video_gen.generate_video_from_audio(mix_path, title_text="Sleep Sounds")

# Generate metadata
meta_gen = MetadataGenerator()
metadata = meta_gen.generate_complete_metadata(
    sound_type="Rain",
    duration_hours=1,
    purpose="sleep"
)
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
pytest tests/ -v
```

Run specific test modules:
```bash
pytest tests/test_metadata_generator.py -v
pytest tests/test_video_generator.py -v
pytest tests/test_youtube_uploader.py -v
pytest tests/test_orchestrator.py -v
pytest tests/test_mix_creator.py -v
```

Run tests with coverage:
```bash
pytest --cov=project_name tests/
```

## Documentation

Detailed documentation is available in the `docs/` folder:

- **[Getting Started Guide](docs/guides/getting-started.md)** - Setup and first steps
- **[Creating Custom Mixes](docs/guides/creating-custom-mixes.md)** - Advanced mix creation
- **[A/B Testing Guide](docs/guides/ab-testing-guide.md)** - Optimize mixes with testing
- **[Audio Processing Pipeline](docs/guides/audio-processing-pipeline.md)** - Technical details
- **[Visualization Guide](docs/guides/visualization-guide.md)** - Create audio visualizations
- **[API Reference](docs/api/)** - Core API documentation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **FFmpeg Not Found** | Ensure FFmpeg is installed and in your PATH |
| **YouTube API Errors** | Check that `client_secrets.json` is valid and API is enabled |
| **Missing Dependencies** | Run `pip install -r requirements.txt` |
| **Audio Format Errors** | Ensure files are in supported formats (WAV, MP3, FLAC, OGG, M4A) |
| **Permission Issues** | Ensure write access to output folders |
| **Python Version Errors** | This project requires Python 3.11. See [Python Setup Guide](docs/guides/PYTHON_SETUP_GUIDE.md) |

For more troubleshooting help, check the logs in `autotube.log` or refer to the [documentation](docs/).

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style (use `ruff` for linting)
   - Add tests for new functionality
   - Update documentation as needed
4. **Run tests**
   ```bash
   pytest tests/ -v
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

### Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code style
ruff check .

# Format code
ruff format .
```

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Or with Poetry
poetry install --with dev
```

## Roadmap

See [TODO.md](TODO.md) for the current list of planned features, known issues, and development tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for video processing
- [Freesound](https://freesound.org/) for the audio library API
- [librosa](https://librosa.org/) for audio analysis
- [pydub](https://github.com/jiaaro/pydub) for audio manipulation
- [Click](https://click.palletsprojects.com/) for the CLI framework
