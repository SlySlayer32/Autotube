"""Pipeline Control Panel for SonicSleep Pro.

This panel provides complete pipeline workflow control including:
- Full pipeline automation (one-click)
- Step-by-step workflow control
- Progress tracking
- Configuration for all workflow stages
- Status display
"""

import logging
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

logger = logging.getLogger(__name__)


class PipelinePanel:
    """Panel for complete pipeline workflow control."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame

        # Initialize orchestrator (lazy load)
        self._orchestrator = None

        # Track pipeline state
        self.pipeline_running = False
        self.current_step = None

        # Create the main layout
        self._create_ui()

    @property
    def orchestrator(self):
        """Lazy-load the orchestrator."""
        if self._orchestrator is None:
            from project_name.core.orchestrator import AutotubeOrchestrator

            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            video_folder = self.video_folder_var.get()

            self._orchestrator = AutotubeOrchestrator(
                input_folder=input_folder,
                output_folder=output_folder,
                video_folder=video_folder,
            )
        return self._orchestrator

    def _create_ui(self):
        """Create the user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.full_pipeline_frame = ttk.Frame(self.notebook)
        self.step_by_step_frame = ttk.Frame(self.notebook)
        self.status_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.full_pipeline_frame, text="🚀 Full Pipeline")
        self.notebook.add(self.step_by_step_frame, text="📋 Step-by-Step")
        self.notebook.add(self.status_frame, text="📊 Status & Info")

        # Setup each tab
        self._setup_full_pipeline_tab()
        self._setup_step_by_step_tab()
        self._setup_status_tab()

    def _setup_full_pipeline_tab(self):
        """Set up the full pipeline automation tab."""
        frame = ttk.Frame(self.full_pipeline_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            frame, text="Full Pipeline Automation", font=("Arial", 12, "bold")
        ).pack(pady=10)

        ttk.Label(
            frame,
            text="Execute the complete workflow: Mix → Metadata → Video → Upload",
        ).pack(pady=5)

        # Configuration section
        config_frame = ttk.LabelFrame(frame, text="Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=10)

        # Folder configuration
        folders_frame = ttk.Frame(config_frame)
        folders_frame.pack(fill=tk.X, pady=5)

        ttk.Label(folders_frame, text="Input Folder:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.input_folder_var = tk.StringVar(value="input_clips")
        ttk.Entry(folders_frame, textvariable=self.input_folder_var, width=40).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(
            folders_frame,
            text="Browse...",
            command=lambda: self._browse_folder(self.input_folder_var),
        ).grid(row=0, column=2)

        ttk.Label(folders_frame, text="Output Folder:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.output_folder_var = tk.StringVar(value="output_mixes")
        ttk.Entry(folders_frame, textvariable=self.output_folder_var, width=40).grid(
            row=1, column=1, padx=5
        )
        ttk.Button(
            folders_frame,
            text="Browse...",
            command=lambda: self._browse_folder(self.output_folder_var),
        ).grid(row=1, column=2)

        ttk.Label(folders_frame, text="Video Folder:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.video_folder_var = tk.StringVar(value="output_videos")
        ttk.Entry(folders_frame, textvariable=self.video_folder_var, width=40).grid(
            row=2, column=1, padx=5
        )
        ttk.Button(
            folders_frame,
            text="Browse...",
            command=lambda: self._browse_folder(self.video_folder_var),
        ).grid(row=2, column=2)

        # Pipeline options
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill=tk.X, pady=10)

        # Left column
        left_col = ttk.Frame(options_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(left_col, text="Sound Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sound_type_var = tk.StringVar(value="Rain")
        sound_types = ["Rain", "Ocean", "Nature", "Forest", "White Noise", "Binaural"]
        ttk.Combobox(
            left_col, textvariable=self.sound_type_var, values=sound_types, width=15
        ).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(left_col, text="Mix Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.mix_type_var = tk.StringVar(value="sleep")
        ttk.Combobox(
            left_col,
            textvariable=self.mix_type_var,
            values=["sleep", "focus", "relax"],
            width=15,
        ).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(left_col, text="Duration (min):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.duration_var = tk.StringVar(value="60")
        ttk.Entry(left_col, textvariable=self.duration_var, width=15).grid(
            row=2, column=1, padx=5, pady=2
        )

        # Right column
        right_col = ttk.Frame(options_frame)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.use_waveform_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            right_col, text="Use Waveform Visualization", variable=self.use_waveform_var
        ).grid(row=0, column=0, sticky=tk.W, pady=2)

        self.upload_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right_col, text="Upload to YouTube", variable=self.upload_var).grid(
            row=1, column=0, sticky=tk.W, pady=2
        )

        ttk.Label(right_col, text="Privacy:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.privacy_var = tk.StringVar(value="private")
        ttk.Combobox(
            right_col,
            textvariable=self.privacy_var,
            values=["public", "private", "unlisted"],
            width=15,
        ).grid(row=2, column=1, padx=5, pady=2)

        # Action buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        self.run_pipeline_btn = ttk.Button(
            button_frame,
            text="▶ Run Full Pipeline",
            command=self._run_full_pipeline,
            width=20,
        )
        self.run_pipeline_btn.pack(side=tk.LEFT, padx=5)

        self.stop_pipeline_btn = ttk.Button(
            button_frame, text="⏹ Stop", command=self._stop_pipeline, width=15, state="disabled"
        )
        self.stop_pipeline_btn.pack(side=tk.LEFT, padx=5)

        # Progress section
        progress_frame = ttk.LabelFrame(frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, mode="determinate", length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.progress_text_var = tk.StringVar(value="Ready to start pipeline")
        ttk.Label(progress_frame, textvariable=self.progress_text_var).pack(pady=5)

        # Results section
        results_frame = ttk.Frame(progress_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD, state="disabled")
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _setup_step_by_step_tab(self):
        """Set up the step-by-step workflow tab."""
        frame = ttk.Frame(self.step_by_step_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Step-by-Step Workflow Control", font=("Arial", 12, "bold")
        ).pack(pady=10)

        ttk.Label(frame, text="Execute each pipeline stage individually").pack(pady=5)

        # Steps frame
        steps_frame = ttk.Frame(frame)
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Step 1: Audio Mix
        step1_frame = ttk.LabelFrame(steps_frame, text="Step 1: Create Audio Mix", padding="10")
        step1_frame.pack(fill=tk.X, pady=5)

        step1_controls = ttk.Frame(step1_frame)
        step1_controls.pack(fill=tk.X)

        ttk.Label(step1_controls, text="Mix Type:").pack(side=tk.LEFT, padx=5)
        self.step_mix_type_var = tk.StringVar(value="sleep")
        ttk.Combobox(
            step1_controls,
            textvariable=self.step_mix_type_var,
            values=["sleep", "focus", "relax"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(step1_controls, text="Duration (min):").pack(side=tk.LEFT, padx=5)
        self.step_duration_var = tk.StringVar(value="60")
        ttk.Entry(step1_controls, textvariable=self.step_duration_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(step1_controls, text="Create Mix", command=self._step_create_mix).pack(
            side=tk.LEFT, padx=5
        )

        self.step1_result_var = tk.StringVar(value="Not executed")
        ttk.Label(step1_frame, textvariable=self.step1_result_var, foreground="gray").pack(
            pady=5
        )

        # Step 2: Generate Metadata
        step2_frame = ttk.LabelFrame(
            steps_frame, text="Step 2: Generate Metadata", padding="10"
        )
        step2_frame.pack(fill=tk.X, pady=5)

        step2_controls = ttk.Frame(step2_frame)
        step2_controls.pack(fill=tk.X)

        ttk.Label(step2_controls, text="Sound Type:").pack(side=tk.LEFT, padx=5)
        self.step_sound_type_var = tk.StringVar(value="Rain")
        ttk.Combobox(
            step2_controls,
            textvariable=self.step_sound_type_var,
            values=["Rain", "Ocean", "Nature", "Forest", "White Noise"],
            width=12,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            step2_controls, text="Generate Metadata", command=self._step_generate_metadata
        ).pack(side=tk.LEFT, padx=5)

        self.step2_result_var = tk.StringVar(value="Not executed")
        ttk.Label(step2_frame, textvariable=self.step2_result_var, foreground="gray").pack(
            pady=5
        )

        # Step 3: Create Video
        step3_frame = ttk.LabelFrame(steps_frame, text="Step 3: Create Video", padding="10")
        step3_frame.pack(fill=tk.X, pady=5)

        step3_controls = ttk.Frame(step3_frame)
        step3_controls.pack(fill=tk.X)

        ttk.Label(step3_controls, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.step_audio_file_var = tk.StringVar()
        ttk.Entry(step3_controls, textvariable=self.step_audio_file_var, width=30).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(step3_controls, text="Browse...", command=self._browse_audio_file).pack(
            side=tk.LEFT, padx=2
        )

        self.step_waveform_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            step3_controls, text="Waveform", variable=self.step_waveform_var
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(step3_controls, text="Create Video", command=self._step_create_video).pack(
            side=tk.LEFT, padx=5
        )

        self.step3_result_var = tk.StringVar(value="Not executed")
        ttk.Label(step3_frame, textvariable=self.step3_result_var, foreground="gray").pack(
            pady=5
        )

        # Step 4: Upload to YouTube
        step4_frame = ttk.LabelFrame(
            steps_frame, text="Step 4: Upload to YouTube", padding="10"
        )
        step4_frame.pack(fill=tk.X, pady=5)

        step4_controls = ttk.Frame(step4_frame)
        step4_controls.pack(fill=tk.X)

        ttk.Label(step4_controls, text="Video File:").pack(side=tk.LEFT, padx=5)
        self.step_video_file_var = tk.StringVar()
        ttk.Entry(step4_controls, textvariable=self.step_video_file_var, width=30).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(step4_controls, text="Browse...", command=self._browse_video_file).pack(
            side=tk.LEFT, padx=2
        )

        ttk.Label(step4_controls, text="Privacy:").pack(side=tk.LEFT, padx=5)
        self.step_privacy_var = tk.StringVar(value="private")
        ttk.Combobox(
            step4_controls,
            textvariable=self.step_privacy_var,
            values=["public", "private", "unlisted"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(step4_controls, text="Upload", command=self._step_upload_video).pack(
            side=tk.LEFT, padx=5
        )

        self.step4_result_var = tk.StringVar(value="Not executed")
        ttk.Label(step4_frame, textvariable=self.step4_result_var, foreground="gray").pack(
            pady=5
        )

    def _setup_status_tab(self):
        """Set up the status and information tab."""
        frame = ttk.Frame(self.status_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="System Status & Information", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        # Refresh button
        ttk.Button(frame, text="🔄 Refresh Status", command=self._refresh_status).pack(pady=5)

        # Status display
        status_display = ttk.Frame(frame)
        status_display.pack(fill=tk.BOTH, expand=True, pady=10)

        # Folder information
        folders_frame = ttk.LabelFrame(status_display, text="Folder Information", padding="10")
        folders_frame.pack(fill=tk.X, pady=5)

        self.status_text = tk.Text(folders_frame, height=15, wrap=tk.WORD, state="disabled")
        scrollbar = ttk.Scrollbar(folders_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=scrollbar.set)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initialize status
        self._refresh_status()

    def _browse_folder(self, var):
        """Browse for a folder."""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            var.set(folder)
            # Reset orchestrator to use new folders
            self._orchestrator = None

    def _browse_audio_file(self):
        """Browse for an audio file."""
        file = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a"),
                ("All Files", "*.*"),
            ],
        )
        if file:
            self.step_audio_file_var.set(file)

    def _browse_video_file(self):
        """Browse for a video file."""
        file = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")],
        )
        if file:
            self.step_video_file_var.set(file)

    def _run_full_pipeline(self):
        """Run the full pipeline."""
        if self.pipeline_running:
            messagebox.showwarning("Pipeline Running", "Pipeline is already running!")
            return

        # Validate configuration
        try:
            duration = int(self.duration_var.get())
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError as e:
            messagebox.showerror("Invalid Duration", f"Please enter a valid duration: {e}")
            return

        # Update UI state
        self.pipeline_running = True
        self.run_pipeline_btn.config(state="disabled")
        self.stop_pipeline_btn.config(state="normal")
        self.progress_var.set(0)
        self.progress_text_var.set("Starting pipeline...")

        # Clear results
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state="disabled")

        # Run pipeline in background thread
        import threading

        def run():
            try:
                self._log_result("Starting Autotube Pipeline...")
                self._log_result(f"Configuration:")
                self._log_result(f"  Sound Type: {self.sound_type_var.get()}")
                self._log_result(f"  Mix Type: {self.mix_type_var.get()}")
                self._log_result(f"  Duration: {duration} minutes")
                self._log_result(f"  Waveform: {self.use_waveform_var.get()}")
                self._log_result(f"  Upload: {self.upload_var.get()}")
                self._log_result("")

                results = self.orchestrator.run_full_pipeline(
                    sound_type=self.sound_type_var.get(),
                    duration_minutes=duration,
                    mix_type=self.mix_type_var.get(),
                    privacy_status=self.privacy_var.get(),
                    use_waveform=self.use_waveform_var.get(),
                    upload=self.upload_var.get(),
                )

                # Update UI with results
                self.root.after(0, self._handle_pipeline_complete, results)

            except Exception as e:
                logger.error(f"Pipeline error: {e}")
                self.root.after(
                    0,
                    self._handle_pipeline_error,
                    str(e),
                )

        self.root = self.panel.winfo_toplevel()
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def _stop_pipeline(self):
        """Stop the pipeline."""
        # Note: Actual stopping would require interrupt mechanism
        self.pipeline_running = False
        self.run_pipeline_btn.config(state="normal")
        self.stop_pipeline_btn.config(state="disabled")
        self.progress_text_var.set("Pipeline stopped by user")

    def _handle_pipeline_complete(self, results):
        """Handle pipeline completion."""
        self.pipeline_running = False
        self.run_pipeline_btn.config(state="normal")
        self.stop_pipeline_btn.config(state="disabled")
        self.progress_var.set(100)

        if results["success"]:
            self.progress_text_var.set("Pipeline completed successfully!")
            self._log_result("\n✓ Pipeline completed successfully!")

            if results["audio_path"]:
                self._log_result(f"\nAudio: {results['audio_path']}")
            if results["video_path"]:
                self._log_result(f"Video: {results['video_path']}")
            if results["video_id"]:
                self._log_result(f"YouTube ID: {results['video_id']}")
                self._log_result(
                    f"URL: https://www.youtube.com/watch?v={results['video_id']}"
                )

            messagebox.showinfo("Success", "Pipeline completed successfully!")
        else:
            self.progress_text_var.set("Pipeline failed")
            self._log_result("\n✗ Pipeline failed:")
            for error in results.get("errors", []):
                self._log_result(f"  - {error}")

            messagebox.showerror(
                "Pipeline Failed", "Pipeline failed:\n" + "\n".join(results.get("errors", []))
            )

    def _handle_pipeline_error(self, error):
        """Handle pipeline error."""
        self.pipeline_running = False
        self.run_pipeline_btn.config(state="normal")
        self.stop_pipeline_btn.config(state="disabled")
        self.progress_text_var.set("Pipeline error")

        self._log_result(f"\n✗ Error: {error}")
        messagebox.showerror("Pipeline Error", f"Pipeline error: {error}")

    def _log_result(self, message):
        """Log a message to the results text."""
        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state="disabled")

    def _step_create_mix(self):
        """Create audio mix (step 1)."""
        try:
            duration = int(self.step_duration_var.get())
            mix_type = self.step_mix_type_var.get()

            self.step1_result_var.set("Creating mix...")
            self.step1_result_var.config(foreground="blue")

            audio_path = self.orchestrator.create_audio_mix(
                duration_minutes=duration, mix_type=mix_type
            )

            if audio_path:
                self.step_audio_file_var.set(audio_path)
                self.step1_result_var.set(f"✓ Created: {os.path.basename(audio_path)}")
                self.step1_result_var.config(foreground="green")
                messagebox.showinfo("Success", f"Mix created: {audio_path}")
            else:
                self.step1_result_var.set("✗ Failed to create mix")
                self.step1_result_var.config(foreground="red")
                messagebox.showerror("Error", "Failed to create mix")

        except Exception as e:
            self.step1_result_var.set(f"✗ Error: {e}")
            self.step1_result_var.config(foreground="red")
            messagebox.showerror("Error", f"Error creating mix: {e}")

    def _step_generate_metadata(self):
        """Generate metadata (step 2)."""
        try:
            sound_type = self.step_sound_type_var.get()
            duration = int(self.step_duration_var.get())
            duration_hours = max(1, round(duration / 60))
            mix_type = self.step_mix_type_var.get()

            self.step2_result_var.set("Generating metadata...")
            self.step2_result_var.config(foreground="blue")

            metadata = self.orchestrator.generate_metadata(
                sound_type=sound_type,
                duration_hours=duration_hours,
                purpose=mix_type,
            )

            # Store metadata for use in video/upload
            self.current_metadata = metadata

            self.step2_result_var.set(f"✓ Generated: {metadata['title'][:50]}...")
            self.step2_result_var.config(foreground="green")

            # Show metadata in a dialog
            self._show_metadata_dialog(metadata)

        except Exception as e:
            self.step2_result_var.set(f"✗ Error: {e}")
            self.step2_result_var.config(foreground="red")
            messagebox.showerror("Error", f"Error generating metadata: {e}")

    def _step_create_video(self):
        """Create video (step 3)."""
        audio_file = self.step_audio_file_var.get()
        if not audio_file:
            messagebox.showerror("Error", "Please select an audio file")
            return

        if not os.path.exists(audio_file):
            messagebox.showerror("Error", f"Audio file not found: {audio_file}")
            return

        try:
            self.step3_result_var.set("Creating video...")
            self.step3_result_var.config(foreground="blue")

            # Get title from metadata if available
            title = None
            if hasattr(self, "current_metadata"):
                title = self.current_metadata.get("title")

            video_path = self.orchestrator.create_video_from_mix(
                audio_path=audio_file,
                title_text=title if not self.step_waveform_var.get() else None,
                use_waveform=self.step_waveform_var.get(),
            )

            if video_path:
                self.step_video_file_var.set(video_path)
                self.step3_result_var.set(f"✓ Created: {os.path.basename(video_path)}")
                self.step3_result_var.config(foreground="green")
                messagebox.showinfo("Success", f"Video created: {video_path}")
            else:
                self.step3_result_var.set("✗ Failed to create video")
                self.step3_result_var.config(foreground="red")
                messagebox.showerror("Error", "Failed to create video")

        except Exception as e:
            self.step3_result_var.set(f"✗ Error: {e}")
            self.step3_result_var.config(foreground="red")
            messagebox.showerror("Error", f"Error creating video: {e}")

    def _step_upload_video(self):
        """Upload video to YouTube (step 4)."""
        video_file = self.step_video_file_var.get()
        if not video_file:
            messagebox.showerror("Error", "Please select a video file")
            return

        if not os.path.exists(video_file):
            messagebox.showerror("Error", f"Video file not found: {video_file}")
            return

        if not hasattr(self, "current_metadata"):
            messagebox.showerror("Error", "Please generate metadata first (Step 2)")
            return

        try:
            self.step4_result_var.set("Uploading to YouTube...")
            self.step4_result_var.config(foreground="blue")

            metadata = self.current_metadata
            video_id = self.orchestrator.upload_video(
                video_path=video_file,
                title=metadata["title"],
                description=metadata["description"],
                tags=metadata["tags"],
                privacy_status=self.step_privacy_var.get(),
            )

            if video_id:
                self.step4_result_var.set(f"✓ Uploaded: {video_id}")
                self.step4_result_var.config(foreground="green")
                url = f"https://www.youtube.com/watch?v={video_id}"
                messagebox.showinfo("Success", f"Video uploaded!\nID: {video_id}\nURL: {url}")
            else:
                self.step4_result_var.set("✗ Upload failed")
                self.step4_result_var.config(foreground="red")
                messagebox.showerror("Error", "Failed to upload video")

        except Exception as e:
            self.step4_result_var.set(f"✗ Error: {e}")
            self.step4_result_var.config(foreground="red")
            messagebox.showerror("Error", f"Error uploading video: {e}")

    def _show_metadata_dialog(self, metadata):
        """Show metadata in a dialog."""
        dialog = tk.Toplevel(self.panel)
        dialog.title("Generated Metadata")
        dialog.geometry("600x400")

        ttk.Label(dialog, text="Generated Metadata", font=("Arial", 12, "bold")).pack(pady=10)

        text = tk.Text(dialog, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, "TITLE:\n")
        text.insert(tk.END, metadata["title"] + "\n\n")
        text.insert(tk.END, "TAGS:\n")
        text.insert(tk.END, ", ".join(metadata["tags"]) + "\n\n")
        text.insert(tk.END, "DESCRIPTION:\n")
        text.insert(tk.END, metadata["description"])

        text.config(state="disabled")

        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def _refresh_status(self):
        """Refresh the status information."""
        try:
            # Get status from orchestrator
            input_folder = self.input_folder_var.get() if hasattr(self, "input_folder_var") else "input_clips"
            output_folder = self.output_folder_var.get() if hasattr(self, "output_folder_var") else "output_mixes"
            video_folder = self.video_folder_var.get() if hasattr(self, "video_folder_var") else "output_videos"

            # Create temporary orchestrator for status
            from project_name.core.orchestrator import AutotubeOrchestrator

            temp_orch = AutotubeOrchestrator(
                input_folder=input_folder,
                output_folder=output_folder,
                video_folder=video_folder,
            )
            status_info = temp_orch.get_status()

            # Update status display
            self.status_text.config(state="normal")
            self.status_text.delete(1.0, tk.END)

            self.status_text.insert(tk.END, "SYSTEM STATUS\n")
            self.status_text.insert(tk.END, "=" * 60 + "\n\n")

            self.status_text.insert(tk.END, f"Input Folder: {status_info['input_folder']}\n")
            self.status_text.insert(tk.END, f"  Files: {status_info['input_files']}\n\n")

            self.status_text.insert(tk.END, f"Output Folder: {status_info['output_folder']}\n")
            self.status_text.insert(tk.END, f"  Files: {status_info['output_files']}\n\n")

            self.status_text.insert(tk.END, f"Video Folder: {status_info['video_folder']}\n")
            self.status_text.insert(tk.END, f"  Files: {status_info['video_files']}\n\n")

            # List recent files if available
            if status_info["output_files"] > 0:
                self.status_text.insert(tk.END, "\nRecent Output Files:\n")
                output_path = status_info["output_folder"]
                if os.path.exists(output_path):
                    files = sorted(
                        [
                            f
                            for f in os.listdir(output_path)
                            if os.path.isfile(os.path.join(output_path, f))
                        ],
                        key=lambda x: os.path.getmtime(os.path.join(output_path, x)),
                        reverse=True,
                    )[:5]
                    for f in files:
                        self.status_text.insert(tk.END, f"  - {f}\n")

            self.status_text.config(state="disabled")

        except Exception as e:
            logger.error(f"Error refreshing status: {e}")
            self.status_text.config(state="normal")
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Error loading status: {e}")
            self.status_text.config(state="disabled")
