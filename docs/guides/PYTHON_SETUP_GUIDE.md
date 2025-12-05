# 🐍 Python Version Setup Guide for OpenL3 Integration

## Current Issue

Your project is using **Python 3.12.6**, but OpenL3 requires **Python 3.10-3.11** due to the deprecated `imp` module.

## ✅ Recommended Solution: Use Python 3.11

### Option 1: Install Python 3.11 with pyenv (Recommended)

```powershell
# Install pyenv-win (if not already installed)
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# Restart PowerShell, then:
pyenv install 3.11.7
pyenv local 3.11.7

# Recreate virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Manual Python 3.11 Installation

1. **Download Python 3.11.7** from [python.org](https://www.python.org/downloads/release/python-3117/)
2. **Install** alongside your current Python (don't replace)
3. **Create new virtual environment**:

   ```powershell
   # Navigate to project directory
   cd "g:\Half built apps\test\project_name"
   
   # Remove current venv
   Remove-Item -Recurse -Force .venv
   
   # Create new venv with Python 3.11
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install --upgrade pip
   pip install openl3 tensorflow tensorflow-hub
   pip install -r requirements.txt
   ```

### Option 3: Use Conda/Anaconda

```powershell
# Create new conda environment
conda create -n project_audio python=3.11
conda activate project_audio

# Install dependencies
pip install openl3 tensorflow tensorflow-hub
pip install -r requirements.txt
```

## 🧪 Test Installation

After setting up Python 3.11, test the installation:

```powershell
python -c "
import openl3
import tensorflow as tf
print('✅ OpenL3 version:', openl3.__version__)
print('✅ TensorFlow version:', tf.__version__)
print('✅ Setup successful!')
"
```

## 📦 Updated Dependencies

Your `pyproject.toml` has been updated with:

- `python = ">=3.10,<3.12"` (excludes Python 3.12+)
- `openl3 = "^0.4.2"` (added OpenL3 dependency)
- Compatible TensorFlow versions

## 🚀 Quick Start After Setup

Once Python 3.11 is installed:

```python
import openl3
import soundfile as sf
import numpy as np

# Load audio file
audio, sr = sf.read('path/to/audio.wav')

# Extract embedding
embedding, timestamps = openl3.get_audio_embedding(audio, sr)

print("Audio similarity matching ready! 🎵")
```

## 🔧 Alternative: Manual OpenL3 Fix (Advanced)

If you must use Python 3.12, you can manually patch OpenL3:

1. Download OpenL3 source
2. Replace `import imp` with `import importlib.util` in setup.py
3. Install from modified source

**Note**: This is not recommended as it may cause other compatibility issues.

## 📞 Support

If you encounter issues:

1. Check Python version: `python --version`
2. Verify virtual environment: `which python` (Linux/Mac) or `Get-Command python` (Windows)
3. Test imports: `python -c "import openl3; print('Success!')"`

## 🎯 Next Steps

After successful installation:

1. Run the project tests: `pytest`
2. Try the OpenL3 integration examples
3. Update the audio similarity matching implementation
