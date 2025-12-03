"""
Autotube - Command-Line Interface (CLI)

A tool for processing, mixing ambient audio, generating videos,
and uploading to YouTube for sleep and relaxation content.
"""

import logging
import os

import click

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("autotube.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="1.0.0", prog_name="autotube")
def cli():
    """
    Autotube - Automated YouTube Video Generation for Sleep/Relaxation Content.

    A complete workflow tool for creating and uploading ambient sound videos
    to YouTube, including audio mixing, video generation, and metadata
    optimization.
    """
    pass


@cli.command()
@click.option(
    "--input", "-i",
    default="input_clips",
    help="Input folder containing raw audio files",
)
@click.option(
    "--output", "-o",
    default="output_mixes",
    help="Output folder for final mixes",
)
@click.option(
    "--duration", "-d",
    default=60,
    type=int,
    help="Duration of mix in minutes",
)
@click.option(
    "--mix-type", "-t",
    default="sleep",
    type=click.Choice(["sleep", "focus", "relax"]),
    help="Type of mix to create",
)
def mix(input, output, duration, mix_type):
    """Create an audio mix from input clips."""
    from project_name.core.processor import SoundProcessor

    click.echo(f"Creating {mix_type} mix ({duration} minutes)...")

    processor = SoundProcessor(input_folder=input, output_folder=output)
    # Preprocess all audio files in the input folder
    for filename in os.listdir(input):
        file_path = os.path.join(input, filename)
        if os.path.isfile(file_path):
            processor.preprocess_audio(file_path)
    processor.analyze_clips()
    mix_path = processor.create_mix(
        target_duration_min=duration, mix_type=mix_type
    )

    if mix_path:
        click.echo(click.style(f"✓ Mix created: {mix_path}", fg="green"))
    else:
        click.echo(click.style("✗ Mix creation failed", fg="red"))


@cli.command()
@click.argument("audio_path", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    default="output_videos",
    help="Output folder for generated videos",
)
@click.option(
    "--title", "-t",
    default=None,
    help="Title text to display on video background",
)
@click.option(
    "--waveform", "-w",
    is_flag=True,
    help="Create video with waveform visualization",
)
def video(audio_path, output, title, waveform):
    """Generate a video from an audio file."""
    from project_name.core.video_generator import VideoGenerator

    click.echo(f"Generating video from: {audio_path}")

    try:
        generator = VideoGenerator(output_folder=output)

        if waveform:
            video_path = generator.generate_video_with_waveform(audio_path)
        else:
            video_path = generator.generate_video_from_audio(
                audio_path=audio_path,
                title_text=title,
            )

        if video_path:
            click.echo(click.style(f"✓ Video created: {video_path}", fg="green"))
        else:
            click.echo(click.style("✗ Video generation failed", fg="red"))

    except RuntimeError as e:
        click.echo(click.style(f"✗ Error: {e}", fg="red"))


@cli.command()
@click.argument("video_path", type=click.Path(exists=True))
@click.option(
    "--title", "-t",
    required=True,
    help="Video title",
)
@click.option(
    "--description", "-d",
    default="",
    help="Video description",
)
@click.option(
    "--tags",
    default="",
    help="Comma-separated list of tags",
)
@click.option(
    "--privacy",
    default="private",
    type=click.Choice(["public", "private", "unlisted"]),
    help="Privacy status for the video",
)
@click.option(
    "--credentials", "-c",
    default="client_secrets.json",
    help="Path to YouTube API client secrets file",
)
def upload(video_path, title, description, tags, privacy, credentials):
    """Upload a video to YouTube."""
    from project_name.api.youtube_uploader import YouTubeUploader

    click.echo(f"Uploading video: {video_path}")

    uploader = YouTubeUploader(client_secrets_file=credentials)

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    video_id = uploader.upload_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=tag_list,
        privacy_status=privacy,
    )

    if video_id:
        click.echo(click.style("✓ Upload successful!", fg="green"))
        click.echo(f"  Video ID: {video_id}")
        click.echo(f"  URL: https://www.youtube.com/watch?v={video_id}")
    else:
        click.echo(click.style("✗ Upload failed", fg="red"))


@cli.command()
@click.option(
    "--sound-type", "-s",
    default="Rain",
    help="Type of sound (e.g., Rain, Ocean, Nature)",
)
@click.option(
    "--duration", "-d",
    default=8,
    type=int,
    help="Duration in hours",
)
@click.option(
    "--purpose", "-p",
    default="sleep",
    type=click.Choice(["sleep", "focus", "relax"]),
    help="Purpose of the video",
)
@click.option(
    "--format", "-f",
    "output_format",
    default="text",
    type=click.Choice(["text", "json"]),
    help="Output format",
)
def metadata(sound_type, duration, purpose, output_format):
    """Generate SEO-optimized metadata for a video."""
    from project_name.core.metadata_generator import MetadataGenerator

    generator = MetadataGenerator()
    meta = generator.generate_complete_metadata(
        sound_type=sound_type,
        duration_hours=duration,
        purpose=purpose,
    )

    if output_format == "json":
        import json
        click.echo(json.dumps(meta, indent=2))
    else:
        click.echo("\n" + "=" * 60)
        click.echo(click.style("TITLE:", fg="cyan", bold=True))
        click.echo(meta["title"])
        click.echo("\n" + click.style("TAGS:", fg="cyan", bold=True))
        click.echo(", ".join(meta["tags"]))
        click.echo("\n" + click.style("DESCRIPTION:", fg="cyan", bold=True))
        desc = meta["description"]
        click.echo(desc[:500] + "..." if len(desc) > 500 else desc)
        click.echo("=" * 60)


@cli.command()
@click.option(
    "--sound-type", "-s",
    default="Rain",
    help="Type of sound (e.g., Rain, Ocean, Nature)",
)
@click.option(
    "--duration", "-d",
    default=60,
    type=int,
    help="Duration in minutes",
)
@click.option(
    "--mix-type", "-t",
    default="sleep",
    type=click.Choice(["sleep", "focus", "relax"]),
    help="Type of mix to create",
)
@click.option(
    "--privacy",
    default="private",
    type=click.Choice(["public", "private", "unlisted"]),
    help="YouTube privacy status",
)
@click.option(
    "--waveform", "-w",
    is_flag=True,
    help="Use waveform visualization",
)
@click.option(
    "--no-upload",
    is_flag=True,
    help="Skip YouTube upload",
)
@click.option(
    "--input", "-i",
    default="input_clips",
    help="Input folder for audio clips",
)
@click.option(
    "--output", "-o",
    default="output_mixes",
    help="Output folder for mixes",
)
@click.option(
    "--video-output",
    default="output_videos",
    help="Output folder for videos",
)
def pipeline(
    sound_type, duration, mix_type, privacy, waveform,
    no_upload, input, output, video_output
):
    """Run the complete Autotube pipeline (mix → video → upload)."""
    from project_name.core.orchestrator import AutotubeOrchestrator

    click.echo(click.style("Starting Autotube Pipeline", fg="cyan", bold=True))
    click.echo("=" * 50)

    orchestrator = AutotubeOrchestrator(
        input_folder=input,
        output_folder=output,
        video_folder=video_output,
    )

    results = orchestrator.run_full_pipeline(
        sound_type=sound_type,
        duration_minutes=duration,
        mix_type=mix_type,
        privacy_status=privacy,
        use_waveform=waveform,
        upload=not no_upload,
    )

    click.echo("\n" + "=" * 50)
    click.echo(click.style("Pipeline Results:", fg="cyan", bold=True))

    if results["success"]:
        click.echo(click.style("✓ Pipeline completed successfully!", fg="green"))
        if results["audio_path"]:
            click.echo(f"  Audio: {results['audio_path']}")
        if results["video_path"]:
            click.echo(f"  Video: {results['video_path']}")
        if results["video_id"]:
            click.echo(f"  YouTube ID: {results['video_id']}")
            click.echo(
                f"  URL: https://www.youtube.com/watch?v={results['video_id']}"
            )
    else:
        click.echo(click.style("✗ Pipeline failed", fg="red"))
        for error in results.get("errors", []):
            click.echo(f"  - {error}")


@cli.command()
@click.option(
    "--num-videos", "-n",
    default=7,
    type=int,
    help="Number of videos to plan",
)
@click.option(
    "--format", "-f",
    "output_format",
    default="table",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
def plan(num_videos, output_format):
    """Plan content for multiple videos."""
    from project_name.core.orchestrator import AutotubeOrchestrator

    orchestrator = AutotubeOrchestrator()
    content_plan = orchestrator.plan_content(num_videos=num_videos)

    if output_format == "json":
        import json
        click.echo(json.dumps(content_plan, indent=2))
    else:
        click.echo("\n" + click.style("Content Plan", fg="cyan", bold=True))
        click.echo("=" * 70)
        click.echo(
            f"{'#':<3} {'Sound Type':<15} {'Purpose':<10} {'Date':<12} "
            f"{'Time':<8} {'Duration':<8}"
        )
        click.echo("-" * 70)
        for item in content_plan:
            click.echo(
                f"{item['video_number']:<3} {item['sound_type']:<15} "
                f"{item['purpose']:<10} {item['scheduled_date']:<12} "
                f"{item['optimal_time']:<8} {item['duration_hours']}h"
            )
        click.echo("=" * 70)


@cli.command()
def status():
    """Show current Autotube status."""
    from project_name.core.orchestrator import AutotubeOrchestrator

    orchestrator = AutotubeOrchestrator()
    status_info = orchestrator.get_status()

    click.echo("\n" + click.style("Autotube Status", fg="cyan", bold=True))
    click.echo("=" * 40)
    click.echo(f"Input folder:  {status_info['input_folder']}")
    click.echo(f"  Files: {status_info['input_files']}")
    click.echo(f"Output folder: {status_info['output_folder']}")
    click.echo(f"  Files: {status_info['output_files']}")
    click.echo(f"Video folder:  {status_info['video_folder']}")
    click.echo(f"  Files: {status_info['video_files']}")
    click.echo("=" * 40)


@cli.command()
@click.option("--classic", is_flag=True, help="Use classic UI instead of dashboard")
def gui(classic):
    """Launch the graphical user interface."""
    launch_gui(use_classic=classic)


@cli.command()
def freesound():
    """Interactive Freesound API search and download."""
    interact_with_freesound_api()


# Legacy support functions
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
        SoundToolGUI(root)
    else:
        from project_name.gui.dashboard_app import SoundDashboardApp

        root = Tk()
        SoundDashboardApp(root)

    root.mainloop()


def interact_with_freesound_api():
    """
    Interact with Freesound API for searching and downloading audio clips.
    """
    from project_name.api.freesound_api import FreesoundAPI

    # Get API key and search query from user input
    api_key = click.prompt("Enter your Freesound API key")
    if not api_key:
        click.echo("API key is required.")
        return

    # Basic validation of API key format
    if len(api_key) < 10 or not api_key.isalnum():
        click.echo(
            "Invalid API key format. "
            "Key should be alphanumeric and at least 10 characters."
        )
        return

    query = click.prompt("Enter search query (e.g., 'ambient rain')")
    if not query:
        click.echo("Search query is required.")
        return

    # Initialize Freesound API client
    api_client = FreesoundAPI(api_key)

    # Perform search
    click.echo(f"Searching for '{query}'...")
    results = api_client.search(query=query, page_size=5)

    if not results.get("results"):
        click.echo("No results found.")
        return

    # Display results
    click.echo("\nSearch results:")
    for idx, result in enumerate(results["results"], start=1):
        click.echo(
            f"{idx}. {result['name']} "
            f"(ID: {result['id']}, Duration: {result['duration']}s)"
        )

    # Ask user to select a sound to download
    choice = click.prompt(
        "\nEnter the number of the sound to download (0 to cancel)",
        type=int,
        default=0,
    )

    if choice == 0:
        click.echo("Download canceled.")
        return

    try:
        selected_sound = results["results"][choice - 1]
    except IndexError:
        click.echo("Invalid choice.")
        return

    # Download the selected sound
    sound_id = selected_sound["id"]
    click.echo(f"Downloading sound ID {sound_id}...")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "processed_clips")
    os.makedirs(output_dir, exist_ok=True)

    file_path = api_client.download(sound_id)
    if file_path:
        new_path = os.path.join(output_dir, os.path.basename(file_path))
        os.rename(file_path, new_path)
        click.echo(click.style(f"✓ Sound downloaded to: {new_path}", fg="green"))
    else:
        click.echo(click.style("✗ Failed to download sound.", fg="red"))


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
