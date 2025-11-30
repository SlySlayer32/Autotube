"""
SonicSleep Pro - Test Runner with Auto-Reload

This script watches for changes in Python files and runs relevant tests
automatically when changes are detected.

Run this script to start test-driven development:
    python scripts/test_watch.py
"""

import argparse
import logging
import os  # Added missing import
import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Get project paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROJECT_PATH = PROJECT_ROOT / "project_name"
TESTS_PATH = PROJECT_ROOT / "tests"


class TestRunner(FileSystemEventHandler):
    """Handles running tests when Python files change."""

    def __init__(self, test_path="tests", run_all_initially=True):
        self.test_path = test_path
        self.last_run = time.time() - 10  # Allow immediate first run

        # Run all tests initially if requested
        if run_all_initially:
            self.run_tests()

    def run_tests(self):
        """Run all tests defined in pytest.ini."""
        # Command now simply runs pytest, relying on pytest.ini for paths/options
        cmd = [sys.executable, "-m", "pytest"]

        logging.info(f"Running tests: {' '.join(cmd)}")
        # Ensure pytest runs from the project root directory and PYTHONPATH is set
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        subprocess.run(cmd, cwd=PROJECT_ROOT, env=env)
        self.last_run = time.time()

    def on_modified(self, event):
        """Handle file modification events."""
        # Only run tests for Python files, ignore cache directories
        if event.src_path.endswith(".py") and not any(
            p in event.src_path for p in ["__pycache__", ".pytest_cache"]
        ):
            # Debounce to prevent multiple test runs
            if time.time() - self.last_run > 2.0:  # 2-second debounce
                logging.info(f"Change detected in {event.src_path}")
                # Always run all tests upon detecting a change in any .py file
                self.run_tests()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SonicSleep Pro Test Runner")
    parser.add_argument(
        "--no-initial-run",
        action="store_true",
        help="Skip running all tests on startup",
    )
    parser.add_argument(
        "--path",
        type=str,
        default="tests",
        help="Path to test directory or specific test file",
    )
    args = parser.parse_args()

    logging.info("Starting test watcher...")
    event_handler = TestRunner(
        test_path=args.path, run_all_initially=not args.no_initial_run
    )

    observer = Observer()
    observer.schedule(event_handler, str(PROJECT_PATH), recursive=True)
    observer.schedule(event_handler, str(TESTS_PATH), recursive=True)
    observer.start()

    try:
        logging.info("Watching for file changes (Ctrl+C to exit)...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down test watcher...")
        observer.stop()

    observer.join()
    logging.info("Test watcher stopped.")
