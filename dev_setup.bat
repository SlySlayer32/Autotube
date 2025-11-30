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
echo Checking for virtual environment at %VENV_DIR%...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        goto :eof
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment found.
)

REM Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    goto :eof
)

REM Install/update dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements.txt.
    goto :eof
)
echo Dependencies installed successfully.

REM Install the project in editable mode
echo Installing project in editable mode...
pip install -e .
if %errorlevel% neq 0 (
    echo Error: Failed to install the project in editable mode.
    goto :eof
)
echo Project installed successfully.

REM Run Ruff linting and formatting
echo Running Ruff check and format...
ruff check --fix .
if %errorlevel% neq 0 (
    echo Warning: Ruff check encountered issues.
)
ruff format .
if %errorlevel% neq 0 (
    echo Warning: Ruff format encountered issues.
)
echo Ruff check and format completed.

REM Create a PowerShell profile script to auto-activate venv
echo Setting up automatic virtual environment activation...
set PROFILE_DIR=%USERPROFILE%\Documents\WindowsPowerShell
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

set PROFILE_FILE=%PROFILE_DIR%\Microsoft.PowerShell_profile.ps1
set PROJECT_DIR=%CD%

REM Create or update PowerShell profile
echo # Auto-activate virtual environment for this project > "%PROFILE_FILE%"
echo if (Get-Location).Path -eq "%PROJECT_DIR%" { >> "%PROFILE_FILE%"
echo     if (Test-Path ".\.venv\Scripts\Activate.ps1") { >> "%PROFILE_FILE%"
echo         ^& ".\.venv\Scripts\Activate.ps1" >> "%PROFILE_FILE%"
echo         Write-Host "Virtual environment activated for project" -ForegroundColor Green >> "%PROFILE_FILE%"
echo     } >> "%PROFILE_FILE%"
echo } >> "%PROFILE_FILE%"

REM Also create a batch file for easy activation
echo @echo off > activate_env.bat
echo call ".venv\Scripts\activate.bat" >> activate_env.bat
echo echo Virtual environment activated! >> activate_env.bat
echo cmd /k >> activate_env.bat

echo.
echo Development environment setup complete!
echo.
echo To activate the virtual environment in new terminals:
echo   1. PowerShell will auto-activate when you cd to this directory
echo   2. Or run: .\activate_env.bat
echo   3. Or manually run: .\.venv\Scripts\Activate.ps1
echo.
echo Starting the test watcher...
python scripts/test_watch.py

echo Script finished.
endlocal
