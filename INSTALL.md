# Autotube - Installation Guide

This guide provides simplified installation instructions for Autotube, making it as easy as running an executable file.

## Quick Install (Recommended)

### Windows

1. **Download or clone** this repository
2. **Double-click** `install.bat`
3. Wait for the installation to complete
4. **Done!** Now double-click `autotube.bat` to launch the application

### macOS / Linux

1. **Download or clone** this repository
2. Open a terminal in the project directory
3. Run: `chmod +x install.sh && ./install.sh`
4. Wait for the installation to complete
5. **Done!** Now run `./autotube.sh` to launch the application

## Running Autotube

After installation, you have multiple ways to run Autotube:

### Option 1: Double-Click Launch (Easiest)

**Windows:**
- **GUI Mode:** Double-click `autotube.bat`
- **CLI Mode:** Double-click `autotube-cli.bat`

**macOS/Linux:**
- **GUI Mode:** Run `./autotube.sh`
- **CLI Mode:** Run `./autotube-cli.sh`

### Option 2: Command Line (For Power Users)

After installation, you can use the `autotube` command from anywhere:

```bash
# Activate the virtual environment first
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Then run autotube commands
autotube --help
autotube gui
autotube status
```

### Option 3: Python Module

You can also run Autotube as a Python module:

```bash
python -m project_name.cli --help
python -m project_name.cli gui
```

## Prerequisites

### Required

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
  - ⚠️ **Important:** During installation, check "Add Python to PATH"
  
- **FFmpeg** (for video generation)
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
  - **macOS:** `brew install ffmpeg`
  - **Ubuntu/Debian:** `sudo apt-get install ffmpeg`

### Optional

- **Freesound API Key** (for downloading sounds) - [Get API Key](https://freesound.org/apiv2/apply/)
- **YouTube API Credentials** (for uploading videos) - [Google Cloud Console](https://console.cloud.google.com/)

## Troubleshooting

### Installation Issues

**Problem:** `Python is not recognized as an internal or external command`

**Solution:** Python is not installed or not in your PATH. Reinstall Python and make sure to check "Add Python to PATH" during installation.

---

**Problem:** `Failed to create virtual environment`

**Solution:** Make sure you have write permissions in the installation directory. Try running the installer as administrator (Windows) or with sudo (macOS/Linux).

---

**Problem:** `Some dependencies failed to install`

**Solution:** This usually happens with complex dependencies like TensorFlow. The application may still work for basic features. To fix:
1. Make sure you have Python 3.11 (not 3.12 or newer)
2. Try running the installer again
3. Check the installation log for specific errors

---

**Problem:** Virtual environment already exists

**Solution:** If you want a fresh installation, delete the `.venv` folder and run the installer again.

---

### Running Issues

**Problem:** `Autotube is not installed` error when launching

**Solution:** Run the installer (`install.bat` or `./install.sh`) first.

---

**Problem:** GUI doesn't launch or shows errors

**Solution:** 
1. Make sure all dependencies are installed
2. Check that FFmpeg is installed and in PATH
3. Run `autotube status` to diagnose issues

---

**Problem:** `ModuleNotFoundError` when running

**Solution:** The virtual environment may not be activated. Run the launcher scripts (`autotube.bat` or `./autotube.sh`) instead of running Python directly.

---

## Advanced Installation Options

### Using Poetry (Alternative Package Manager)

If you prefer using Poetry for dependency management:

```bash
# Install Poetry first
pip install poetry

# Install dependencies
poetry install

# Run Autotube
poetry run autotube --help
```

### Manual Installation

If you prefer to install manually without the automated scripts:

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Autotube
pip install -e .

# 6. Run Autotube
autotube --help
```

### Building a Standalone Executable (Optional)

If you want to create a true `.exe` file that doesn't require Python:

```bash
# 1. Activate your virtual environment
# 2. Install PyInstaller
pip install pyinstaller

# 3. Build the executable
pyinstaller autotube.spec

# 4. Find the executable in dist/autotube/
```

**Note:** The executable will be quite large (500MB+) due to including Python and all dependencies. This is only recommended for distributing to users who don't have Python installed.

---

## Updating Autotube

To update to the latest version:

```bash
# 1. Pull the latest changes (if using git)
git pull

# 2. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Update dependencies
pip install -r requirements.txt --upgrade

# 4. Reinstall Autotube
pip install -e .
```

Or simply run the installer again to get a fresh installation.

---

## Uninstalling Autotube

To completely remove Autotube:

1. Delete the entire project directory
2. That's it! The virtual environment and all dependencies are contained within the project folder

---

## Getting Help

If you continue to have issues:

1. Check the main [README.md](README.md) for detailed documentation
2. Look at the logs in `autotube.log`
3. Open an issue on GitHub with:
   - Your operating system and Python version
   - The complete error message
   - What you were trying to do

---

## Next Steps

After installation, check out:

- [README.md](README.md) - Full feature documentation
- Run `autotube --help` to see all available commands
- Try the GUI: `autotube gui`
- Check system status: `autotube status`

Enjoy using Autotube! 🎵
