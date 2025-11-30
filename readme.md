# Project Name

## Overview

A tool for processing and mixing ambient audio for sleep and relaxation.

## Features

- Audio preprocessing (normalize, trim silence)
- Visualization (waveform, spectrogram)
- Mix creation (sleep, focus, relax)
- Freesound API integration

## Project Structure

```
project_name/
├── project_name/          # Main package
│   ├── core/              # Core logic
│   ├── gui/               # GUI logic
│   ├── api/               # API integrations
│   └── utils/             # Utility functions
├── tests/                 # Test directory
├── data/                  # Optional for datasets
├── docs/                  # Documentation
├── visualizations/        # Visualization outputs
├── input_clips/           # Input audio files
├── processed_clips/       # Processed audio files
├── output_mixes/          # Output mixes
├── logs/                  # Log files
├── pyproject.toml         # Modern build configuration
├── README.md              # Project README
└── LICENSE                # License file
```

## Installation

1. Clone the repository.
2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

Run the GUI:

```bash
python -m project_name.gui.gui
```

Run tests:

```bash
pytest
```

## TODO List

- **GUI**: Implement the `SoundToolGUI` class to make the GUI functional.
- **Audio Processing**: Complete the logic for methods in `SoundProcessor`, such as `_classify_by_rules`.
- **Mixing**: Finalize advanced features in `MixCreator`, including binaural beats and personalized mixes.
- **Preview**: Add functionality for previewing output mixes in both CLI and GUI.

## Troubleshooting

- **Missing Dependencies**: Ensure all dependencies are installed using Poetry:

  ```bash
  poetry install
  ```

- **File Format Errors**: Verify that input files are in supported formats (e.g., WAV, MP3).
- **Permission Issues**: Ensure the script has write access to the `output_mixes` and `logs` folders.
- **Audio Processing Errors**: Check the `logs/` folder for detailed error messages.

## Examples

### Input Example

Place audio files in the `input_clips/` folder. Example:

```
input_clips/
├── rain_alleywaydrops-on-leavespuddlessidewalk.wav
├── 662201__giddster__summer-rain-and-thunder-4.wav
```

### Output Example

Generated mixes will appear in the `output_mixes/` folder. Example:

```
output_mixes/
├── sleep_mix_1743891573.mp3
├── sleep_mix_1743891574.mp3
```

## License

This project is licensed under the MIT License.
