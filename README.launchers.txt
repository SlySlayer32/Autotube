===============================================================================
                        AUTOTUBE LAUNCHER SCRIPTS
===============================================================================

This folder contains simple launcher scripts that make running Autotube
as easy as double-clicking an executable file!

INSTALLATION:
-------------

  Windows:      Double-click "install.bat"
  Mac/Linux:    Run "./install.sh" in terminal

RUNNING AUTOTUBE:
-----------------

After installation, you can launch Autotube in two ways:

1. GUI MODE (Graphical User Interface) - Recommended for most users
   
   Windows:      Double-click "autotube.bat"
   Mac/Linux:    Run "./autotube.sh" in terminal

2. CLI MODE (Command-Line Interface) - For advanced users and automation
   
   Windows:      Double-click "autotube-cli.bat"
   Mac/Linux:    Run "./autotube-cli.sh" in terminal

WHAT EACH FILE DOES:
--------------------

  install.bat / install.sh
    - One-click installer that sets up everything automatically
    - Creates virtual environment
    - Installs all dependencies
    - Sets up the application

  autotube.bat / autotube.sh
    - Launches Autotube with graphical interface
    - Best for visual workflow and easy access to all features

  autotube-cli.bat / autotube-cli.sh
    - Launches Autotube command-line interface
    - Shows available commands
    - Best for automation and scripting

NEED HELP?
----------

  Quick Start:    See QUICKSTART.md
  Installation:   See INSTALL.md
  Documentation:  See README.md

TROUBLESHOOTING:
----------------

  Problem: "Python is not recognized"
  Solution: Install Python 3.11+ from https://www.python.org/downloads/
           Make sure to check "Add Python to PATH" during installation

  Problem: "Autotube is not installed"
  Solution: Run the installer first (install.bat or ./install.sh)

  Problem: GUI doesn't launch
  Solution: Make sure FFmpeg is installed and Python dependencies are set up
           Run "autotube status" command to check

===============================================================================
