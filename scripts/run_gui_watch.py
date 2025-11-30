import logging
import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Project paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
GUI_MAIN_SCRIPT = PROJECT_ROOT / "project_name" / "gui" / "main.py"
WATCH_DIRS = [
    PROJECT_ROOT / "project_name" / "gui",
    PROJECT_ROOT / "project_name" / "core",  # Watch core logic too
]

process = None


def start_gui():
    """Starts the GUI application in a subprocess."""
    global process
    if process:
        logging.info("Terminating existing GUI process...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logging.warning("GUI process did not terminate gracefully, killing.")
            process.kill()
        process = None

    logging.info(f"Starting GUI: {GUI_MAIN_SCRIPT}")
    # Ensure it runs with the correct Python interpreter from the venv
    # and from the project root directory
    python_executable = sys.executable  # Uses the interpreter running this script
    process = subprocess.Popen(
        [python_executable, str(GUI_MAIN_SCRIPT)], cwd=PROJECT_ROOT
    )
    logging.info(f"GUI process started (PID: {process.pid}).")


class GuiChangeHandler(FileSystemEventHandler):
    """Restarts the GUI when relevant Python files change."""

    def __init__(self):
        self.last_restart = time.time()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            # Debounce restarts
            if time.time() - self.last_restart > 2.0:
                logging.info(f"Change detected in {event.src_path}, restarting GUI...")
                start_gui()
                self.last_restart = time.time()


if __name__ == "__main__":
    logging.info("Starting GUI watcher...")
    start_gui()  # Start initial instance

    event_handler = GuiChangeHandler()
    observer = Observer()
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=True)
            logging.info(f"Watching directory: {watch_dir}")
        else:
            logging.warning(f"Watch directory not found: {watch_dir}")

    if not observer.emitters:
        logging.error("No valid directories found to watch. Exiting.")
        sys.exit(1)

    observer.start()
    logging.info("Watching for file changes to restart GUI (Ctrl+C to exit)...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down GUI watcher...")
        if process:
            process.terminate()
            process.wait()
        observer.stop()

    observer.join()
    logging.info("GUI watcher stopped.")
