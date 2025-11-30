import io  # Added missing import
import logging
import os

import librosa
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from pydub import AudioSegment  # Added missing import

logger = logging.getLogger(__name__)


class Visualizer:
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the visualizer.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def visualize_audio_files(self, input_folder: str) -> dict:
        """
        Generate visualizations for all audio files in a folder.

        Args:
            input_folder: Folder containing audio files

        Returns:
            Dictionary mapping filenames to visualization paths
        """
        visualizations = {}

        for filename in os.listdir(input_folder):
            if filename.endswith((".wav", ".mp3")):
                input_path = os.path.join(input_folder, filename)
                try:
                    # Generate different types of visualizations
                    waveform_path = self.create_waveform(input_path)
                    spectrogram_path = self.create_spectrogram(input_path)
                    mel_spec_path = self.create_mel_spectrogram(input_path)

                    visualizations[filename] = {
                        "waveform": waveform_path,
                        "spectrogram": spectrogram_path,
                        "mel_spectrogram": mel_spec_path,
                    }

                    logger.info(f"Created visualizations for {filename}")
                except Exception as e:
                    logger.error(f"Error visualizing {filename}: {str(e)}")

        return visualizations

    def create_waveform(self, audio_path: str) -> str:
        """
        Create waveform visualization.

        Args:
            audio_path: Path to audio file

        Returns:
            Path to saved visualization
        """
        y, sr = librosa.load(audio_path)

        plt.figure(figsize=(12, 4))
        plt.plot(np.linspace(0, len(y) / sr, len(y)), y)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")

        # Save visualization
        output_path = os.path.join(
            self.output_dir,
            f"{os.path.splitext(os.path.basename(audio_path))[0]}_waveform.png",
        )
        plt.savefig(output_path)
        plt.close()

        return output_path

    def create_spectrogram(self, audio_path: str) -> str:
        """
        Create spectrogram visualization.

        Args:
            audio_path: Path to audio file

        Returns:
            Path to saved visualization
        """
        y, sr = librosa.load(audio_path)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

        plt.figure(figsize=(12, 8))
        librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log")
        plt.colorbar(format="%+2.0f dB")
        plt.title("Spectrogram")

        output_path = os.path.join(
            self.output_dir,
            f"{os.path.splitext(os.path.basename(audio_path))[0]}_spectrogram.png",
        )
        plt.savefig(output_path)
        plt.close()

        return output_path

    def create_mel_spectrogram(self, audio_path: str) -> str:
        """
        Create mel-spectrogram visualization.

        Args:
            audio_path: Path to audio file

        Returns:
            Path to saved visualization
        """
        y, sr = librosa.load(audio_path)
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        S_db = librosa.power_to_db(S, ref=np.max)

        plt.figure(figsize=(12, 8))
        librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="mel")
        plt.colorbar(format="%+2.0f dB")
        plt.title("Mel-Spectrogram")

        output_path = os.path.join(
            self.output_dir,
            f"{os.path.splitext(os.path.basename(audio_path))[0]}_mel_spectrogram.png",
        )
        plt.savefig(output_path)
        plt.close()

        return output_path

    def create_preview_image(
        self, audio_path: str, width: int = 800, height: int = 200
    ) -> bytes | None:  # Updated return type hint
        """
        Create a waveform preview image for GUI display.

        Args:
            audio_path: Path to audio file
            width: Image width in pixels
            height: Image height in pixels

        Returns:
            Image bytes in PNG format
        """
        try:
            y, sr = librosa.load(audio_path)

            # Create figure with specific size
            dpi = 100
            fig = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
            canvas = FigureCanvasAgg(fig)
            ax = fig.add_subplot(111)

            # Plot waveform
            ax.plot(np.linspace(0, len(y) / sr, len(y)), y, color="blue", linewidth=0.5)
            ax.set_xlim(0, len(y) / sr)
            ax.set_ylim(-1, 1)

            # Remove axes for cleaner look
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)

            # Adjust layout and convert to PNG
            fig.tight_layout(pad=0)
            canvas.draw()

            # Convert to PNG bytes
            png_buffer = io.BytesIO()
            canvas.print_png(png_buffer)
            plt.close(fig)

            return png_buffer.getvalue()

        except Exception as e:
            logger.error(f"Error creating preview image: {str(e)}")
            return None

    def plot_features(self, features: dict, output_path: str = None) -> str:
        """
        Create visualization of audio features.

        Args:
            features: Dictionary of audio features
            output_path: Optional path to save visualization

        Returns:
            Path to saved visualization
        """
        plt.figure(figsize=(12, 6))

        # Plot features as a bar chart
        plt.bar(range(len(features)), list(features.values()))
        plt.xticks(range(len(features)), list(features.keys()), rotation=45)
        plt.title("Audio Features")
        plt.tight_layout()

        save_path = output_path
        if save_path is None:
            save_path = os.path.join(self.output_dir, "features.png")

        plt.savefig(save_path)
        plt.close()

        return save_path


def visualize_audio(file_path: str, output_folder: str = "visualizations") -> None:
    """
    Create a waveform visualization for an audio file.

    Args:
        file_path: Path to the audio file
        output_folder: Folder to save the visualization
    """
    logger.info(f"Visualizing audio: {file_path}")

    try:
        # Load audio file
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Generate time axis
        time_axis = np.linspace(0, len(samples) / sample_rate, num=len(samples))

        # Plot waveform
        plt.figure(figsize=(10, 4))
        plt.plot(time_axis, samples, color="blue")
        plt.title(f"Waveform of {os.path.basename(file_path)}")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid()

        # Save visualization
        output_path = os.path.join(output_folder, f"{os.path.basename(file_path)}.png")
        plt.savefig(output_path)
        plt.close()

        logger.info(f"Saved visualization to {output_path}")

    except Exception as e:
        logger.error(f"Error visualizing audio: {str(e)}")


def visualize_category(categories: dict, output_folder: str = "visualizations") -> None:
    """
    Create visualizations for all audio files in specified categories.

    Args:
        categories: Dictionary of categories with file paths
        output_folder: Folder to save the visualizations
    """
    logger.info("Creating visualizations for categories")

    try:
        for category, files in categories.items():
            category_folder = os.path.join(output_folder, category)
            os.makedirs(category_folder, exist_ok=True)

            for file_path in files:
                visualize_audio(file_path, output_folder=category_folder)

    except Exception as e:
        logger.error(f"Error creating category visualizations: {str(e)}")
