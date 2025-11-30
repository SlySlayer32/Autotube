# Getting Started with SonicSleep Pro

This guide will help you set up SonicSleep Pro for development and start using its core features.

## Prerequisites

Before starting with SonicSleep Pro, ensure that you have:

- Python 3.10 or newer
- Git for version control
- A code editor (VS Code, PyCharm, etc.)
- Basic knowledge of Python programming
- Audio playback capability on your device

## Installation

### 1. Clone the Repository

If you haven't already, clone the SonicSleep Pro repository:

```bash
git clone [repository-url]
cd project_name
```

### 2. Set Up the Development Environment

SonicSleep Pro includes a convenient setup script for Windows users:

```bash
# For Windows
.\dev_setup.bat
```

For manual setup on any platform:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. Verify Installation

Run the test suite to verify that everything is set up correctly:

```bash
pytest -xvs
```

You should see the tests run and pass.

## Quick Start

### Running the GUI Application

The easiest way to get started is to run the GUI application:

```bash
# On Windows, you can use the batch file
run_gui.bat

# Or directly with Python
python -m project_name.gui.main
```

This will open the SonicSleep Pro dashboard where you can:

- Process audio files
- Create mixes
- Visualize audio data
- Run A/B tests

### Creating Your First Mix Via Code

Here's a simple example to create a basic sleep mix using the Python API:

```python
from project_name.core.processor import SoundProcessor
from project_name.core.mix_creator import MixCreator
import os

# Initialize components
processor = SoundProcessor(
    input_folder="input_clips",
    processed_folder="processed_clips"
)

mixer = MixCreator(output_folder="output_mixes")

# Process input audio files
processed_files = processor.process_batch()

# Organize processed files by category
audio_files = {
    "rain": [f for f in processed_files if "rain" in f.lower()],
    "thunder": [f for f in processed_files if "thunder" in f.lower()]
}

# Create a 10-minute sleep mix
mix_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=10,
    output_format="mp3",
    bitrate="192k"
)

print(f"Created mix: {mix_path}")
```

### Visualizing Audio

You can create visualizations of your audio files:

```python
from project_name.core.visualizer import AudioVisualizer

# Initialize visualizer
visualizer = AudioVisualizer(output_folder="visualizations")

# Create a waveform visualization
waveform_path = visualizer.plot_waveform(
    audio_file="processed_clips/proc_rain_alleywaydrops-on-leavespuddlessidewalk.wav",
    title="Rain Waveform",
    color="#3498db"
)

print(f"Created visualization: {waveform_path}")
```

## Project Structure

The SonicSleep Pro project is organized as follows:

```
project_name/            # Main package
├── api/                 # External API integrations
├── core/                # Core functionality
│   ├── ab_testing.py    # A/B testing system
│   ├── mix_creator.py   # Mix creation
│   ├── processor.py     # Audio processing
│   ├── user_profile.py  # User profiles
│   └── visualizer.py    # Visualization
├── gui/                 # GUI application
│   └── panels/          # UI components
└── utils/               # Utilities

scripts/                 # Helper scripts
tests/                   # Test suite
docs/                    # Documentation
```

## Development Workflow

### Running Tests

SonicSleep Pro uses pytest for testing:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_mix_creator.py

# Run with coverage report
pytest --cov=project_name

# Continuous test watching
python scripts/test_watch.py
```

### Code Cleanup

Use the clean script to remove temporary files:

```bash
python scripts/clean.py

# To clean everything including virtual environments
python scripts/clean.py --all
```

## Next Steps

- Read the [Core API Reference](api/core-api-reference.md) to understand the main components
- Explore [Creating Custom Mixes](guides/creating-custom-mixes.md) for more advanced usage
- Check the [A/B Testing Guide](guides/ab-testing-guide.md) to understand the learning system
- Learn about the [Audio Processing Pipeline](guides/audio-processing-pipeline.md) for technical details

## Troubleshooting

### Common Issues

**Problem**: ModuleNotFoundError when running scripts
**Solution**: Ensure your virtual environment is activated and the package is installed with `pip install -e .`

**Problem**: Audio processing fails with "No such file or directory"
**Solution**: Check that input_clips directory exists and contains audio files

**Problem**: Tests fail with import errors
**Solution**: Make sure all dependencies are installed with `pip install -e ".[dev]"`

### Getting Help

If you encounter issues not covered here:

1. Check the logs in the `logs/` directory
2. Review the documentation in the `docs/` directory
3. Look at the test suite for examples of proper API usage
