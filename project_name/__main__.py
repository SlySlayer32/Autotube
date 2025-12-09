"""
Autotube - Package entry point for python -m execution.

This module allows running the package directly with:
    python -m project_name

It will launch the CLI by default.
"""

from project_name.cli import main

if __name__ == "__main__":
    main()
