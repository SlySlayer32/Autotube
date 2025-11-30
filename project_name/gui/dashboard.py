"""SonicSleep Pro Dashboard Interface.

This module provides the main dashboard interface for the application,
integrating all panels and components into a cohesive UI.
"""

import logging
import tkinter as tk
from tkinter import ttk

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.mix_creator import MixCreator
from project_name.core.processor import SoundProcessor
from project_name.core.visualizer import Visualizer
from project_name.gui.panels import (
    AnalysisPanel,
    AudioProcessingPanel,
    InputProcessingPanel,
    TherapeuticAudioPanel,
    EnhancedTherapeuticPanel,
    SettingsPanel,
)

logger = logging.getLogger(__name__)


class SidebarPanel:
    """Sidebar panel to navigate between different dashboard sections."""

    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        # Create sidebar frame
        self.frame = ttk.Frame(parent, width=200, relief="raised", padding="10")
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Logo/Title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill=tk.X, pady=10)

        ttk.Label(title_frame, text="SonicSleep", font=("Arial", 14, "bold")).pack(
            side=tk.LEFT
        )
        ttk.Label(title_frame, text="Pro", font=("Arial", 14)).pack(side=tk.LEFT)

        # Separator
        ttk.Separator(self.frame).pack(fill=tk.X, pady=10)

        # Navigation buttons
        self.buttons = {}

        # Input panel button
        self.buttons["input"] = ttk.Button(
            self.frame,
            text="Input Processing",
            width=20,
            command=lambda: self.callback("input"),
        )
        self.buttons["input"].pack(fill=tk.X, pady=5)

        # Analysis panel button
        self.buttons["analysis"] = ttk.Button(
            self.frame,
            text="Analysis",
            width=20,
            command=lambda: self.callback("analysis"),
        )
        self.buttons["analysis"].pack(fill=tk.X, pady=5)        # Audio processing panel button
        self.buttons["audio"] = ttk.Button(
            self.frame,
            text="Audio Processing",
            width=20,
            command=lambda: self.callback("audio"),
        )
        self.buttons["audio"].pack(fill=tk.X, pady=5)

        # Therapeutic audio panel button (NEW 2024 RESEARCH)
        self.buttons["therapeutic"] = ttk.Button(
            self.frame,
            text="🧠 Therapeutic Audio",
            width=20,
            command=lambda: self.callback("therapeutic"),
        )
        self.buttons["therapeutic"].pack(fill=tk.X, pady=5)

        # Settings panel button
        self.buttons["settings"] = ttk.Button(
            self.frame,
            text="Settings",
            width=20,
            command=lambda: self.callback("settings"),
        )
        self.buttons["settings"].pack(fill=tk.X, pady=5)

        # Separator
        ttk.Separator(self.frame).pack(fill=tk.X, pady=10)

        # Status info
        self.status_var = tk.StringVar(value="Ready")
        status_frame = ttk.Frame(self.frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

    def set_active(self, panel_name):
        """Set the active panel button."""
        for name, button in self.buttons.items():
            if name == panel_name:
                button.state(["pressed"])
            else:
                button.state(["!pressed"])

    def set_status(self, status):
        """Set the status text."""
        self.status_var.set(status)


class Dashboard:
    """Main dashboard interface for SonicSleep Pro."""

    def __init__(self, root):
        """Initialize the dashboard."""
        self.root = root
        self.root.title("SonicSleep Pro Dashboard")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 700)

        # Set up the main components
        self.setup_components()

        # Configure grid layout
        self.root.columnconfigure(1, weight=1)  # Content column expands
        self.root.rowconfigure(0, weight=1)  # Main row expands

        # Initialize UI
        self.setup_ui()        # Switch to therapeutic panel by default (2024 research features)
        self.show_panel("therapeutic")

        # Set up periodic callbacks
        self.setup_periodic_callbacks()

    def setup_components(self):
        """Set up the application components."""        # Core components
        self.processor = SoundProcessor()
        self.mix_creator = MixCreator()
        self.visualizer = Visualizer()

        # Optional API client - will be initialized when user provides key
        self.freesound_api = None

    def setup_ui(self):
        """Set up the user interface."""
        # Create sidebar for navigation
        self.sidebar = SidebarPanel(self.root, self.show_panel)

        # Create main content frame
        self.content_frame = ttk.Frame(self.root, padding="10")
        self.content_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5
        )

        # Create panel container
        self.panel_container = ttk.Frame(self.content_frame)
        self.panel_container.pack(fill=tk.BOTH, expand=True)

        # Initialize panels
        self.panels = {}

        # Create status bar at the bottom
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_message = tk.StringVar()
        self.status_message.set("Ready")
        ttk.Label(
            self.status_bar, textvariable=self.status_message, padding=(10, 2)
        ).pack(side=tk.LEFT)

        # Version info
        version = "1.0.0"  # Should be imported from a version module
        ttk.Label(self.status_bar, text=f"v{version}", padding=(10, 2)).pack(
            side=tk.RIGHT
        )

    def show_panel(self, panel_name):
        """Show the specified panel."""
        logger.info(f"Switching to {panel_name} panel")

        # Update sidebar selection
        self.sidebar.set_active(panel_name)        # Hide all panels
        for panel in self.panels.values():
            panel.pack_forget()

        # Create the panel if it doesn't exist
        if panel_name not in self.panels:
            panel_frame = ttk.Frame(self.panel_container)
            panel_frame.content_frame = ttk.Frame(panel_frame)
            panel_frame.content_frame.pack(fill=tk.BOTH, expand=True)

            if panel_name == "input":
                InputProcessingPanel(panel_frame)
                panel_title = "Input Processing"
            elif panel_name == "analysis":
                AnalysisPanel(panel_frame)
                panel_title = "Audio Analysis"
            elif panel_name == "audio":
                AudioProcessingPanel(panel_frame)
                panel_title = "Audio Processing"
            elif panel_name == "therapeutic":
                EnhancedTherapeuticPanel(panel_frame)
                panel_title = "🧠 Enhanced Therapeutic Audio - 2024 Research"
            elif panel_name == "settings":
                SettingsPanel(panel_frame)
                panel_title = "Settings"
            else:
                raise ValueError(f"Unknown panel: {panel_name}")

            # Set panel header
            header_frame = ttk.Frame(panel_frame)
            header_frame.pack(fill=tk.X, before=panel_frame.content_frame)

            ttk.Label(header_frame, text=panel_title, font=("Arial", 16, "bold")).pack(
                side=tk.LEFT, pady=10
            )
            ttk.Separator(header_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

            self.panels[panel_name] = panel_frame

        # Show the requested panel
        self.panels[panel_name].pack(fill=tk.BOTH, expand=True)
        self.status_message.set(f"Viewing {panel_name} panel")

    def setup_periodic_callbacks(self):
        """Set up periodic callbacks for updating UI."""
        # Check processor status every second
        self.root.after(1000, self.update_processor_status)

        # Update system resources every 5 seconds
        self.root.after(5000, self.update_system_resources)

    def update_processor_status(self):
        """Update the processor status in the UI."""
        # In a real implementation, we would check the processor status
        # and update the UI accordingly
        self.root.after(1000, self.update_processor_status)

    def update_system_resources(self):
        """Update system resource usage in the UI."""
        # In a real implementation, we would check system resources
        # and update the UI accordingly
        self.root.after(5000, self.update_system_resources)


def run_dashboard():
    """Run the dashboard application."""
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    run_dashboard()
