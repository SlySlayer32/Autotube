@echo off
setlocal

REM Define the virtual environment directory
set VENV_DIR=.venv

REM Check if Python is available
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in the system PATH. Please install Python.
    goto :eof
)

REM Check if the virtual environment directory exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Error: Virtual environment not found at %VENV_DIR%.
    echo Please run 'npm run dev:setup' first to create it and install dependencies.
    goto :eof
)

REM Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    goto :eof
)

REM Run the GUI watcher script
echo Starting GUI with hot-reload watcher...
python scripts/run_gui_watch.py

echo Script finished.
endlocal
