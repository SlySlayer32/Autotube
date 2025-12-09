# Autotube - Quick Start Guide

Get up and running with Autotube in minutes!

## 📦 Install

Choose your operating system:

### Windows
1. Double-click **`install.bat`**
2. Wait for installation to complete
3. Done! ✓

### macOS / Linux
1. Open terminal in project folder
2. Run: `./install.sh`
3. Done! ✓

## 🚀 Launch

### GUI Mode (Graphical Interface)
**Windows:** Double-click **`autotube.bat`**  
**macOS/Linux:** Run `./autotube.sh`

### CLI Mode (Command Line)
**Windows:** Double-click **`autotube-cli.bat`**  
**macOS/Linux:** Run `./autotube-cli.sh`

## 📚 First Steps

After launching the GUI:

1. **Check Status**: Click "Check Status" to verify FFmpeg is installed
2. **Load Files**: Load some audio files (or search Freesound)
3. **Create Mix**: Process and mix your audio
4. **Generate Video**: Create a video from your mix
5. **Upload** (Optional): Upload to YouTube

## 🎯 Common Tasks

### Create a Sleep Mix
```bash
autotube mix --duration 60 --mix-type sleep
```

### Generate a Video
```bash
autotube video output_mixes/mix.mp3 --waveform
```

### Run Full Pipeline
```bash
autotube pipeline --sound-type Rain --duration 60
```

### Launch GUI
```bash
autotube gui
```

## ❓ Need Help?

- **Detailed Installation**: See [INSTALL.md](INSTALL.md)
- **Full Documentation**: See [README.md](README.md)
- **Troubleshooting**: Check [INSTALL.md](INSTALL.md#troubleshooting)

## 🔧 Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **FFmpeg** ([Download](https://ffmpeg.org/download.html))

## 💡 Tips

- Use GUI for visual workflow
- Use CLI for automation and scripts
- Check `autotube --help` for all commands
- Run `autotube status` to diagnose issues

---

Enjoy creating ambient sound videos! 🎵
