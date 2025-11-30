@echo off
REM Project Python Version Control Script
REM This script ensures the project always uses Python 3.11

set PYTHON_311_PATH=C:\Users\Sly\AppData\Local\Programs\Python\Python311\python.exe

echo ========================================
echo   PROJECT PYTHON VERSION CONTROL
echo ========================================
echo.
echo Checking Python 3.11 installation...

if not exist "%PYTHON_311_PATH%" (
    echo ERROR: Python 3.11 not found at expected location!
    echo Expected: %PYTHON_311_PATH%
    echo.
    echo Please install Python 3.11 or update the path in this script.
    pause
    exit /b 1
)

echo ✅ Python 3.11 found: %PYTHON_311_PATH%

REM Display version
echo.
echo Python version:
"%PYTHON_311_PATH%" --version

echo.
echo ========================================
echo   RECREATING VIRTUAL ENVIRONMENT
echo ========================================

REM Remove existing virtual environment
if exist ".venv" (
    echo Removing existing virtual environment...
    rmdir /s /q .venv
)

REM Create new virtual environment with Python 3.11
echo Creating new virtual environment with Python 3.11...
"%PYTHON_311_PATH%" -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo ========================================
echo   INSTALLING DEPENDENCIES
echo ========================================

REM Install core dependencies first
echo Installing core dependencies...
pip install numpy==1.24.3
pip install scipy==1.10.1

REM Install TensorFlow (compatible with Python 3.11)
echo Installing TensorFlow...
pip install "tensorflow>=2.10.0,<2.16.0"
pip install "tensorflow-hub>=0.14.0,<0.16.0"

REM Install OpenL3
echo Installing OpenL3...
pip install openl3

REM Install remaining dependencies
echo Installing remaining dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo   VERIFICATION
echo ========================================

echo Testing critical imports...
python -c "
try:
    import tensorflow as tf
    import openl3
    import numpy as np
    import librosa
    print('✅ TensorFlow version:', tf.__version__)
    print('✅ OpenL3 version:', openl3.__version__)
    print('✅ NumPy version:', np.__version__)
    print('✅ Librosa version:', librosa.__version__)
    print('✅ All critical dependencies installed successfully!')
except ImportError as e:
    print('❌ Import error:', str(e))
    exit(1)
"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Dependency installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SETUP COMPLETE
echo ========================================
echo.
echo ✅ Project successfully configured for Python 3.11
echo ✅ Virtual environment created and activated
echo ✅ All dependencies installed
echo.
echo To activate the environment in future sessions, run:
echo   .venv\Scripts\activate.bat
echo.
echo To run the project:
echo   python cli.py
echo.
pause
