#!/bin/bash
# ============================================================================
# Autotube - One-Click Installer (Unix/Linux/macOS)
# ============================================================================
# This script automatically sets up Autotube on your system.
# Run: chmod +x install.sh && ./install.sh
# ============================================================================

echo ""
echo "============================================================================"
echo "                    AUTOTUBE - One-Click Installer"
echo "============================================================================"
echo ""
echo "This installer will:"
echo "  1. Check for Python 3.11"
echo "  2. Create a virtual environment"
echo "  3. Install all dependencies"
echo "  4. Set up the application"
echo ""
echo "NOTE: This project requires Python 3.11 specifically due to"
echo "      OpenL3 dependency constraints. Python 3.12+ is not supported yet."
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Check if Python is available
echo ""
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.11:"
    echo "  Ubuntu/Debian: sudo apt-get install python3.11"
    echo "  macOS: brew install python@3.11"
    echo "  Other: https://www.python.org/downloads/release/python-3119/"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check if virtual environment exists
echo ""
echo "[2/4] Setting up virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists."
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf .venv
        echo "Creating new virtual environment..."
        python3 -m venv .venv
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to create virtual environment!"
            exit 1
        fi
    else
        echo "Keeping existing virtual environment."
    fi
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment!"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment!"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "[3/4] Installing dependencies..."
echo "This may take several minutes. Please be patient..."
echo ""
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some dependencies may have failed to install."
    echo "The application might still work, but some features may be unavailable."
    echo ""
fi

# Install package in editable mode
echo ""
echo "[4/4] Installing Autotube..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Autotube!"
    exit 1
fi

echo ""
echo "============================================================================"
echo "                    INSTALLATION COMPLETE!"
echo "============================================================================"
echo ""
echo "Autotube has been successfully installed!"
echo ""
echo "To run Autotube:"
echo "  - GUI mode: ./autotube.sh"
echo "  - CLI mode: ./autotube-cli.sh"
echo "  - Or activate venv: source .venv/bin/activate && autotube --help"
echo ""
echo "For more information, see README.md"
echo ""
echo "============================================================================"
echo ""
