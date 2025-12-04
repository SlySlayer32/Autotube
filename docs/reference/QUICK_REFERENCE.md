# SonicSleep Pro - Quick Reference Card

## 🚀 Quick Start

```bash
# Launch Enhanced GUI
python -m project_name.gui.main

# Or use launcher
launch_therapeutic_gui.bat

# Test enhanced features
python test_enhanced_gui.py
```

## 🎯 Main Interface Tabs

### 🎵 Audio Processing

- **Left Panel:** File management + Processing controls
- **Right Panel:** Waveform visualization + Audio player
- **Key Features:** Enhanced file tree, real-time waveform, professional player

### 💾 Session Manager  

- **Save/Load:** Complete session configurations
- **Export/Import:** Share setups with others
- **Notes:** Document successful settings
- **Backup:** Automatic session preservation

### 🎛️ Advanced Mixing

- **Levels:** Volume controls for all audio components
- **EQ:** 3-band equalizer with presets
- **Effects:** Reverb, chorus, delay, compression
- **Advanced:** Crossfade, fade in/out, loop settings
- **Presets:** Save and load mixing configurations

## 🧠 Research-Based Quick Settings

### 😴 Sleep Enhancement

- **Protocol:** Pink noise + 0.25 Hz binaural beats
- **Duration:** 45-90 minutes
- **Volume:** Low, comfortable level
- **Position:** 30 minutes before sleep

### 😌 Anxiety Relief

- **Protocol:** 2 Hz beats + nature sounds
- **Duration:** 15-30 minutes
- **Volume:** Gentle, non-intrusive
- **Position:** As needed throughout day

### 🎯 Focus Enhancement

- **Protocol:** Pink noise dominant
- **Duration:** 25-60 minutes work sessions
- **Volume:** Background level
- **Position:** During cognitive tasks

## 🎧 Essential Requirements

- ✅ **Headphones required** (binaural beats need stereo)
- ✅ **Consistent use** (3+ weeks for full benefits)
- ✅ **Appropriate volume** (therapeutic, not recreational)
- ✅ **Regular sessions** (daily use recommended)

## 🔧 Quick Troubleshooting

### GUI Won't Start

```bash
# Check Python version (3.10+ required)
python --version

# Install/update dependencies
pip install -r requirements.txt

# Test with enhanced GUI
python test_enhanced_gui.py
```

### Audio Issues

- Check system volume and headphone connection
- Verify supported formats: WAV, MP3, OGG, FLAC
- Try different audio files to isolate problem
- Restart application if audio freezes

### Waveform Not Showing

- Ensure matplotlib installed: `pip install matplotlib`
- Check file permissions for selected audio
- Try smaller files first (< 10MB)
- Click "Analyze" button after selecting file

## 🎵 Quick Workflow

### Creating Therapeutic Audio

1. **Load files** → Enhanced Input section
2. **Select audio** → File tree selection
3. **View waveform** → Automatic visualization
4. **Apply processing** → 🧠 Therapeutic Process button
5. **Adjust mix** → Advanced Mixing tab
6. **Save session** → Session Manager tab
7. **Export audio** → Export buttons

### Recommended File Organization

```
/audio_library/
  /nature_sounds/     # Rain, thunder, ocean
  /ambient/           # Background atmospheres  
  /processed/         # Generated therapeutic audio
  /sessions/          # Saved configurations
```

## 📊 Progress Tracking

- **Week 1:** Initial improvements in sleep onset
- **Week 2-3:** Enhanced sleep quality, reduced anxiety
- **Week 3+:** Maximum therapeutic benefits
- **Monthly:** Reassess and adjust protocols

## 🔍 File Support

- **Input:** WAV, MP3, OGG, FLAC
- **Output:** WAV (high quality), MP3 (portable)
- **Quality:** Up to 96kHz, 24-bit supported
- **Metadata:** Duration, format, size displayed

## 💡 Pro Tips

- Save successful sessions with descriptive notes
- Create presets for different times of day
- Use batch processing for multiple files
- Export waveform plots for documentation
- Regular backups of session configurations

---
**For detailed instructions, see:** `USER_MANUAL_ENHANCED_GUI.md`
**Technical docs:** `docs/` directory
**Research basis:** `docs/research/` directory
