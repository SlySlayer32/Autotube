"""Settings Panel for SonicSleep Pro.

This panel provides interfaces for:
- Parameter configuration
- AI recommendations
- Preset application
"""

import logging
import tkinter as tk
from tkinter import messagebox, ttk

logger = logging.getLogger(__name__)


class SettingsPanel:
    """Panel for settings management functions."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame

        # Create a notebook with tabs for each step
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for each step in the settings function
        self.config_frame = ttk.Frame(self.notebook)
        self.ai_frame = ttk.Frame(self.notebook)
        self.preset_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.config_frame, text="Parameter Configuration")
        self.notebook.add(self.ai_frame, text="AI Recommendations")
        self.notebook.add(self.preset_frame, text="Preset Application")

        # Setup each tab
        self._setup_config_tab()
        self._setup_ai_tab()
        self._setup_preset_tab()

    def _setup_config_tab(self):
        """Set up the parameter configuration tab."""
        frame = ttk.Frame(self.config_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Parameter Configuration", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=10)

        # Parameter categories
        notebook = ttk.Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Audio processing parameters
        audio_frame = ttk.Frame(notebook, padding="10")
        notebook.add(audio_frame, text="Audio")

        ttk.Label(audio_frame, text="Sample Rate:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.sample_rate_var = tk.StringVar(value="44100")
        ttk.Combobox(
            audio_frame,
            textvariable=self.sample_rate_var,
            values=["22050", "44100", "48000", "96000"],
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(audio_frame, text="Bit Depth:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.bit_depth_var = tk.StringVar(value="16")
        ttk.Combobox(
            audio_frame, textvariable=self.bit_depth_var, values=["16", "24", "32"]
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Mix parameters
        mix_frame = ttk.Frame(notebook, padding="10")
        notebook.add(mix_frame, text="Mix")

        ttk.Label(mix_frame, text="Duration (min):").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.duration_var = tk.StringVar(value="60")
        ttk.Entry(mix_frame, textvariable=self.duration_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5
        )

        ttk.Label(mix_frame, text="Transition Length (sec):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.transition_var = tk.StringVar(value="5")
        ttk.Entry(mix_frame, textvariable=self.transition_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )

        # Save and reset buttons
        ttk.Button(frame, text="Save Parameters", command=self._save_parameters).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        ttk.Button(
            frame, text="Reset to Defaults", command=self._reset_parameters
        ).grid(row=2, column=1, sticky=tk.W, pady=10)

    def _save_parameters(self):
        """Save parameters to a config file."""
        try:
            config = {
                "audio": {
                    "sample_rate": self.sample_rate_var.get(),
                    "bit_depth": self.bit_depth_var.get(),
                },
                "mix": {
                    "duration": self.duration_var.get(),
                    "transition": self.transition_var.get(),
                },
            }

            # We would normally save this to a config file
            # For now, just log it
            logger.info(f"Parameters saved: {config}")
            messagebox.showinfo("Success", "Parameters saved successfully")

        except Exception as e:
            logger.error(f"Error saving parameters: {str(e)}")
            messagebox.showerror("Error", f"Failed to save parameters: {str(e)}")

    def _reset_parameters(self):
        """Reset parameters to defaults."""
        self.sample_rate_var.set("44100")
        self.bit_depth_var.set("16")
        self.duration_var.set("60")
        self.transition_var.set("5")
        logger.info("Parameters reset to defaults")
        messagebox.showinfo("Reset", "Parameters reset to default values")

    def _setup_ai_tab(self):
        """Set up the AI recommendations tab."""
        frame = ttk.Frame(self.ai_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="AI Recommendations", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=10
        )

        # Mix type
        ttk.Label(frame, text="Mix Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mix_type_var = tk.StringVar(value="sleep")
        ttk.Combobox(
            frame, textvariable=self.mix_type_var, values=["sleep", "focus", "relax"]
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Get recommendations button
        ttk.Button(
            frame, text="Get Recommendations", command=self._get_recommendations
        ).grid(row=2, column=1, sticky=tk.W, pady=10)

        # Recommendations list
        ttk.Label(frame, text="Recommendations:").grid(
            row=3, column=0, sticky=tk.NW, pady=5
        )
        self.recommendations_list = tk.Listbox(frame, height=10, width=50)
        self.recommendations_list.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        # Apply button
        ttk.Button(
            frame, text="Apply Selected", command=self._apply_recommendation
        ).grid(row=4, column=1, sticky=tk.W, pady=5)

    def _get_recommendations(self):
        """Get AI recommendations."""
        mix_type = self.mix_type_var.get()

        # In a real implementation, this would connect to an AI model
        # For now, just simulate some recommendations
        recommendations = {
            "sleep": [
                "Rain with low-frequency binaural beats (2-4 Hz)",
                "Ocean waves with gentle white noise",
                "Soft forest sounds with delta brainwaves",
                "Night crickets with gentle rain",
            ],
            "focus": [
                "Brown noise with alpha waves (8-12 Hz)",
                "Light rainfall without thunder",
                "Ambient cafe noises",
                "Mountain stream with light birds",
            ],
            "relax": [
                "Beach waves with theta waves (4-8 Hz)",
                "Gentle rain on leaves",
                "Soft wind chimes with distant thunder",
                "Forest ambience with occasional birds",
            ],
        }

        self.recommendations_list.delete(0, tk.END)
        for rec in recommendations.get(mix_type, []):
            self.recommendations_list.insert(tk.END, rec)

        logger.info(f"Generated recommendations for {mix_type} mix type")

    def _apply_recommendation(self):
        """Apply the selected recommendation."""
        selection = self.recommendations_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recommendation first")
            return

        recommendation = self.recommendations_list.get(selection[0])
        logger.info(f"Applying recommendation: {recommendation}")
        messagebox.showinfo("Applied", f"Applied recommendation: {recommendation}")

    def _setup_preset_tab(self):
        """Set up the preset application tab."""
        frame = ttk.Frame(self.preset_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Preset Application", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=10
        )

        # Saved presets
        ttk.Label(frame, text="Saved Presets:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.presets_var = tk.StringVar()
        ttk.Combobox(
            frame,
            textvariable=self.presets_var,
            values=["Rain Storm", "Gentle Sleep", "Focus Session", "Nature Relax"],
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Preset details
        ttk.Label(frame, text="Preset Details:").grid(
            row=2, column=0, sticky=tk.NW, pady=5
        )
        self.preset_details = tk.Text(frame, height=8, width=50, wrap=tk.WORD)
        self.preset_details.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Set sample preset details
        self.preset_details.insert(tk.END, "Select a preset to view its details.")

        # Preset actions
        ttk.Button(frame, text="Apply Preset", command=self._apply_preset).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        ttk.Button(
            frame, text="Save Current as Preset", command=self._save_preset
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
        ttk.Button(frame, text="Delete Preset", command=self._delete_preset).grid(
            row=4, column=1, sticky=tk.W, pady=5
        )

        # Bind event to combobox selection
        self.presets_var.trace("w", self._on_preset_selected)

        # Sample preset details (would normally be loaded from a file)
        self.preset_data = {
            "Rain Storm": {
                "description": "A thunderstorm with heavy rain and occasional thunder. Great for deep sleep.",
                "audio": {"sample_rate": "48000", "bit_depth": "24"},
                "mix": {"duration": "120", "transition": "8"},
                "sounds": ["heavy_rain.wav", "distant_thunder.wav", "wind.wav"],
            },
            "Gentle Sleep": {
                "description": "Soft rainfall with gentle background ambience. Perfect for light sleepers.",
                "audio": {"sample_rate": "44100", "bit_depth": "16"},
                "mix": {"duration": "480", "transition": "10"},
                "sounds": ["light_rain.wav", "white_noise_soft.wav"],
            },
            "Focus Session": {
                "description": "Brown noise with subtle cafe background. Designed for productivity and focus.",
                "audio": {"sample_rate": "48000", "bit_depth": "24"},
                "mix": {"duration": "90", "transition": "5"},
                "sounds": ["brown_noise.wav", "cafe_distant.wav"],
            },
            "Nature Relax": {
                "description": "Forest sounds with birds and a distant stream. Creates a relaxing natural environment.",
                "audio": {"sample_rate": "44100", "bit_depth": "16"},
                "mix": {"duration": "120", "transition": "15"},
                "sounds": [
                    "forest_ambience.wav",
                    "birds_morning.wav",
                    "stream_small.wav",
                ],
            },
        }

    def _on_preset_selected(self, *args):
        """Handle preset selection."""
        preset_name = self.presets_var.get()
        if preset_name in self.preset_data:
            preset = self.preset_data[preset_name]
            details = f"Description: {preset['description']}\n\n"
            details += "Audio Settings:\n"
            details += f"  Sample Rate: {preset['audio']['sample_rate']} Hz\n"
            details += f"  Bit Depth: {preset['audio']['bit_depth']} bits\n\n"
            details += "Mix Settings:\n"
            details += f"  Duration: {preset['mix']['duration']} minutes\n"
            details += f"  Transition: {preset['mix']['transition']} seconds\n\n"
            details += f"Sounds: {', '.join(preset['sounds'])}"

            self.preset_details.delete(1.0, tk.END)
            self.preset_details.insert(tk.END, details)

    def _apply_preset(self):
        """Apply the selected preset."""
        preset_name = self.presets_var.get()
        if not preset_name:
            messagebox.showwarning("Warning", "Please select a preset first")
            return

        if preset_name in self.preset_data:
            preset = self.preset_data[preset_name]

            # Update parameter values from the preset
            self.sample_rate_var.set(preset["audio"]["sample_rate"])
            self.bit_depth_var.set(preset["audio"]["bit_depth"])
            self.duration_var.set(preset["mix"]["duration"])
            self.transition_var.set(preset["mix"]["transition"])

            logger.info(f"Applied preset: {preset_name}")
            messagebox.showinfo(
                "Success", f"Preset '{preset_name}' applied successfully"
            )

    def _save_preset(self):
        """Save the current settings as a preset."""
        # In a real implementation, this would prompt for a name and save to a file
        preset_name = tk.simpledialog.askstring("Save Preset", "Enter preset name:")
        if preset_name:
            logger.info(f"Saved preset: {preset_name}")
            messagebox.showinfo("Success", f"Preset '{preset_name}' saved successfully")

    def _delete_preset(self):
        """Delete the selected preset."""
        preset_name = self.presets_var.get()
        if not preset_name:
            messagebox.showwarning("Warning", "Please select a preset first")
            return

        # In a real implementation, this would delete from a file
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the preset '{preset_name}'?",
        ):
            logger.info(f"Deleted preset: {preset_name}")
            messagebox.showinfo(
                "Success", f"Preset '{preset_name}' deleted successfully"
            )
