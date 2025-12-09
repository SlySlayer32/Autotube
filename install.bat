@echo off
REM ============================================================================
REM Autotube - One-Click Installer
REM ============================================================================
REM This script automatically sets up Autotube on your system.
REM Simply double-click this file to install!
REM ============================================================================

echo.
echo ============================================================================
echo                    AUTOTUBE - One-Click Installer
echo ============================================================================
echo.
echo This installer will:
echo   1. Check for Python 3.11+
echo   2. Create a virtual environment
echo   3. Install all dependencies
echo   4. Set up the application
echo.
echo Press Ctrl+C to cancel or
pause

REM Check if Python is available
echo.
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check if virtual environment exists
echo.
echo [2/4] Setting up virtual environment...
if exist .venv (
    echo Virtual environment already exists.
    choice /C YN /M "Do you want to recreate it"
    if errorlevel 2 (
        echo Keeping existing virtual environment.
    ) else (
        echo Removing existing virtual environment...
        rmdir /s /q .venv
        echo Creating new virtual environment...
        python -m venv .venv
        if %errorlevel% neq 0 (
            echo ERROR: Failed to create virtual environment!
            pause
            exit /b 1
        )
    )
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo.
echo [3/4] Installing dependencies...
echo This may take several minutes. Please be patient...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some dependencies may have failed to install.
    echo The application might still work, but some features may be unavailable.
    echo.
)

REM Install package in editable mode
echo.
echo [4/4] Installing Autotube...
pip install -e .
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Autotube!
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                    INSTALLATION COMPLETE!
echo ============================================================================
echo.
echo Autotube has been successfully installed!
echo.
echo To run Autotube:
echo   - Double-click 'autotube.bat' (GUI mode)
echo   - Double-click 'autotube-cli.bat' (Command-line mode)
echo   - Or run from command line: autotube --help
echo.
echo For more information, see README.md
echo.
echo ============================================================================
echo.
pause
