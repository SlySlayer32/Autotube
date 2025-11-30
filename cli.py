#!/usr/bin/env python3
"""
SonicSleep Pro - CLI Entry Point

This is a convenience script for running the command-line interface.
Simply execute this file to start the CLI:
    python cli.py

This is equivalent to running:
    python -m project_name.cli
"""

# STRICT Python version control - must be first import
try:
    from python_version_control import check_python_version
    check_python_version()
except ImportError:
    print("❌ Python version control module not found!")
    print("🔧 Run setup_python311.ps1 to configure the project properly")
    exit(1)
except Exception as e:
    print(f"❌ Python version check failed: {e}")
    exit(1)

from project_name.cli import main

if __name__ == "__main__":
    main()
