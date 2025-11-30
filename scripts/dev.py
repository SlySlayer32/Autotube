"""
SonicSleep Pro - Development Script with Hot Reloading

This script provides a hot-reloading development environment
that automatically restarts the application when Python files change.

Simply run this script to start developing with auto-reload:
    python scripts/dev.py

The dashboard UI will be launched by default.
"""

import logging
import os
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


class AppReloader(FileSystemEventHandler):
    """Handles hot reloading of the application when Python files change."""

    def __init__(self):
        self.process = None
        self.last_restart = time.time()
        self.restart_app()

    def restart_app(self):
        """Restart the application process."""
        if self.process:
            logging.info("Stopping application...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logging.warning("Application did not terminate gracefully, forcing...")
                self.process.kill()

        # Start the application with the dashboard UI
        cmd = [sys.executable, "-m", "project_name.gui.main"]

        logging.info("Starting SonicSleep Pro Dashboard...")
        env = os.environ.copy()
        self.process = subprocess.Popen(cmd, env=env)
        self.last_restart = time.time()

    def on_modified(self, event):
        """Handle file modification events."""
        # Only restart for Python files and avoid certain directories
        if event.src_path.endswith(".py") and not any(
            p in event.src_path for p in ["__pycache__", ".pytest_cache"]
        ):
            # Debounce to prevent multiple restarts for the same change
            if time.time() - self.last_restart > 1.0:
                logging.info(f"Change detected in {event.src_path}")
                self.restart_app()


if __name__ == "__main__":
    logging.info("Starting development environment with hot-reloading...")
    event_handler = AppReloader()
    observer = Observer()
    observer.schedule(event_handler, str(PROJECT_PATH), recursive=True)
    observer.start()

    try:
        logging.info("Watching for file changes (Ctrl+C to exit)...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down development environment...")
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()

    observer.join()
    logging.info("Development environment stopped.")
