#!/bin/bash
# ============================================================================
# Autotube - CLI Launcher (Unix/Linux/macOS)
# ============================================================================
# Run this script to launch Autotube command-line interface
# Usage: ./autotube-cli.sh
# ============================================================================

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Autotube is not installed!"
    echo ""
    echo "Please run './install.sh' first to set up Autotube."
    echo ""
    exit 1
fi

# Activate virtual environment and show help
source .venv/bin/activate
echo ""
echo "============================================================================"
echo "                    AUTOTUBE - Command-Line Interface"
echo "============================================================================"
echo ""
autotube --help
echo ""
echo "============================================================================"
echo ""
echo "Type 'autotube COMMAND --help' for help with a specific command."
echo "Examples:"
echo "  autotube gui           - Launch graphical interface"
echo "  autotube status        - Check system status"
echo "  autotube mix           - Create audio mix"
echo "  autotube video         - Generate video"
echo "  autotube pipeline      - Run full pipeline"
echo ""
echo "============================================================================"
echo ""

# Keep shell open
exec $SHELL
