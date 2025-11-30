"""Analysis Panel for SonicSleep Pro.

This panel provides interfaces for:
- Audio visualization
- Frequency analysis
- A/B testing
- Sleep quality metrics
"""

import logging
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


class AnalysisPanel:
    """Panel for audio analysis and visualization functions."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame

        # Create a notebook with tabs for different analysis methods
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for each analysis method
        self.visualization_frame = ttk.Frame(self.notebook)
        self.spectrum_frame = ttk.Frame(self.notebook)
        self.ab_frame = ttk.Frame(self.notebook)
        self.sleep_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.visualization_frame, text="Waveform")
        self.notebook.add(self.spectrum_frame, text="Spectrum")
        self.notebook.add(self.ab_frame, text="A/B Testing")
        self.notebook.add(self.sleep_frame, text="Sleep Metrics")

        # Setup each tab
        self._setup_visualization_tab()
        self._setup_spectrum_tab()
        self._setup_ab_testing_tab()
        self._setup_sleep_metrics_tab()

    def _setup_visualization_tab(self):
        """Set up the waveform visualization tab."""
        frame = ttk.Frame(self.visualization_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Waveform Visualization", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=10)

        # File selection
        file_frame = ttk.Frame(frame)
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(file_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.vis_file_var = tk.StringVar()
        ttk.Combobox(file_frame, textvariable=self.vis_file_var, width=40).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(file_frame, text="Refresh", command=self._refresh_file_list).pack(
            side=tk.LEFT, padx=5
        )

        # Visualization options
        options_frame = ttk.LabelFrame(frame, text="Display Options", padding="5")
        options_frame.grid(row=2, column=0, sticky=(tk.N, tk.W), padx=5, pady=10)

        # Channel options
        ttk.Label(options_frame, text="Channel:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.channel_var = tk.StringVar(value="Both")
        ttk.Combobox(
            options_frame,
            textvariable=self.channel_var,
            values=["Left", "Right", "Both"],
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Color options
        ttk.Label(options_frame, text="Color:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.color_var = tk.StringVar(value="Blue")
        ttk.Combobox(
            options_frame,
            textvariable=self.color_var,
            values=["Blue", "Green", "Red", "Purple"],
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Time range
        ttk.Label(options_frame, text="Time Range (s):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        range_frame = ttk.Frame(options_frame)
        range_frame.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.start_time_var = tk.StringVar(value="0")
        self.end_time_var = tk.StringVar(value="60")
        ttk.Entry(range_frame, textvariable=self.start_time_var, width=6).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Label(range_frame, text="to").pack(side=tk.LEFT, padx=2)
        ttk.Entry(range_frame, textvariable=self.end_time_var, width=6).pack(
            side=tk.LEFT, padx=2
        )

        # Additional options checkboxes
        options2_frame = ttk.LabelFrame(frame, text="Additional Options", padding="5")
        options2_frame.grid(row=2, column=1, sticky=(tk.N, tk.W), padx=5, pady=10)

        # Grid
        self.show_grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options2_frame, text="Show Grid", variable=self.show_grid_var
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        # Peak markers
        self.show_peaks_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options2_frame, text="Show Peaks", variable=self.show_peaks_var
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        # RMS line
        self.show_rms_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options2_frame, text="Show RMS", variable=self.show_rms_var
        ).grid(row=2, column=0, sticky=tk.W, pady=5)

        # Update and export buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(
            button_frame,
            text="Update Visualization",
            command=self._update_visualization,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Export Image", command=self._export_visualization
        ).pack(side=tk.LEFT, padx=5)

        # Matplotlib figure setup
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)

        # Canvas setup
        canvas_frame = ttk.Frame(frame)
        canvas_frame.grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )
        frame.rowconfigure(4, weight=1)

        self.canvas = FigureCanvasTkAgg(self.figure, canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Set initial plot
        self._draw_placeholder_visualization()

    def _refresh_file_list(self):
        """Refresh the list of available audio files."""
        # In a real implementation, this would scan for audio files
        example_files = [
            "processed_clips/proc_662201__giddster__summer-rain-and-thunder-4.wav",
            "processed_clips/proc_rain_alleywaydrops-on-leavespuddlessidewalk.wav",
            "output_mixes/sleep_mix_1743891573.mp3",
            "output_mixes/sleep_mix_1743891574.mp3",
        ]

        combobox = self.vis_file_var._nametowidget(self.vis_file_var._name)
        combobox["values"] = example_files

        if example_files:
            self.vis_file_var.set(example_files[0])

        logger.info("Refreshed file list")

    def _draw_placeholder_visualization(self):
        """Draw a placeholder waveform visualization."""
        self.axes.clear()
        # Create some dummy data for visualization
        t = np.linspace(0, 10, 1000)
        y = 0.5 * np.sin(2 * np.pi * 1 * t) + 0.2 * np.sin(2 * np.pi * 2.5 * t)

        # Add some random noise
        y = y + 0.1 * np.random.randn(len(t))

        # Plot the data
        self.axes.plot(t, y, color="blue")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Amplitude")
        self.axes.set_title("Waveform Visualization")
        self.axes.grid(True)

        # Update the canvas
        self.canvas.draw()

    def _update_visualization(self):
        """Update the visualization with current options."""
        selected_file = self.vis_file_var.get()

        if not selected_file:
            messagebox.showwarning("Warning", "Please select an audio file first")
            return

        # In a real implementation, this would load the audio file
        # and generate a proper visualization

        try:
            # Get options
            color = self.color_var.get().lower()
            show_grid = self.show_grid_var.get()
            show_peaks = self.show_peaks_var.get()
            show_rms = self.show_rms_var.get()

            # Try to get time range
            try:
                start_time = float(self.start_time_var.get())
                end_time = float(self.end_time_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Invalid time range values")
                start_time = 0
                end_time = 10

            # Clear the plot
            self.axes.clear()

            # Generate dummy data based on the file name
            # In a real implementation, this would use actual audio data
            t = np.linspace(start_time, end_time, 1000)

            # Use a simplified hash of the filename to create different but consistent waveforms
            seed = sum(ord(c) for c in selected_file)
            np.random.seed(seed)

            # Generate a more complex waveform with multiple frequencies
            y = 0.4 * np.sin(2 * np.pi * 1 * t)
            y += 0.3 * np.sin(2 * np.pi * 2.5 * t + 0.2)
            y += 0.15 * np.sin(2 * np.pi * 5 * t + 0.5)
            y += 0.05 * np.sin(2 * np.pi * 10 * t + 1.0)

            # Add some random noise
            y = y + 0.1 * np.random.randn(len(t))

            # Plot the waveform
            self.axes.plot(t, y, color=color)

            # Show peaks if requested
            if show_peaks:
                # Find peaks (very simple approach)
                from scipy.signal import find_peaks

                peaks, _ = find_peaks(y, height=0.5)
                self.axes.plot(t[peaks], y[peaks], "x", color="red")

            # Show RMS line if requested
            if show_rms:
                rms = np.sqrt(np.mean(y**2))
                self.axes.axhline(
                    y=rms, color="green", linestyle="--", label=f"RMS: {rms:.2f}"
                )
                self.axes.axhline(y=-rms, color="green", linestyle="--")
                self.axes.legend()

            # Set up the plot
            self.axes.set_xlabel("Time (s)")
            self.axes.set_ylabel("Amplitude")
            self.axes.set_title(f"Waveform: {selected_file.split('/')[-1]}")
            self.axes.grid(show_grid)

            # Update the canvas
            self.canvas.draw()

            logger.info(f"Updated visualization for {selected_file}")

        except Exception as e:
            logger.error(f"Error updating visualization: {str(e)}")
            messagebox.showerror("Error", f"Error updating visualization: {str(e)}")

    def _export_visualization(self):
        """Export the current visualization as an image."""
        selected_file = self.vis_file_var.get()

        if not selected_file:
            messagebox.showwarning("Warning", "Please generate a visualization first")
            return

        # Get export path
        from tkinter import filedialog

        filename = selected_file.split("/")[-1].split(".")[0] + "_waveform.png"
        export_path = filedialog.asksaveasfilename(
            title="Export Visualization",
            initialfile=filename,
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*"),
            ],
        )

        if export_path:
            try:
                self.figure.savefig(export_path, dpi=300, bbox_inches="tight")
                logger.info(f"Exported visualization to {export_path}")
                messagebox.showinfo(
                    "Export Successful", f"Visualization exported to {export_path}"
                )
            except Exception as e:
                logger.error(f"Error exporting visualization: {str(e)}")
                messagebox.showerror(
                    "Error", f"Error exporting visualization: {str(e)}"
                )

    def _setup_spectrum_tab(self):
        """Set up the frequency spectrum analysis tab."""
        frame = ttk.Frame(self.spectrum_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Frequency Spectrum Analysis", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=10)

        # File selection
        file_frame = ttk.Frame(frame)
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(file_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.spec_file_var = tk.StringVar()
        ttk.Combobox(file_frame, textvariable=self.spec_file_var, width=40).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            file_frame, text="Refresh", command=self._refresh_spectrum_file_list
        ).pack(side=tk.LEFT, padx=5)

        # Analysis options
        options_frame = ttk.LabelFrame(frame, text="Analysis Options", padding="5")
        options_frame.grid(row=2, column=0, sticky=(tk.N, tk.W), padx=5, pady=10)

        # FFT size
        ttk.Label(options_frame, text="FFT Size:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.fft_size_var = tk.StringVar(value="2048")
        ttk.Combobox(
            options_frame,
            textvariable=self.fft_size_var,
            values=["512", "1024", "2048", "4096", "8192"],
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Window function
        ttk.Label(options_frame, text="Window:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.window_var = tk.StringVar(value="Hann")
        ttk.Combobox(
            options_frame,
            textvariable=self.window_var,
            values=["Rectangular", "Hann", "Hamming", "Blackman"],
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Time segment
        ttk.Label(options_frame, text="Time Segment (s):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        segment_frame = ttk.Frame(options_frame)
        segment_frame.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.segment_start_var = tk.StringVar(value="0")
        self.segment_len_var = tk.StringVar(value="5")
        ttk.Entry(segment_frame, textvariable=self.segment_start_var, width=6).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Label(segment_frame, text="for").pack(side=tk.LEFT, padx=2)
        ttk.Entry(segment_frame, textvariable=self.segment_len_var, width=6).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Label(segment_frame, text="seconds").pack(side=tk.LEFT, padx=2)

        # Display options
        display_frame = ttk.LabelFrame(frame, text="Display Options", padding="5")
        display_frame.grid(row=2, column=1, sticky=(tk.N, tk.W), padx=5, pady=10)

        # Scale
        ttk.Label(display_frame, text="Scale:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.scale_var = tk.StringVar(value="Linear")
        ttk.Combobox(
            display_frame, textvariable=self.scale_var, values=["Linear", "Log", "dB"]
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Frequency range
        ttk.Label(display_frame, text="Freq Range (Hz):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        freq_frame = ttk.Frame(display_frame)
        freq_frame.grid(row=1, column=1, sticky=tk.W, pady=5)

        self.min_freq_var = tk.StringVar(value="20")
        self.max_freq_var = tk.StringVar(value="20000")
        ttk.Entry(freq_frame, textvariable=self.min_freq_var, width=6).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Label(freq_frame, text="to").pack(side=tk.LEFT, padx=2)
        ttk.Entry(freq_frame, textvariable=self.max_freq_var, width=6).pack(
            side=tk.LEFT, padx=2
        )

        # Show peaks
        self.spec_peaks_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            display_frame, text="Show Frequency Peaks", variable=self.spec_peaks_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Update and export buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Analyze", command=self._update_spectrum).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="Export Data", command=self._export_spectrum_data
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Export Image", command=self._export_spectrum_image
        ).pack(side=tk.LEFT, padx=5)

        # Matplotlib figure setup
        self.spec_figure = Figure(figsize=(8, 4), dpi=100)
        self.spec_axes = self.spec_figure.add_subplot(111)

        # Canvas setup
        canvas_frame = ttk.Frame(frame)
        canvas_frame.grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )
        frame.rowconfigure(4, weight=1)

        self.spec_canvas = FigureCanvasTkAgg(self.spec_figure, canvas_frame)
        self.spec_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Set initial plot
        self._draw_placeholder_spectrum()

    def _refresh_spectrum_file_list(self):
        """Refresh the list of available audio files."""
        # Reuse file list from visualization tab
        self._refresh_file_list()
        combobox = self.spec_file_var._nametowidget(self.spec_file_var._name)
        combobox["values"] = self.vis_file_var._nametowidget(self.vis_file_var._name)[
            "values"
        ]

        if combobox["values"]:
            self.spec_file_var.set(combobox["values"][0])

    def _draw_placeholder_spectrum(self):
        """Draw a placeholder frequency spectrum."""
        self.spec_axes.clear()

        # Create some dummy data
        freqs = np.linspace(20, 20000, 1000)
        # Generate a spectrum with a couple of peaks
        spectrum = (
            1 / freqs
            + 5 * np.exp(-((freqs - 100) ** 2) / 100)
            + 3 * np.exp(-((freqs - 1000) ** 2) / 10000)
        )
        spectrum = spectrum / np.max(spectrum)  # Normalize

        # Plot using log scale
        self.spec_axes.semilogx(freqs, spectrum)
        self.spec_axes.set_xlabel("Frequency (Hz)")
        self.spec_axes.set_ylabel("Magnitude")
        self.spec_axes.set_title("Frequency Spectrum")
        self.spec_axes.grid(True)
        self.spec_axes.set_xlim(20, 20000)

        # Update the canvas
        self.spec_canvas.draw()

    def _update_spectrum(self):
        """Update the spectrum analysis with current options."""
        selected_file = self.spec_file_var.get()

        if not selected_file:
            messagebox.showwarning("Warning", "Please select an audio file first")
            return

        # In a real implementation, this would load the audio file
        # and generate a proper spectrum analysis

        try:
            # Get options
            fft_size = int(self.fft_size_var.get())
            window_type = self.window_var.get().lower()
            scale = self.scale_var.get().lower()
            show_peaks = self.spec_peaks_var.get()

            # Try to get time segment
            try:
                segment_start = float(self.segment_start_var.get())
                segment_len = float(self.segment_len_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Invalid time segment values")
                segment_start = 0
                segment_len = 5

            # Try to get frequency range
            try:
                min_freq = float(self.min_freq_var.get())
                max_freq = float(self.max_freq_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Invalid frequency range values")
                min_freq = 20
                max_freq = 20000

            # Clear the plot
            self.spec_axes.clear()

            # Generate dummy spectrum data based on the file name
            # In a real implementation, this would use actual audio data
            freqs = np.linspace(min_freq, max_freq, 1000)

            # Use a simplified hash of the filename for reproducibility
            seed = sum(ord(c) for c in selected_file)
            np.random.seed(seed)

            # Generate spectral peaks at different frequencies
            spectrum = np.zeros_like(freqs)

            # Add some characteristic peaks
            # Base frequency and harmonics (e.g., for tonal sounds)
            base_freq = 80 + (seed % 400)  # Base frequency between 80-480 Hz
            for i in range(1, 6):
                center = i * base_freq
                if center < max_freq:
                    spectrum += (10 / i) * np.exp(
                        -((freqs - center) ** 2) / (10 * i) ** 2
                    )

            # Add some noise peaks (e.g., for noise/rain sounds)
            for _ in range(8):
                center = min_freq + np.random.rand() * (max_freq - min_freq)
                width = 50 + np.random.rand() * 200
                height = 0.1 + np.random.rand() * 0.9
                spectrum += height * np.exp(-((freqs - center) ** 2) / width**2)

            # Add 1/f noise (common in natural sounds)
            pink_noise = 1 / np.sqrt(freqs)
            pink_noise = pink_noise / np.max(pink_noise) * 0.5
            spectrum += pink_noise

            # Normalize
            spectrum = spectrum / np.max(spectrum)

            # Apply different scales
            if scale == "db":
                # Convert to dB scale (avoid log of zero)
                spectrum = 20 * np.log10(spectrum + 1e-6)
                spectrum = np.clip(spectrum, -60, 0)  # Clip to reasonable dB range
                y_label = "Magnitude (dB)"
            else:
                y_label = "Magnitude"

            # Plot with appropriate scale
            if scale == "log" or scale == "db":
                self.spec_axes.semilogx(freqs, spectrum)
            else:  # linear
                self.spec_axes.plot(freqs, spectrum)

            # Show peaks if requested
            if show_peaks:
                from scipy.signal import find_peaks

                peaks, _ = find_peaks(spectrum, height=0.5, distance=50)
                peak_freqs = freqs[peaks]
                peak_mags = spectrum[peaks]
                self.spec_axes.plot(peak_freqs, peak_mags, "x", color="red")

                # Annotate the top 3 peaks
                sorted_peaks = sorted(
                    zip(peak_mags, peak_freqs, strict=False), reverse=True
                )[:3]
                for i, (mag, freq) in enumerate(sorted_peaks):
                    self.spec_axes.annotate(
                        f"{freq:.0f} Hz",
                        xy=(freq, mag),
                        xytext=(0, 10),
                        textcoords="offset points",
                        ha="center",
                    )

            # Set up the plot
            self.spec_axes.set_xlabel("Frequency (Hz)")
            self.spec_axes.set_ylabel(y_label)
            self.spec_axes.set_title(f"Spectrum: {selected_file.split('/')[-1]}")
            self.spec_axes.grid(True)
            self.spec_axes.set_xlim(min_freq, max_freq)

            # Update the canvas
            self.spec_canvas.draw()

            logger.info(f"Updated spectrum for {selected_file}")

        except Exception as e:
            logger.error(f"Error updating spectrum: {str(e)}")
            messagebox.showerror("Error", f"Error updating spectrum: {str(e)}")

    def _export_spectrum_data(self):
        """Export the spectrum data as CSV."""
        selected_file = self.spec_file_var.get()

        if not selected_file:
            messagebox.showwarning("Warning", "Please analyze a file first")
            return

        # Get export path
        from tkinter import filedialog

        filename = selected_file.split("/")[-1].split(".")[0] + "_spectrum.csv"
        export_path = filedialog.asksaveasfilename(
            title="Export Spectrum Data",
            initialfile=filename,
            defaultextension=".csv",
            filetypes=[
                ("CSV File", "*.csv"),
                ("Text File", "*.txt"),
                ("All Files", "*.*"),
            ],
        )

        if export_path:
            try:
                # In a real implementation, this would export actual data
                # For now, just create a simple CSV with the dummy data
                import csv

                # Generate dummy data similar to what's shown
                freqs = np.linspace(
                    float(self.min_freq_var.get()), float(self.max_freq_var.get()), 1000
                )

                # Use same seed as visualization for consistency
                seed = sum(ord(c) for c in selected_file)
                np.random.seed(seed)

                # Similar spectrum generation as in _update_spectrum
                spectrum = np.zeros_like(freqs)
                base_freq = 80 + (seed % 400)
                for i in range(1, 6):
                    center = i * base_freq
                    spectrum += (10 / i) * np.exp(
                        -((freqs - center) ** 2) / (10 * i) ** 2
                    )

                for _ in range(8):
                    center = np.random.rand() * 20000
                    width = 50 + np.random.rand() * 200
                    height = 0.1 + np.random.rand() * 0.9
                    spectrum += height * np.exp(-((freqs - center) ** 2) / width**2)

                spectrum += 1 / np.sqrt(freqs + 1) * 0.5
                spectrum = spectrum / np.max(spectrum)

                # Apply scale if needed
                if self.scale_var.get().lower() == "db":
                    spectrum = 20 * np.log10(spectrum + 1e-6)

                # Write to CSV
                with open(export_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Frequency (Hz)", "Magnitude"])
                    for i in range(len(freqs)):
                        writer.writerow([freqs[i], spectrum[i]])

                logger.info(f"Exported spectrum data to {export_path}")
                messagebox.showinfo(
                    "Export Successful", f"Spectrum data exported to {export_path}"
                )

            except Exception as e:
                logger.error(f"Error exporting spectrum data: {str(e)}")
                messagebox.showerror(
                    "Error", f"Error exporting spectrum data: {str(e)}"
                )

    def _export_spectrum_image(self):
        """Export the current spectrum visualization as an image."""
        selected_file = self.spec_file_var.get()

        if not selected_file:
            messagebox.showwarning("Warning", "Please generate a spectrum first")
            return

        # Get export path
        from tkinter import filedialog

        filename = selected_file.split("/")[-1].split(".")[0] + "_spectrum.png"
        export_path = filedialog.asksaveasfilename(
            title="Export Spectrum Image",
            initialfile=filename,
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*"),
            ],
        )

        if export_path:
            try:
                self.spec_figure.savefig(export_path, dpi=300, bbox_inches="tight")
                logger.info(f"Exported spectrum image to {export_path}")
                messagebox.showinfo(
                    "Export Successful", f"Spectrum image exported to {export_path}"
                )
            except Exception as e:
                logger.error(f"Error exporting spectrum image: {str(e)}")
                messagebox.showerror(
                    "Error", f"Error exporting spectrum image: {str(e)}"
                )

    def _setup_ab_testing_tab(self):
        """Set up the A/B testing tab."""
        frame = ttk.Frame(self.ab_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="A/B Testing Module", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=10
        )

        # File selection
        ab_files_frame = ttk.Frame(frame)
        ab_files_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(ab_files_frame, text="File A:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.file_a_var = tk.StringVar()
        ttk.Combobox(ab_files_frame, textvariable=self.file_a_var, width=40).grid(
            row=0, column=1, sticky=tk.W, pady=5
        )

        ttk.Label(ab_files_frame, text="File B:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.file_b_var = tk.StringVar()
        ttk.Combobox(ab_files_frame, textvariable=self.file_b_var, width=40).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )

        ttk.Button(
            ab_files_frame, text="Refresh Files", command=self._refresh_ab_files
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Test settings
        settings_frame = ttk.LabelFrame(frame, text="Test Settings", padding="5")
        settings_frame.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E), padx=5, pady=10)

        ttk.Label(settings_frame, text="Test Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.test_name_var = tk.StringVar(value="Sleep Quality Test")
        ttk.Entry(settings_frame, textvariable=self.test_name_var, width=30).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5
        )

        ttk.Label(settings_frame, text="Test Duration:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.test_duration_var = tk.StringVar(value="5")
        ttk.Entry(settings_frame, textvariable=self.test_duration_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )
        ttk.Label(settings_frame, text="minutes per sample").grid(
            row=1, column=2, sticky=tk.W, pady=5
        )

        ttk.Label(settings_frame, text="Test Type:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.test_type_var = tk.StringVar(value="Blind Test")
        ttk.Combobox(
            settings_frame,
            textvariable=self.test_type_var,
            values=["Blind Test", "Self-Assessment", "Sleep Monitor"],
        ).grid(row=2, column=1, sticky=tk.W, pady=5)

        # Result display
        results_frame = ttk.LabelFrame(frame, text="Test Results", padding="5")
        results_frame.grid(row=2, column=1, sticky=(tk.N, tk.W, tk.E), padx=5, pady=10)

        # Run and report buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Start Test", command=self._start_ab_test).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Stop Test", command=self._stop_ab_test).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="View Results", command=self._view_ab_results
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Export Report", command=self._export_ab_report
        ).pack(side=tk.LEFT, padx=5)

        # Results visualization
        result_display_frame = ttk.Frame(frame)
        result_display_frame.grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )
        frame.rowconfigure(4, weight=1)

        # Sample results table
        self.result_table = ttk.Treeview(
            result_display_frame,
            columns=("metric", "file_a", "file_b", "difference"),
            show="headings",
            height=8,
        )

        # Configure columns
        self.result_table.heading("metric", text="Metric")
        self.result_table.heading("file_a", text="File A")
        self.result_table.heading("file_b", text="File B")
        self.result_table.heading("difference", text="Difference")

        self.result_table.column("metric", width=150)
        self.result_table.column("file_a", width=100)
        self.result_table.column("file_b", width=100)
        self.result_table.column("difference", width=100)

        # Add scrollbar
        yscrollbar = ttk.Scrollbar(
            result_display_frame, orient="vertical", command=self.result_table.yview
        )
        self.result_table.configure(yscrollcommand=yscrollbar.set)

        # Pack components
        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add some sample data
        self._populate_sample_results()

    def _refresh_ab_files(self):
        """Refresh the list of available audio files for A/B testing."""
        # Reuse file list from visualization tab
        self._refresh_file_list()

        combobox_a = self.file_a_var._nametowidget(self.file_a_var._name)
        combobox_b = self.file_b_var._nametowidget(self.file_b_var._name)

        values = self.vis_file_var._nametowidget(self.vis_file_var._name)["values"]
        combobox_a["values"] = values
        combobox_b["values"] = values

        if values:
            self.file_a_var.set(values[0])
            if len(values) > 1:
                self.file_b_var.set(values[1])
            else:
                self.file_b_var.set(values[0])

    def _populate_sample_results(self):
        """Populate the results table with sample data."""
        # Clear existing items
        for item in self.result_table.get_children():
            self.result_table.delete(item)

        # Add sample data
        sample_data = [
            ("Sleep Onset Time", "18.2 min", "15.7 min", "-2.5 min"),
            ("Sleep Quality Score", "7.4", "8.1", "+0.7"),
            ("Awakenings", "3.2", "2.4", "-0.8"),
            ("Deep Sleep %", "22%", "24%", "+2%"),
            ("REM Sleep %", "19%", "20%", "+1%"),
            ("Morning Alertness", "6.8", "7.3", "+0.5"),
            ("Heart Rate", "63 bpm", "61 bpm", "-2 bpm"),
        ]

        for data in sample_data:
            self.result_table.insert("", tk.END, values=data)

    def _start_ab_test(self):
        """Start the A/B test."""
        file_a = self.file_a_var.get()
        file_b = self.file_b_var.get()

        if not file_a or not file_b:
            messagebox.showwarning("Warning", "Please select both files for testing")
            return

        try:
            # Validate test duration
            duration = float(self.test_duration_var.get())
            if duration <= 0:
                messagebox.showwarning("Warning", "Test duration must be positive")
                return

            # In a real implementation, this would start an actual test
            test_name = self.test_name_var.get()
            test_type = self.test_type_var.get()

            logger.info(f"Starting {test_type} comparing {file_a} and {file_b}")
            messagebox.showinfo(
                "Test Started",
                f"Started {test_type} with {duration} minute samples.\n\nPlease follow the test protocol for '{test_name}'.",
            )

        except ValueError:
            messagebox.showwarning("Warning", "Invalid test duration")
        except Exception as e:
            logger.error(f"Error starting test: {str(e)}")
            messagebox.showerror("Error", f"Error starting test: {str(e)}")

    def _stop_ab_test(self):
        """Stop the currently running A/B test."""
        # In a real implementation, this would stop an actual test
        logger.info("Stopping A/B test")
        messagebox.showinfo(
            "Test Stopped",
            "A/B test has been stopped.\nResults up to this point will be saved.",
        )

    def _view_ab_results(self):
        """Display the results of the A/B test."""
        # In a real implementation, this would load and display actual results
        # For now, just update with new random data
        import random

        # Clear existing items
        for item in self.result_table.get_children():
            self.result_table.delete(item)

        # Generate slightly different random results
        metrics = [
            "Sleep Onset Time",
            "Sleep Quality Score",
            "Awakenings",
            "Deep Sleep %",
            "REM Sleep %",
            "Morning Alertness",
            "Heart Rate",
        ]

        for metric in metrics:
            if metric == "Sleep Onset Time":
                a_val = round(random.uniform(15, 25), 1)
                b_val = round(random.uniform(13, 23), 1)
                a_str = f"{a_val} min"
                b_str = f"{b_val} min"
                diff = round(b_val - a_val, 1)
                diff_str = f"{diff:+.1f} min"
            elif metric == "Sleep Quality Score":
                a_val = round(random.uniform(6, 9), 1)
                b_val = round(random.uniform(6, 9), 1)
                a_str = f"{a_val}"
                b_str = f"{b_val}"
                diff = round(b_val - a_val, 1)
                diff_str = f"{diff:+.1f}"
            elif metric == "Awakenings":
                a_val = round(random.uniform(2, 5), 1)
                b_val = round(random.uniform(1.5, 4.5), 1)
                a_str = f"{a_val}"
                b_str = f"{b_val}"
                diff = round(b_val - a_val, 1)
                diff_str = f"{diff:+.1f}"
            elif "%" in metric:
                a_val = round(random.uniform(15, 30))
                b_val = round(random.uniform(16, 32))
                a_str = f"{a_val}%"
                b_str = f"{b_val}%"
                diff = b_val - a_val
                diff_str = f"{diff:+d}%"
            elif metric == "Morning Alertness":
                a_val = round(random.uniform(6, 8), 1)
                b_val = round(random.uniform(6, 8), 1)
                a_str = f"{a_val}"
                b_str = f"{b_val}"
                diff = round(b_val - a_val, 1)
                diff_str = f"{diff:+.1f}"
            elif metric == "Heart Rate":
                a_val = round(random.uniform(60, 70))
                b_val = round(random.uniform(58, 68))
                a_str = f"{a_val} bpm"
                b_str = f"{b_val} bpm"
                diff = b_val - a_val
                diff_str = f"{diff:+d} bpm"

            self.result_table.insert(
                "", tk.END, values=(metric, a_str, b_str, diff_str)
            )

        logger.info("Updated A/B test results")

    def _export_ab_report(self):
        """Export the A/B test results as a report."""
        # Get export path
        from tkinter import filedialog

        test_name = self.test_name_var.get().replace(" ", "_").lower()
        filename = f"ab_test_{test_name}.pdf"
        export_path = filedialog.asksaveasfilename(
            title="Export A/B Test Report",
            initialfile=filename,
            defaultextension=".pdf",
            filetypes=[
                ("PDF File", "*.pdf"),
                ("HTML Report", "*.html"),
                ("CSV Data", "*.csv"),
                ("All Files", "*.*"),
            ],
        )

        if export_path:
            try:
                # In a real implementation, this would generate an actual report
                logger.info(f"Exporting A/B test report to {export_path}")
                messagebox.showinfo(
                    "Export Successful", f"A/B test report exported to {export_path}"
                )
            except Exception as e:
                logger.error(f"Error exporting report: {str(e)}")
                messagebox.showerror("Error", f"Error exporting report: {str(e)}")

    def _setup_sleep_metrics_tab(self):
        """Set up the sleep metrics tab."""
        frame = ttk.Frame(self.sleep_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Sleep Quality Metrics", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=10
        )

        # Sound selection
        sound_frame = ttk.Frame(frame)
        sound_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(sound_frame, text="Sound Mix:").pack(side=tk.LEFT, padx=5)
        self.sleep_mix_var = tk.StringVar()
        ttk.Combobox(sound_frame, textvariable=self.sleep_mix_var, width=40).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(sound_frame, text="Refresh", command=self._refresh_sleep_mixes).pack(
            side=tk.LEFT, padx=5
        )

        # Sleep metrics display
        metrics_frame = ttk.LabelFrame(
            frame, text="Predicted Sleep Metrics", padding="5"
        )
        metrics_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )
        frame.rowconfigure(2, weight=1)

        # Create a canvas with a scrollbar
        canvas = tk.Canvas(metrics_frame)
        scrollbar = ttk.Scrollbar(
            metrics_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add metrics content to scrollable frame
        metrics = [
            ("Sleep Onset", "17.3", "minutes", "Time to fall asleep"),
            (
                "Sleep Efficiency",
                "94.2",
                "%",
                "Percentage of time in bed spent sleeping",
            ),
            (
                "Deep Sleep",
                "22.5",
                "%",
                "Percentage of total sleep time in deep sleep phase",
            ),
            (
                "REM Sleep",
                "19.8",
                "%",
                "Percentage of total sleep time in REM sleep phase",
            ),
            (
                "Light Sleep",
                "57.7",
                "%",
                "Percentage of total sleep time in light sleep phase",
            ),
            (
                "Awakenings",
                "2.3",
                "events",
                "Number of times waking up during the night",
            ),
            ("Sleep Quality Score", "8.3", "out of 10", "Overall sleep quality score"),
            (
                "Relaxation Index",
                "76",
                "out of 100",
                "How well the sound induces relaxation",
            ),
            ("Heart Rate", "61.5", "bpm", "Average heart rate during sleep"),
            ("Movement", "12.4", "events/hour", "Movement during sleep"),
            (
                "Morning Alertness",
                "7.8",
                "out of 10",
                "Predicted alertness upon waking",
            ),
        ]

        # Display metrics in a grid
        for i, (name, value, unit, desc) in enumerate(metrics):
            ttk.Label(scrollable_frame, text=name, font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=5
            )
            ttk.Label(scrollable_frame, text=value, font=("Arial", 10)).grid(
                row=i, column=1, sticky=tk.E, padx=5, pady=5
            )
            ttk.Label(scrollable_frame, text=unit).grid(
                row=i, column=2, sticky=tk.W, padx=5, pady=5
            )
            ttk.Label(scrollable_frame, text=desc, foreground="gray").grid(
                row=i, column=3, sticky=tk.W, padx=20, pady=5
            )

        # Actions and visualizations
        actions_frame = ttk.Frame(frame)
        actions_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(
            actions_frame,
            text="Calculate Metrics",
            command=self._calculate_sleep_metrics,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            actions_frame, text="Compare to Average", command=self._compare_to_average
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            actions_frame, text="Generate Report", command=self._generate_sleep_report
        ).pack(side=tk.LEFT, padx=5)

        # Initialize with default values
        self._refresh_sleep_mixes()

    def _refresh_sleep_mixes(self):
        """Refresh the list of available sleep mixes."""
        # Example files
        sleep_mixes = [
            "output_mixes/sleep_mix_1743891573.mp3",
            "output_mixes/sleep_mix_1743891574.mp3",
        ]

        combobox = self.sleep_mix_var._nametowidget(self.sleep_mix_var._name)
        combobox["values"] = sleep_mixes

        if sleep_mixes:
            self.sleep_mix_var.set(sleep_mixes[0])

        logger.info("Refreshed sleep mix list")

    def _calculate_sleep_metrics(self):
        """Calculate sleep metrics for the selected mix."""
        selected_mix = self.sleep_mix_var.get()

        if not selected_mix:
            messagebox.showwarning("Warning", "Please select a sleep mix first")
            return

        # In a real implementation, this would analyze the mix and predict metrics
        logger.info(f"Calculating sleep metrics for {selected_mix}")
        messagebox.showinfo(
            "Calculation Complete", "Sleep metrics have been calculated and updated."
        )

        # Here we would update the metrics display

    def _compare_to_average(self):
        """Compare current metrics to average."""
        selected_mix = self.sleep_mix_var.get()

        if not selected_mix:
            messagebox.showwarning("Warning", "Please select a sleep mix first")
            return

        # In a real implementation, this would show a comparison chart
        logger.info("Comparing to average metrics")

        # Create a simple comparison window
        compare_window = tk.Toplevel()
        compare_window.title("Metrics Comparison")
        compare_window.geometry("600x400")

        # Create a comparison chart
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Sample data
        metrics = [
            "Sleep Onset",
            "Sleep Quality",
            "Deep Sleep",
            "REM Sleep",
            "Awakenings",
        ]
        current = [17.3, 8.3, 22.5, 19.8, 2.3]
        average = [21.6, 7.2, 19.2, 18.5, 3.1]

        # Normalize data for display
        normalized_current = []
        normalized_avg = []

        for i, (curr, avg) in enumerate(zip(current, average, strict=False)):
            if i == 0 or i == 4:  # Lower is better for Sleep Onset and Awakenings
                # Invert for display so higher is always better
                max_val = max(curr, avg) * 1.2
                normalized_current.append((max_val - curr) / max_val * 100)
                normalized_avg.append((max_val - avg) / max_val * 100)
            else:  # Higher is better
                normalized_current.append(curr / 10 * 100)  # Assuming 10 is max
                normalized_avg.append(avg / 10 * 100)

        # Plot comparison
        x = range(len(metrics))
        width = 0.35

        ax.bar(
            [i - width / 2 for i in x],
            normalized_current,
            width,
            label=f"{selected_mix.split('/')[-1]}",
        )
        ax.bar([i + width / 2 for i in x], normalized_avg, width, label="Average")

        ax.set_title("Sleep Metrics Comparison")
        ax.set_ylim(0, 100)
        ax.set_ylabel("Score (normalized)")
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()

        # Add the chart to the window
        canvas = FigureCanvasTkAgg(fig, compare_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _generate_sleep_report(self):
        """Generate a sleep quality report."""
        selected_mix = self.sleep_mix_var.get()

        if not selected_mix:
            messagebox.showwarning("Warning", "Please select a sleep mix first")
            return

        # Get export path
        from tkinter import filedialog

        filename = f"sleep_report_{selected_mix.split('/')[-1].split('.')[0]}.pdf"
        export_path = filedialog.asksaveasfilename(
            title="Export Sleep Report",
            initialfile=filename,
            defaultextension=".pdf",
            filetypes=[
                ("PDF File", "*.pdf"),
                ("HTML Report", "*.html"),
                ("All Files", "*.*"),
            ],
        )

        if export_path:
            try:
                # In a real implementation, this would generate an actual report
                logger.info(f"Generating sleep report to {export_path}")
                messagebox.showinfo(
                    "Export Successful",
                    f"Sleep metrics report exported to {export_path}",
                )
            except Exception as e:
                logger.error(f"Error exporting report: {str(e)}")
                messagebox.showerror("Error", f"Error exporting report: {str(e)}")
