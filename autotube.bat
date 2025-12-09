@echo off
REM ============================================================================
REM Autotube - GUI Launcher
REM ============================================================================
REM Double-click this file to launch Autotube with the graphical interface
REM ============================================================================

REM Check if virtual environment exists
if not exist .venv (
    echo ERROR: Autotube is not installed!
    echo.
    echo Please run 'install.bat' first to set up Autotube.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and launch GUI
call .venv\Scripts\activate.bat
python -m project_name.cli gui

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred while running Autotube.
    pause
)
