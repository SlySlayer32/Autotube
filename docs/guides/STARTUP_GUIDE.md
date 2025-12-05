# 🚀 Project Startup Guide

## 🎯 How to Start Your Audio Processing Project

### **📋 Prerequisites Check**

✅ Python 3.11 installed and configured  
✅ Virtual environment activated  
✅ Dependencies installed (OpenL3, TensorFlow, etc.)

### **🔧 Quick Setup Verification**

```powershell
# 1. Verify Python version
python --version  # Should show Python 3.11.x

# 2. Check virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Verify critical dependencies
python -c "import openl3, tensorflow; print('✅ All dependencies ready!')"
```

---

## 🖥️ **GUI Launch Options**

### **Option 1: Dashboard Interface (Recommended)**

```powershell
# Launch the modern dashboard GUI
python -m project_name.gui.main
```

### **Option 2: Classic Interface**  

```powershell
# Launch the classic GUI interface
python -m project_name.gui.main --use-classic
```

### **Option 3: Direct Script Launch**

```powershell
# Run GUI directly
python project_name/gui/main.py
```

### **Option 4: Development Mode with Hot Reload**

```powershell
# Launch with file watching (auto-restart on changes)
python scripts/run_gui_watch.py
```

---

## 📱 **CLI Interface Options**

### **Main CLI Interface**

```powershell
# Launch the command-line interface
python cli.py
```

### **Audio Processing Commands**

```powershell
# Process audio files
python cli.py process --input input_clips --output output_mixes

# Categorize audio files
python cli.py categorize --folder input_clips

# Create a mix
python cli.py mix --type sleep --duration 60
```

---

## 🧪 **Testing & Demo Options**

### **OpenL3 Similarity Demo**

```powershell
# Test audio similarity matching
python demo_openl3.py
```

### **Run Tests**

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=project_name

# Run specific test category
pytest -m unit
pytest -m integration
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Fixes**

#### ❌ "No module named 'project_name'"

```powershell
# Fix: Install the project as editable package
pip install -e .
```

#### ❌ "OpenL3/TensorFlow not found"

```powershell
# Fix: Run setup script
.\setup_python311.ps1
```

#### ❌ "Virtual environment not activated"

```powershell
# Fix: Activate environment
.\.venv\Scripts\Activate.ps1
```

#### ❌ "Python version wrong"

```powershell
# Fix: Check Python version
python --version
# Should be 3.11.x - if not, run setup_python311.ps1
```

---

## 🎵 **Feature Overview**

### **Available Functionality**

- 🎧 **Audio Processing**: Normalize, filter, trim audio
- 🎛️ **Mix Creation**: Sleep, focus, relax mixes with binaural beats  
- 🔍 **Similarity Matching**: Find similar audio clips using OpenL3
- 📊 **Audio Analysis**: YAMNet classification, mood detection
- 👤 **User Profiles**: Personalized recommendations and learning
- 📈 **Visualization**: Audio waveforms, spectrograms, analysis charts
- ⚡ **A/B Testing**: Optimize mixes based on user feedback

### **GUI Features**

- 📱 **Modern Dashboard**: Streamlined interface with real-time monitoring
- 🔄 **Classic Interface**: Full-featured traditional GUI
- 🎚️ **Audio Controls**: Volume, effects, mixing controls
- 📁 **File Management**: Drag-and-drop, batch processing
- 📊 **Analytics**: Usage statistics, mix performance

---

## 🚀 **Quick Start Workflow**

1. **Launch GUI**: `python -m project_name.gui.main`
2. **Add Audio Files**: Drop files into `input_clips/` folder
3. **Process Audio**: Use GUI or CLI to categorize and process
4. **Create Mixes**: Choose mix type and generate personalized audio
5. **Test Similarity**: Find related clips using OpenL3 matching
6. **Export & Enjoy**: Save your custom mixes to `output_mixes/`

---

## 📖 **Documentation Links**

- **Core Modules**: `project_name/core/`
- **GUI Components**: `project_name/gui/`
- **API Reference**: `project_name/api/`
- **Test Suite**: `tests/`
- **Configuration**: `pyproject.toml`, `.python-version`

---

## 🎉 **Ready to Create Amazing Audio Experiences!**

Your project is fully configured with:
✅ OpenL3 semantic audio similarity  
✅ TensorFlow-powered analysis  
✅ Modern GUI interfaces  
✅ Comprehensive testing  
✅ Python 3.11 strict version control  

**Happy audio processing!** 🎵✨
