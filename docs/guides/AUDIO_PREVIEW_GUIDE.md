# Audio Preview Feature Guide

## Overview

The SonicSleep Pro GUI now includes **audio preview functionality** for both collected and manually added files. This allows you to listen to samples of your audio files to verify they contain the correct content before processing.

## Features

### 🎵 Audio Preview Capabilities

- **Double-click playback**: Double-click any file in the "Collected Files" or "Selected Files" lists to instantly preview it
- **Preview button**: Select a file and click the "▶ Preview" button for controlled playback
- **Stop functionality**: Use the "⏹ Stop" button to stop any currently playing audio
- **Real-time status**: See what's currently playing in the status text below each file list
- **Multiple format support**: Works with WAV, MP3, OGG, and FLAC files

### 🔧 How It Works

#### For Collected Files (Automated Collection)

1. Start the automated collection process using "🎵 Start Automated Collection"
2. Files will appear in the "Collected Files" list as they're downloaded
3. **Double-click** any file in the list to preview it
4. Or **select a file and click "▶ Preview"** to play it
5. Click "⏹ Stop" to stop playback

#### For Manual Files (Browse & Upload)

1. Use "Browse for Audio Files" or "Browse for Folder" to add your own files
2. Files will appear in the "Selected Files" list
3. **Double-click** any file in the list to preview it
4. Or **select a file and click "▶ Preview"** to play it
5. Click "⏹ Stop" to stop playback

### 🎧 Audio Backend Support

The audio preview system automatically detects and uses the best available audio library:

1. **Pygame** (Primary): Full format support (WAV, MP3, OGG, FLAC) with good control
2. **Winsound** (Windows fallback): WAV files only, limited control
3. **System player** (Last resort): Opens files in your default audio player

### 📝 Usage Instructions

#### Quick Preview (Recommended)

```
1. Double-click any audio file in either list
2. Audio will start playing immediately
3. Status will show "Playing: [filename]"
4. Double-click another file or click Stop to change/stop
```

#### Controlled Preview

```
1. Click once to select an audio file
2. Click the "▶ Preview" button
3. Monitor the status text for playback information
4. Click "⏹ Stop" when finished
```

### ⚠️ Troubleshooting

#### No Audio Playing

- **Check file format**: Ensure the file is a supported audio format (WAV, MP3, OGG, FLAC)
- **Check file location**: Verify the file exists and hasn't been moved or deleted
- **Volume settings**: Check your system volume and audio output device
- **File corruption**: Try playing the file in another audio player to verify it's not corrupted

#### Limited Functionality

- **WAV only**: If only WAV files work, pygame might not be properly installed
- **No preview button response**: The file might be corrupted or in an unsupported format
- **System player opens**: If an external player opens instead of inline preview, the audio libraries need installation

#### Error Messages

- **"File not found or invalid"**: The file path is incorrect or the file was deleted
- **"Audio preview not available"**: No audio libraries are installed
- **"Error: [specific error]"**: Check the console output for detailed error information

### 🔧 Technical Details

#### Audio Libraries Used

```python
# Primary: Pygame (full feature support)
import pygame
pygame.mixer.music.load(file_path)
pygame.mixer.music.play()

# Fallback: Windows winsound (WAV only)
import winsound
winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

# Last resort: System default player
os.startfile(file_path)  # Windows
```

#### File Path Tracking

The system maintains dictionaries to track the full file paths:

- `collected_files_paths{}`: Maps display names to actual file paths for collected files
- `manual_files_paths{}`: Maps display names to actual file paths for manual files

### 🎯 Benefits

1. **Quality Verification**: Ensure downloaded files contain the expected audio content
2. **Quick Audition**: Rapidly test multiple files without leaving the interface
3. **Workflow Efficiency**: Preview files before committing to processing
4. **Error Detection**: Identify corrupted or incorrect files early in the process
5. **User Confidence**: Verify that automatic collection is working correctly

### 📊 Preview Status Messages

| Status Message | Meaning |
|----------------|---------|
| "Double-click or select and press Preview to play" | Ready state, no file selected |
| "Playing: [filename]" | Currently playing the specified file |
| "Preview stopped" | Playback has been stopped |
| "Please select a file to preview" | No file is selected |
| "File not found or invalid" | The selected file doesn't exist or is corrupted |
| "Audio preview not available - no audio libraries found" | No audio playback libraries are installed |

### 🚀 Getting Started

1. **Install Audio Support** (if needed):

   ```bash
   pip install pygame
   ```

2. **Start the GUI**:

   ```bash
   python unified_sleep_audio_gui.py
   ```

3. **Test Preview**:
   - Go to Step 1: Collect Sounds
   - Start automated collection or browse for files
   - Double-click any file in the lists to test preview functionality

### 💡 Tips for Best Experience

- **Use headphones**: For better audio quality assessment
- **Test early**: Preview files immediately after collection to catch issues
- **Check duration**: Ensure files are the expected length
- **Listen for quality**: Verify audio is clear and not distorted
- **Volume control**: Adjust your system volume for comfortable listening

---

*This feature enhances the SonicSleep Pro workflow by providing immediate audio feedback, ensuring you're working with the right sounds for your therapeutic sleep audio projects.*
