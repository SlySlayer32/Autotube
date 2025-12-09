@echo off
REM ============================================================================
REM Autotube - CLI Launcher
REM ============================================================================
REM Double-click this file to launch Autotube command-line interface
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

REM Activate virtual environment and show help
call .venv\Scripts\activate.bat
echo.
echo ============================================================================
echo                    AUTOTUBE - Command-Line Interface
echo ============================================================================
echo.
autotube --help
echo.
echo ============================================================================
echo.
echo Type 'autotube COMMAND --help' for help with a specific command.
echo Examples:
echo   autotube gui           - Launch graphical interface
echo   autotube status        - Check system status
echo   autotube mix           - Create audio mix
echo   autotube video         - Generate video
echo   autotube pipeline      - Run full pipeline
echo.
echo Press Ctrl+C to exit
echo ============================================================================
echo.

REM Keep the command prompt open
cmd /k
