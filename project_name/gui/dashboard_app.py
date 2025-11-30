"""
SonicSleep Pro Dashboard Application

This module provides the main dashboard application for the SonicSleep Pro
audio processing tool.
"""

import logging
import tkinter as tk

from project_name.gui.dashboard import Dashboard

logger = logging.getLogger(__name__)


class SoundDashboardApp:
    """Application using the dashboard for Sound Tool."""

    def __init__(self, root):
        self.root = root
        self.root.title("SonicSleep Pro Dashboard")
        self.root.geometry("1200x800")

        # Create the dashboard - it handles everything internally
        self.dashboard = Dashboard(root)

    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = SoundDashboardApp(root)
    app.run()


if __name__ == "__main__":
    main()
