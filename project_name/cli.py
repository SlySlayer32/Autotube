"""
Sleep Sound Mixer - Command-Line Interface (CLI)
A tool for processing and mixing ambient audio for sleep and relaxation.
"""

import argparse
import logging
import os

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.processor import SoundProcessor
from project_name.core.visualizer import Visualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("sound_tool.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the sound tool.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Sleep Sound Mixer Tool")
    parser.add_argument(
        "--input",
        type=str,
        default="input_clips",
        help="Input folder containing raw audio files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_mixes",
        help="Output folder for final mixes",
    )
    parser.add_argument(
        "--duration", type=int, default=60, help="Duration of mix in minutes"
    )
    parser.add_argument(
        "--mix-type",
        type=str,
        default="sleep",
        choices=["sleep", "focus", "relax"],
        help="Type of mix to create",
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Create visualizations of audio files"
    )
    parser.add_argument(
        "--freesound",
        action="store_true",
        help="Interact with Freesound API for searching and downloading audio clips",
    )
    parser.add_argument(
        "--gui", action="store_true", help="Launch the graphical user interface"
    )
    parser.add_argument(
        "--classic-ui",
        action="store_true",
        help="Use the classic UI instead of the new dashboard (only with --gui)",
    )

    args = parser.parse_args()

    # Launch GUI if requested
    if args.gui:
        launch_gui(use_classic=args.classic_ui)
        return

    if args.freesound:
        interact_with_freesound_api()
        return

    # Initialize processor and create mix
    processor = SoundProcessor(input_folder=args.input, output_folder=args.output)
    processor.preprocess_audio()
    processor.analyze_clips()
    mix_path = processor.create_mix(
        target_duration_min=args.duration, mix_type=args.mix_type
    )

    logger.info(f"Mix created at: {mix_path}")

    # Optionally visualize audio files
    if args.visualize:
        visualizer = Visualizer()
        visualizer.visualize_audio_files(args.input)


def launch_gui(use_classic=False):
    """
    Launch the graphical user interface.

    Args:
        use_classic (bool): If True, use the classic UI instead of the new dashboard
    """
    from tkinter import Tk

    if use_classic:
        from project_name.gui.gui import SoundToolGUI

        root = Tk()
        app = SoundToolGUI(root)
    else:
        from project_name.gui.dashboard_app import SoundDashboardApp

        root = Tk()
        app = SoundDashboardApp(root)

    root.mainloop()


def interact_with_freesound_api():
    """
    Interact with Freesound API for searching and downloading audio clips.
    """
    # Get API key and search query from user input
    api_key = input("Enter your Freesound API key: ").strip()
    if not api_key:
        print("API key is required.")
        return

    query = input("Enter search query (e.g., 'ambient rain'): ").strip()
    if not query:
        print("Search query is required.")
        return

    # Initialize Freesound API client
    api_client = FreesoundAPI(api_key)

    # Perform search
    print(f"Searching for '{query}'...")
    results = api_client.search(
        query=query, page_size=5
    )  # Limit to 5 results for simplicity

    if not results.get("results"):
        print("No results found.")
        return

    # Display results
    print("Search results:")
    for idx, result in enumerate(results["results"], start=1):
        print(
            f"{idx}. {result['name']} (ID: {result['id']}, Duration: {result['duration']}s)"
        )

    # Ask user to select a sound to download
    try:
        choice = int(input("Enter the number of the sound to download (0 to cancel): "))
        if choice == 0:
            print("Download canceled.")
            return

        selected_sound = results["results"][choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    # Download the selected sound
    sound_id = selected_sound["id"]
    print(f"Downloading sound ID {sound_id}...")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "processed_clips")
    os.makedirs(output_dir, exist_ok=True)

    file_path = api_client.download(sound_id)
    if file_path:
        new_path = os.path.join(output_dir, os.path.basename(file_path))
        os.rename(file_path, new_path)
        print(f"Sound downloaded to: {new_path}")
    else:
        print("Failed to download sound.")


if __name__ == "__main__":
    main()
