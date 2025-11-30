#!/usr/bin/env python
"""
SonicSleep Pro - Simple Application Launcher

This script launches the SonicSleep Pro application with the dashboard UI.
Simply run this script to start the application:
    python scripts/run.py
"""

import sys

from project_name.gui.main import main

if __name__ == "__main__":
    # Start the application directly
    sys.exit(main())
