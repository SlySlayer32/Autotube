@echo off
REM Launch SonicSleep Pro with Enhanced GUI and 2024 Features

echo ===============================================
echo  SonicSleep Pro - Enhanced GUI with 2024 Research
echo ===============================================
echo.
echo Starting Enhanced GUI with advanced features:
echo - Real-time waveform visualization
echo - Enhanced audio player with controls
echo - Progress tracking and session management
echo - Advanced mixing controls with EQ and effects
echo - Therapeutic audio protocols
echo.

cd /d "%~dp0"

REM Try to activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Launch the enhanced GUI (using classic interface)
python -m project_name.gui.main --use-classic

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Failed to launch GUI. Trying alternative method...
    python test_gui_integration.py --launch
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ GUI launch failed. Please check your installation:
    echo 1. Make sure Python is installed
    echo 2. Install dependencies: pip install numpy scipy soundfile matplotlib pygame
    echo 3. Try running: python test_gui_integration.py --test
    echo.
    pause
)
