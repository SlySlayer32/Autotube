#!/bin/bash
# ============================================================================
# Autotube - GUI Launcher (Unix/Linux/macOS)
# ============================================================================
# Run this script to launch Autotube with the graphical interface
# Usage: ./autotube.sh
# ============================================================================

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Autotube is not installed!"
    echo ""
    echo "Please run './install.sh' first to set up Autotube."
    echo ""
    exit 1
fi

# Activate virtual environment and launch GUI
source .venv/bin/activate
python -m project_name.cli gui

# Check for errors
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred while running Autotube."
    read -p "Press Enter to exit..."
fi
