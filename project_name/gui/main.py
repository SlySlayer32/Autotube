# Main entry point for the Sleep Sound Mixer application
import argparse
from tkinter import Tk

from project_name.gui.dashboard_app import SoundDashboardApp
from project_name.gui.gui import SoundToolGUI
from unified_sleep_audio_gui import UnifiedSleepAudioGUI


def main():
    """Main function to run the application"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SonicSleep Pro Sound Mixer")
    parser.add_argument(
        "--use-classic",
        action="store_true",
        help="Use the classic interface instead of the unified interface",
    )
    parser.add_argument(
        "--use-dashboard",
        action="store_true",
        help="Use the dashboard interface instead of the unified interface",
    )
    args, unknown = parser.parse_known_args()

    root = Tk()

    # Choose which interface to use
    if args.use_classic:
        # Use the classic interface
        app = SoundToolGUI(root)
    elif args.use_dashboard:
        # Use the dashboard interface
        app = SoundDashboardApp(root)
    else:
        # Use the new unified step-by-step interface (DEFAULT)
        app = UnifiedSleepAudioGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
