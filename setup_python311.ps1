# Project Python Version Control - PowerShell Version
# This script ensures the project always uses Python 3.11

$PYTHON_311_PATH = "C:\Users\Sly\AppData\Local\Programs\Python\Python311\python.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PROJECT PYTHON VERSION CONTROL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Python 3.11 installation..." -ForegroundColor Yellow

if (-not (Test-Path $PYTHON_311_PATH)) {
    Write-Host "ERROR: Python 3.11 not found at expected location!" -ForegroundColor Red
    Write-Host "Expected: $PYTHON_311_PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11 or update the path in this script." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Python 3.11 found: $PYTHON_311_PATH" -ForegroundColor Green

# Display version
Write-Host ""
Write-Host "Python version:" -ForegroundColor Yellow
& $PYTHON_311_PATH --version

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   RECREATING VIRTUAL ENVIRONMENT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Remove existing virtual environment
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

# Create new virtual environment with Python 3.11
Write-Host "Creating new virtual environment with Python 3.11..." -ForegroundColor Yellow
& $PYTHON_311_PATH -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   INSTALLING DEPENDENCIES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Install core dependencies first
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
pip install "numpy>=1.21.0,<1.25.0"
pip install "scipy>=1.9.0,<1.12.0"

# Install TensorFlow (compatible with Python 3.11)
Write-Host "Installing TensorFlow..." -ForegroundColor Yellow
pip install "tensorflow>=2.10.0,<2.16.0"
pip install "tensorflow-hub>=0.14.0,<0.16.0"

# Install OpenL3
Write-Host "Installing OpenL3..." -ForegroundColor Yellow
pip install openl3

# Install remaining dependencies
Write-Host "Installing remaining dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VERIFICATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Testing critical imports..." -ForegroundColor Yellow
$testScript = @"
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
"@

python -c $testScript

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Dependency installation failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Project successfully configured for Python 3.11" -ForegroundColor Green
Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
Write-Host "✅ All dependencies installed" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment in future sessions, run:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run the project:" -ForegroundColor Yellow
Write-Host "  python cli.py" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"
