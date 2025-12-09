# Installation Process Improvements - Changelog

## Overview

This update significantly improves the installation and running process for Autotube, making it as easy as double-clicking an executable file. No command-line knowledge is required for basic usage.

## What's New

### 🚀 One-Click Installation

**Windows Users:**
- Simply double-click `install.bat` to install everything automatically
- No need to manually create virtual environments or install dependencies
- The installer checks for prerequisites and guides you through any issues

**macOS/Linux Users:**
- Run `./install.sh` for automated installation
- Same automated process as Windows - creates venv, installs dependencies, sets up the application

### 🎯 Simple Launchers

After installation, running Autotube is as easy as double-clicking a file:

**GUI Mode (Graphical Interface):**
- Windows: Double-click `autotube.bat`
- macOS/Linux: Run `./autotube.sh`

**CLI Mode (Command-Line):**
- Windows: Double-click `autotube-cli.bat`
- macOS/Linux: Run `./autotube-cli.sh`

### 📚 Improved Documentation

**New Documentation Files:**
- `QUICKSTART.md` - Ultra-simple getting started guide
- `INSTALL.md` - Comprehensive installation guide with troubleshooting
- `README.launchers.txt` - Plain text explanation of launcher scripts
- Updated `README.md` with prominent Quick Start section

### 🔧 Technical Improvements

**Python Module Entry Point:**
- Added `project_name/__main__.py` to enable `python -m project_name` execution
- Makes the package executable as a module

**Setup Configuration:**
- Updated `setup.py` with proper `autotube` entry point (was `sonicsleep`)
- Added all required dependencies to setup.py
- Set correct Python version requirements (3.11)
- Added "build" extras with PyInstaller for creating executables

**PyInstaller Support (Optional):**
- Added `autotube.spec` configuration file
- Enables creation of standalone executables for distribution
- Useful for users who don't have Python installed

## Files Added

### Installation Scripts
- `install.bat` - Windows one-click installer
- `install.sh` - Unix/Linux/macOS one-click installer

### Launcher Scripts
- `autotube.bat` - Windows GUI launcher
- `autotube.sh` - Unix/Linux/macOS GUI launcher
- `autotube-cli.bat` - Windows CLI launcher
- `autotube-cli.sh` - Unix/Linux/macOS CLI launcher

### Documentation
- `QUICKSTART.md` - Quick start guide
- `INSTALL.md` - Detailed installation guide
- `README.launchers.txt` - Launcher scripts explanation
- `CHANGELOG_INSTALL_IMPROVEMENTS.md` - This file

### Configuration
- `project_name/__main__.py` - Module entry point
- `autotube.spec` - PyInstaller specification

## Files Modified

- `setup.py` - Updated entry points and dependencies
- `README.md` - Added Quick Start section
- `.gitignore` - Already includes dist/ and build/ for PyInstaller artifacts

## Breaking Changes

**None** - This is a purely additive update. All existing installation and usage methods continue to work.

## Migration Guide

If you have an existing installation:

1. **Option 1: Fresh Install (Recommended)**
   - Delete your existing `.venv` directory
   - Run the new installer (`install.bat` or `./install.sh`)
   - Use the new launchers

2. **Option 2: Keep Existing Setup**
   - Your existing installation will continue to work
   - You can optionally use the new launchers if you want the simplified experience
   - Run `pip install -e .` to update the entry point from `sonicsleep` to `autotube`

## Usage Examples

### For New Users

```bash
# Install (one-time)
# Windows: Double-click install.bat
# Unix: ./install.sh

# Run GUI
# Windows: Double-click autotube.bat
# Unix: ./autotube.sh

# That's it!
```

### For Power Users

All existing methods still work:

```bash
# Activate virtual environment
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows

# Use the autotube command
autotube --help
autotube gui
autotube status
autotube mix --duration 60

# Or use as Python module
python -m project_name.cli --help
python -m project_name.cli gui
```

## Benefits

1. **Easier Onboarding**: New users can get started in minutes without command-line knowledge
2. **Cross-Platform**: Consistent experience across Windows, macOS, and Linux
3. **Backward Compatible**: All existing usage methods continue to work
4. **Professional**: Installation process feels more polished and "app-like"
5. **Flexible**: Users can choose between simple launchers or advanced CLI/Python module usage
6. **Future-Ready**: PyInstaller support enables true executable distribution

## Technical Notes

### Python Version Requirement

The project requires **Python 3.11 specifically** (not 3.12+) due to OpenL3 dependency constraints. The installers now clearly communicate this requirement.

### Virtual Environment

All installations use virtual environments (`.venv`) to isolate dependencies and avoid conflicts with system Python packages.

### Entry Point

The package is now installed with the `autotube` command (changed from `sonicsleep`) to match the project name.

### Dependencies

All dependencies from `requirements.txt` are now also listed in `setup.py` for consistency and to enable proper package installation.

## Testing

All changes have been:
- ✅ Code reviewed
- ✅ Security scanned (CodeQL - no issues found)
- ✅ Tested for module entry point functionality
- ✅ Verified Python version requirements match across files

## Future Enhancements

Potential future improvements:
- Create actual compiled executables using PyInstaller for easy distribution
- Add auto-update functionality
- Create installer packages (.msi for Windows, .dmg for macOS, .deb for Linux)
- Add desktop shortcuts during installation

## Support

If you encounter any issues with the new installation process:

1. Check [INSTALL.md](INSTALL.md) for troubleshooting
2. Check [QUICKSTART.md](QUICKSTART.md) for simple instructions
3. Open an issue on GitHub with:
   - Your operating system and Python version
   - The complete error message
   - What you were trying to do

---

**Version:** 0.1.0  
**Date:** December 2025  
**Status:** Complete ✅
