#!/usr/bin/env python
"""
SonicSleep Pro - Project Cleanup Script

This script cleans up cache files, __pycache__ directories, and other temporary
files from the project to keep things tidy.

Usage:
    python scripts/clean.py [--all]

Options:
    --all    Also remove virtual environment and egg-info directories
"""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Project cleanup script")
    parser.add_argument(
        "--all", action="store_true", help="Also clean virtual environment and egg-info"
    )
    args = parser.parse_args()

    # Get the project root directory
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    print(f"Cleaning project at: {project_root}")

    # Files and directories to always clean
    to_clean = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/.coverage",
        "**/.mypy_cache",
        "**/htmlcov",
        "**/build",
        "**/dist",
        "**/.DS_Store",
    ]

    # Additional items to clean if --all is specified
    if args.all:
        to_clean.extend(
            [
                "**/node_modules",
                "**/venv",
                "**/.venv",
                "**/*.egg-info",
            ]
        )

    # Track what's been cleaned
    cleaned = []

    # Find and remove the specified patterns
    for pattern in to_clean:
        for path in project_root.glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    cleaned.append(
                        f"Removed directory: {path.relative_to(project_root)}"
                    )
                else:
                    path.unlink()
                    cleaned.append(f"Removed file: {path.relative_to(project_root)}")
            except Exception as e:
                print(f"Error removing {path}: {e}")

    # Print summary
    if cleaned:
        print("\nCleanup Summary:")
        for item in cleaned:
            print(f"  {item}")
        print(f"\nRemoved {len(cleaned)} items.")
    else:
        print("Nothing to clean.")


if __name__ == "__main__":
    main()
