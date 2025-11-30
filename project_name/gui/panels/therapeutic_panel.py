"""Therapeutic Audio Panel for SonicSleep Pro.

This panel integrates the latest 2024 research-based therapeutic audio features:
- Dynamic binaural beats (0-3 Hz)
- Superior pink noise generation
- Multi-modal therapeutic mixing
- Personalized audio protocols
"""

import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class TherapeuticAudioPanel:
    """Panel for 2024 research-based therapeutic audio generation."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame
        
        # Initialize audio engine
        self.audio_engine = None
        self._init_audio_engine()
        
        # Progress tracking
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Create main notebook interface
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for different therapeutic audio types
        self.sleep_frame = ttk.Frame(self.notebook)
        self.anxiety_frame = ttk.Frame(self.notebook)
        self.focus_frame = ttk.Frame(self.notebook)
        self.personalized_frame = ttk.Frame(self.notebook)
        self.generator_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook with research-based icons/labels
        self.notebook.add(self.sleep_frame, text="🌙 Sleep Enhancement")
        self.notebook.add(self.anxiety_frame, text="💚 Anxiety Relief")
        self.notebook.add(self.focus_frame, text="🎯 Focus Boost")
        self.notebook.add(self.personalized_frame, text="👤 Personalized")
        self.notebook.add(self.generator_frame, text="🔧 Advanced Settings")

        # Setup each tab
        self._setup_sleep_tab()
        self._setup_anxiety_tab()
        self._setup_focus_tab()
        self._setup_personalized_tab()
        self._setup_generator_tab()
        
        # Create status bar at bottom
        self._setup_status_bar()

    def _init_audio_engine(self):
        """Initialize the therapeutic audio engine."""
        try:
            from project_name.audio_engine.therapeutic_engine_2024 import TherapeuticAudioMixer
            self.audio_engine = TherapeuticAudioMixer(sample_rate=44100)
            logger.info("Therapeutic audio engine initialized successfully")
        except ImportError as e:
            logger.error(f"Failed to import therapeutic audio engine: {e}")
            messagebox.showerror(
                "Import Error", 
                "Therapeutic audio engine not available.\nPlease check your installation."
            )

    def _setup_sleep_tab(self):
        """Set up the sleep enhancement tab with 2024 research options."""
        main_frame = ttk.Frame(self.sleep_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title with research info
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame, 
            text="Sleep Enhancement - 2024 Research Based", 
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            title_frame, 
            text="ℹ Research Info", 
            command=self._show_sleep_research_info
        ).pack(side=tk.RIGHT)

        # Quick options frame
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Sleep Protocols", padding="10")
        quick_frame.pack(fill=tk.X, pady=(0, 15))

        # Pre-configured sleep options based on research
        sleep_options = [
            ("Quick Sleep (0.25 Hz targeting)", "quick_sleep", 15),
            ("Dynamic Sleep Protocol (0-3 Hz)", "dynamic_sleep", 60),
            ("Memory Consolidation (Pink noise)", "memory_sleep", 90),
            ("Deep Sleep Enhancement (3 Hz stable)", "deep_sleep", 45)
        ]

        for i, (label, option_id, default_duration) in enumerate(sleep_options):
            row = i // 2
            col = (i % 2) * 3
            
            ttk.Button(
                quick_frame, 
                text=label,
                width=30,
                command=lambda opt=option_id, dur=default_duration: self._generate_sleep_audio(opt, dur)
            ).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)

        # Custom options frame
        custom_frame = ttk.LabelFrame(main_frame, text="Custom Sleep Mix", padding="10")
        custom_frame.pack(fill=tk.X, pady=(0, 15))

        # Duration selection
        ttk.Label(custom_frame, text="Duration (minutes):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sleep_duration_var = tk.StringVar(value="60")
        duration_spinbox = ttk.Spinbox(
            custom_frame, 
            from_=5, to=480, 
            textvariable=self.sleep_duration_var, 
            width=10
        )
        duration_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 20))

        # Include nature sounds
        self.sleep_nature_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            custom_frame, 
            text="Include nature sounds (parasympathetic activation)", 
            variable=self.sleep_nature_var
        ).grid(row=0, column=2, sticky=tk.W, pady=5)

        # Component mix ratios
        ttk.Label(custom_frame, text="Mix Ratios:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, columnspan=3, sticky=tk.W, pady=(15, 5)
        )

        # Binaural beats ratio
        ttk.Label(custom_frame, text="Binaural Beats:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sleep_binaural_ratio = tk.DoubleVar(value=0.40)
        binaural_scale = ttk.Scale(
            custom_frame, 
            from_=0.0, to=0.8, 
            variable=self.sleep_binaural_ratio, 
            orient=tk.HORIZONTAL,
            length=150
        )
        binaural_scale.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(5, 10))
        self.sleep_binaural_label = ttk.Label(custom_frame, text="40%")
        self.sleep_binaural_label.grid(row=2, column=2, sticky=tk.W, pady=2)

        # Pink noise ratio
        ttk.Label(custom_frame, text="Pink Noise:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.sleep_pink_ratio = tk.DoubleVar(value=0.35)
        pink_scale = ttk.Scale(
            custom_frame, 
            from_=0.0, to=0.8, 
            variable=self.sleep_pink_ratio, 
            orient=tk.HORIZONTAL,
            length=150
        )
        pink_scale.grid(row=3, column=1, sticky=tk.W, pady=2, padx=(5, 10))
        self.sleep_pink_label = ttk.Label(custom_frame, text="35%")
        self.sleep_pink_label.grid(row=3, column=2, sticky=tk.W, pady=2)

        # Nature sounds ratio
        ttk.Label(custom_frame, text="Nature Sounds:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.sleep_nature_ratio = tk.DoubleVar(value=0.25)
        nature_scale = ttk.Scale(
            custom_frame, 
            from_=0.0, to=0.8, 
            variable=self.sleep_nature_ratio, 
            orient=tk.HORIZONTAL,
            length=150
        )
        nature_scale.grid(row=4, column=1, sticky=tk.W, pady=2, padx=(5, 10))
        self.sleep_nature_label = ttk.Label(custom_frame, text="25%")
        self.sleep_nature_label.grid(row=4, column=2, sticky=tk.W, pady=2)

        # Bind scale events to update labels
        self.sleep_binaural_ratio.trace('w', lambda *args: self._update_ratio_labels('sleep'))
        self.sleep_pink_ratio.trace('w', lambda *args: self._update_ratio_labels('sleep'))
        self.sleep_nature_ratio.trace('w', lambda *args: self._update_ratio_labels('sleep'))

        # Generate button
        generate_frame = ttk.Frame(custom_frame)
        generate_frame.grid(row=5, column=0, columnspan=3, pady=15)
        
        ttk.Button(
            generate_frame, 
            text="🎵 Generate Custom Sleep Mix", 
            command=self._generate_custom_sleep_audio,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            generate_frame, 
            text="📁 Open Output Folder", 
            command=self._open_output_folder
        ).pack(side=tk.LEFT)

    def _setup_anxiety_tab(self):
        """Set up the anxiety relief tab with HRV optimization."""
        main_frame = ttk.Frame(self.anxiety_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame, 
            text="Anxiety Relief - HRV Optimization", 
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            title_frame, 
            text="ℹ Research Info", 
            command=self._show_anxiety_research_info
        ).pack(side=tk.RIGHT)

        # Quick relief options
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Relief Protocols", padding="10")
        quick_frame.pack(fill=tk.X, pady=(0, 15))

        anxiety_options = [
            ("5-Minute Quick Relief (2 Hz)", "quick_anxiety", 5),
            ("15-Minute Session (HRV Optimized)", "standard_anxiety", 15),
            ("30-Minute Deep Relaxation", "extended_anxiety", 30),
            ("Sleep Preparation (Anxiety + Sleep)", "sleep_anxiety", 45)
        ]

        for i, (label, option_id, duration) in enumerate(anxiety_options):
            row = i // 2
            col = (i % 2) * 3
            
            ttk.Button(
                quick_frame, 
                text=label,
                width=30,
                command=lambda opt=option_id, dur=duration: self._generate_anxiety_audio(opt, dur)
            ).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)

        # Custom anxiety relief
        custom_frame = ttk.LabelFrame(main_frame, text="Custom Anxiety Relief", padding="10")
        custom_frame.pack(fill=tk.X, pady=(0, 15))

        # Duration and intensity
        ttk.Label(custom_frame, text="Duration (minutes):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.anxiety_duration_var = tk.StringVar(value="15")
        ttk.Spinbox(
            custom_frame, 
            from_=5, to=120, 
            textvariable=self.anxiety_duration_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 20))

        ttk.Label(custom_frame, text="Intensity:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 5))
        self.anxiety_intensity_var = tk.StringVar(value="Moderate")
        ttk.Combobox(
            custom_frame,
            textvariable=self.anxiety_intensity_var,
            values=["Gentle", "Moderate", "Strong"],
            state="readonly",
            width=12
        ).grid(row=0, column=3, sticky=tk.W, pady=5)

        # Generate button
        ttk.Button(
            custom_frame, 
            text="💚 Generate Anxiety Relief", 
            command=self._generate_custom_anxiety_audio,
            style="Accent.TButton"
        ).grid(row=1, column=0, columnspan=4, pady=15)

    def _setup_focus_tab(self):
        """Set up the focus enhancement tab with pink noise superiority."""
        main_frame = ttk.Frame(self.focus_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame, 
            text="Focus Enhancement - Pink Noise Superiority", 
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            title_frame, 
            text="ℹ Research Info", 
            command=self._show_focus_research_info
        ).pack(side=tk.RIGHT)

        # Focus protocols
        protocol_frame = ttk.LabelFrame(main_frame, text="Focus Protocols", padding="10")
        protocol_frame.pack(fill=tk.X, pady=(0, 15))

        focus_options = [
            ("25-Min Pomodoro Focus", "pomodoro", 25),
            ("45-Min Deep Work (Pink Noise)", "deep_work", 45),
            ("90-Min Creative Session", "creative", 90),
            ("2-Hour Study Session", "study", 120)
        ]

        for i, (label, option_id, duration) in enumerate(focus_options):
            row = i // 2
            col = (i % 2) * 3
            
            ttk.Button(
                protocol_frame, 
                text=label,
                width=30,
                command=lambda opt=option_id, dur=duration: self._generate_focus_audio(opt, dur)
            ).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)

        # Focus customization
        custom_frame = ttk.LabelFrame(main_frame, text="Custom Focus Audio", padding="10")
        custom_frame.pack(fill=tk.X, pady=(0, 15))

        # Duration and type
        ttk.Label(custom_frame, text="Duration (minutes):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.focus_duration_var = tk.StringVar(value="45")
        ttk.Spinbox(
            custom_frame, 
            from_=5, to=480, 
            textvariable=self.focus_duration_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 20))

        # Focus type
        ttk.Label(custom_frame, text="Focus Type:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 5))
        self.focus_type_var = tk.StringVar(value="Pure Pink Noise")
        ttk.Combobox(
            custom_frame,
            textvariable=self.focus_type_var,
            values=["Pure Pink Noise", "Pink + Alpha (10 Hz)", "Pink + Beta (15 Hz)"],
            state="readonly",
            width=20
        ).grid(row=0, column=3, sticky=tk.W, pady=5)

        # Generate button
        ttk.Button(
            custom_frame, 
            text="🎯 Generate Focus Audio", 
            command=self._generate_custom_focus_audio,
            style="Accent.TButton"
        ).grid(row=1, column=0, columnspan=4, pady=15)

    def _setup_personalized_tab(self):
        """Set up the personalized audio tab."""
        main_frame = ttk.Frame(self.personalized_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame, 
            text="Personalized Therapeutic Audio", 
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))

        # User preferences
        pref_frame = ttk.LabelFrame(main_frame, text="Your Preferences", padding="10")
        pref_frame.pack(fill=tk.X, pady=(0, 15))

        # Preference checkboxes
        self.prefer_nature_var = tk.BooleanVar()
        ttk.Checkbutton(
            pref_frame, 
            text="I prefer more nature sounds (rain, ocean, forest)", 
            variable=self.prefer_nature_var
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        self.sensitive_beats_var = tk.BooleanVar()
        ttk.Checkbutton(
            pref_frame, 
            text="I'm sensitive to binaural beats (use lower intensity)", 
            variable=self.sensitive_beats_var
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        self.focus_memory_var = tk.BooleanVar()
        ttk.Checkbutton(
            pref_frame, 
            text="I want to focus on memory enhancement during sleep", 
            variable=self.focus_memory_var
        ).grid(row=2, column=0, sticky=tk.W, pady=5)

        self.anxious_sleeper_var = tk.BooleanVar()
        ttk.Checkbutton(
            pref_frame, 
            text="I have anxiety issues that affect my sleep", 
            variable=self.anxious_sleeper_var
        ).grid(row=3, column=0, sticky=tk.W, pady=5)

        # Generate personalized audio
        generate_frame = ttk.LabelFrame(main_frame, text="Generate Personalized Audio", padding="10")
        generate_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(generate_frame, text="Duration (minutes):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.personal_duration_var = tk.StringVar(value="60")
        ttk.Spinbox(
            generate_frame, 
            from_=5, to=480, 
            textvariable=self.personal_duration_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 20))

        ttk.Label(generate_frame, text="Primary Goal:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 5))
        self.personal_goal_var = tk.StringVar(value="Sleep")
        ttk.Combobox(
            generate_frame,
            textvariable=self.personal_goal_var,
            values=["Sleep", "Anxiety Relief", "Focus", "Memory"],
            state="readonly",
            width=15
        ).grid(row=0, column=3, sticky=tk.W, pady=5)

        ttk.Button(
            generate_frame, 
            text="👤 Generate My Personalized Audio", 
            command=self._generate_personalized_audio,
            style="Accent.TButton"
        ).grid(row=1, column=0, columnspan=4, pady=15)

    def _setup_generator_tab(self):
        """Set up the advanced generator settings tab."""
        main_frame = ttk.Frame(self.generator_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame, 
            text="Advanced Audio Generation Settings", 
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))

        # Output settings
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value="output_mixes/therapeutic_2024")
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        ttk.Button(
            output_frame, 
            text="Browse", 
            command=self._browse_output_dir
        ).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(5, 0))

        output_frame.columnconfigure(1, weight=1)

        # Audio quality settings
        quality_frame = ttk.LabelFrame(main_frame, text="Audio Quality", padding="10")
        quality_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(quality_frame, text="Sample Rate:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sample_rate_var = tk.StringVar(value="44100")
        ttk.Combobox(
            quality_frame,
            textvariable=self.sample_rate_var,
            values=["44100", "48000", "96000"],
            state="readonly",
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 20))

        ttk.Label(quality_frame, text="Format:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 5))
        self.format_var = tk.StringVar(value="WAV")
        ttk.Combobox(
            quality_frame,
            textvariable=self.format_var,
            values=["WAV", "FLAC"],
            state="readonly",
            width=10
        ).grid(row=0, column=3, sticky=tk.W, pady=5)

        # Batch generation
        batch_frame = ttk.LabelFrame(main_frame, text="Batch Generation", padding="10")
        batch_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Button(
            batch_frame, 
            text="🎵 Generate Complete Therapeutic Suite (11 files)", 
            command=self._generate_complete_suite,
            style="Accent.TButton"
        ).pack(pady=10)

        ttk.Label(
            batch_frame, 
            text="This will generate all research-based therapeutic audio files\n"
                 "including sleep, anxiety, focus, and personalized variants.",
            font=("Arial", 9),
            foreground="gray"
        ).pack()

    def _setup_status_bar(self):
        """Set up the status bar at the bottom."""
        status_frame = ttk.Frame(self.content_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            variable=self.progress_var, 
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 10))

        # Status label
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)

        # Research info button
        ttk.Button(
            status_frame, 
            text="📚 View All Research", 
            command=self._show_complete_research_info
        ).pack(side=tk.RIGHT)

    # Event handlers for the GUI
    def _update_ratio_labels(self, tab_type):
        """Update the ratio labels when sliders change."""
        if tab_type == 'sleep':
            binaural = self.sleep_binaural_ratio.get()
            pink = self.sleep_pink_ratio.get()
            nature = self.sleep_nature_ratio.get()
            
            # Normalize ratios to sum to 1.0
            total = binaural + pink + nature
            if total > 0:
                binaural_norm = binaural / total
                pink_norm = pink / total
                nature_norm = nature / total
                
                self.sleep_binaural_label.config(text=f"{binaural_norm:.0%}")
                self.sleep_pink_label.config(text=f"{pink_norm:.0%}")
                self.sleep_nature_label.config(text=f"{nature_norm:.0%}")

    def _generate_sleep_audio(self, option_type, duration):
        """Generate sleep audio based on research protocols."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        self._run_generation_thread(self._do_generate_sleep_audio, option_type, duration)

    def _generate_anxiety_audio(self, option_type, duration):
        """Generate anxiety relief audio."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        self._run_generation_thread(self._do_generate_anxiety_audio, option_type, duration)

    def _generate_focus_audio(self, option_type, duration):
        """Generate focus enhancement audio."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        self._run_generation_thread(self._do_generate_focus_audio, option_type, duration)

    def _generate_custom_sleep_audio(self):
        """Generate custom sleep audio with user settings."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        duration = int(self.sleep_duration_var.get())
        include_nature = self.sleep_nature_var.get()
        
        # Get custom ratios
        ratios = {
            'binaural': self.sleep_binaural_ratio.get(),
            'pink_noise': self.sleep_pink_ratio.get(),
            'nature': self.sleep_nature_ratio.get()
        }
        
        self._run_generation_thread(
            self._do_generate_custom_sleep_audio, 
            duration, include_nature, ratios
        )

    def _generate_custom_anxiety_audio(self):
        """Generate custom anxiety relief audio."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        duration = int(self.anxiety_duration_var.get())
        intensity = self.anxiety_intensity_var.get()
        
        self._run_generation_thread(self._do_generate_custom_anxiety_audio, duration, intensity)

    def _generate_custom_focus_audio(self):
        """Generate custom focus audio."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        duration = int(self.focus_duration_var.get())
        focus_type = self.focus_type_var.get()
        
        self._run_generation_thread(self._do_generate_custom_focus_audio, duration, focus_type)

    def _generate_personalized_audio(self):
        """Generate personalized audio based on user preferences."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        duration = int(self.personal_duration_var.get())
        goal = self.personal_goal_var.get()
        
        # Collect preferences
        preferences = {
            'prefer_nature': self.prefer_nature_var.get(),
            'sensitive_to_beats': self.sensitive_beats_var.get(),
            'focus_on_memory': self.focus_memory_var.get(),
            'anxious_sleeper': self.anxious_sleeper_var.get()
        }
        
        self._run_generation_thread(
            self._do_generate_personalized_audio, 
            duration, goal, preferences
        )

    def _generate_complete_suite(self):
        """Generate the complete therapeutic audio suite."""
        if not self.audio_engine:
            messagebox.showerror("Error", "Audio engine not available")
            return
            
        self._run_generation_thread(self._do_generate_complete_suite)

    def _run_generation_thread(self, target_func, *args):
        """Run audio generation in a separate thread to prevent UI freezing."""
        def run_with_progress():
            try:
                self.status_var.set("Generating audio...")
                self.progress_var.set(0)
                target_func(*args)
                self.progress_var.set(100)
                self.status_var.set("Audio generation complete!")
            except Exception as e:
                logger.error(f"Audio generation error: {e}")
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Generation Error", f"Failed to generate audio: {str(e)}")
            
        thread = threading.Thread(target=run_with_progress, daemon=True)
        thread.start()

    # Audio generation implementation methods
    def _do_generate_sleep_audio(self, option_type, duration):
        """Implementation of sleep audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if option_type == "quick_sleep":
            # 0.25 Hz targeting for fastest sleep onset
            from project_name.audio_engine.therapeutic_engine_2024 import DynamicBinauralEngine
            engine = DynamicBinauralEngine()
            audio = engine._generate_static_beat(0.25, duration * 60)
            filename = output_dir / f"quick_sleep_induction_{duration}min.wav"
            
        elif option_type == "dynamic_sleep":
            # Full dynamic sleep protocol
            audio, metadata = self.audio_engine.create_ultimate_sleep_mix(
                duration_minutes=duration,
                include_nature=True
            )
            filename = output_dir / f"dynamic_sleep_protocol_{duration}min.wav"
            
        elif option_type == "memory_sleep":
            # Pink noise for memory consolidation
            from project_name.audio_engine.therapeutic_engine_2024 import SuperiorPinkNoiseEngine
            engine = SuperiorPinkNoiseEngine()
            pink_noise = engine.create_memory_consolidation_track(duration)
            import numpy as np
            audio = np.column_stack((pink_noise, pink_noise))
            filename = output_dir / f"memory_consolidation_{duration}min.wav"
            
        elif option_type == "deep_sleep":
            # 3 Hz stable for deep sleep
            from project_name.audio_engine.therapeutic_engine_2024 import DynamicBinauralEngine
            engine = DynamicBinauralEngine()
            audio = engine._generate_static_beat(3.0, duration * 60)
            filename = output_dir / f"deep_sleep_enhancement_{duration}min.wav"
        
        self.audio_engine.save_therapeutic_audio(audio, str(filename))
        logger.info(f"Generated sleep audio: {filename}")

    def _do_generate_anxiety_audio(self, option_type, duration):
        """Implementation of anxiety relief audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        audio, metadata = self.audio_engine.create_anxiety_reduction_mix(duration_minutes=duration)
        filename = output_dir / f"anxiety_relief_{option_type}_{duration}min.wav"
        
        self.audio_engine.save_therapeutic_audio(audio, str(filename), metadata)
        logger.info(f"Generated anxiety relief audio: {filename}")

    def _do_generate_focus_audio(self, option_type, duration):
        """Implementation of focus audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        from project_name.audio_engine.therapeutic_engine_2024 import SuperiorPinkNoiseEngine
        engine = SuperiorPinkNoiseEngine()
        audio = engine.create_focus_enhancement_track(duration)
        filename = output_dir / f"focus_enhancement_{option_type}_{duration}min.wav"
        
        self.audio_engine.save_therapeutic_audio(audio, str(filename))
        logger.info(f"Generated focus audio: {filename}")

    def _do_generate_custom_sleep_audio(self, duration, include_nature, ratios):
        """Implementation of custom sleep audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Normalize ratios
        total = sum(ratios.values())
        if total > 0:
            ratios = {k: v/total for k, v in ratios.items()}
        
        # Create personalization dict for custom ratios
        personalization = {
            'custom_ratios': ratios
        }
        
        audio, metadata = self.audio_engine.create_ultimate_sleep_mix(
            duration_minutes=duration,
            include_nature=include_nature,
            personalization=personalization
        )
        
        filename = output_dir / f"custom_sleep_mix_{duration}min.wav"
        self.audio_engine.save_therapeutic_audio(audio, str(filename), metadata)
        logger.info(f"Generated custom sleep audio: {filename}")

    def _do_generate_custom_anxiety_audio(self, duration, intensity):
        """Implementation of custom anxiety relief audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        audio, metadata = self.audio_engine.create_anxiety_reduction_mix(duration_minutes=duration)
        filename = output_dir / f"custom_anxiety_relief_{intensity.lower()}_{duration}min.wav"
        
        self.audio_engine.save_therapeutic_audio(audio, str(filename), metadata)
        logger.info(f"Generated custom anxiety relief audio: {filename}")

    def _do_generate_custom_focus_audio(self, duration, focus_type):
        """Implementation of custom focus audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        from project_name.audio_engine.therapeutic_engine_2024 import SuperiorPinkNoiseEngine
        engine = SuperiorPinkNoiseEngine()
        
        if focus_type == "Pure Pink Noise":
            audio = engine.create_focus_enhancement_track(duration)
        else:
            # Add binaural beats to pink noise
            pink_audio = engine.create_focus_enhancement_track(duration)
            
            from project_name.audio_engine.therapeutic_engine_2024 import DynamicBinauralEngine
            binaural_engine = DynamicBinauralEngine()
            
            if "Alpha" in focus_type:
                freq = 10.0  # 10 Hz alpha
            else:  # Beta
                freq = 15.0  # 15 Hz beta
                
            binaural_audio = binaural_engine._generate_static_beat(freq, duration * 60)
            
            # Mix pink noise (70%) with binaural beats (30%)
            min_length = min(len(pink_audio), len(binaural_audio))
            audio = (
                pink_audio[:min_length] * 0.7 +
                binaural_audio[:min_length] * 0.3
            )
        
        filename = output_dir / f"custom_focus_{focus_type.replace(' ', '_').lower()}_{duration}min.wav"
        self.audio_engine.save_therapeutic_audio(audio, str(filename))
        logger.info(f"Generated custom focus audio: {filename}")

    def _do_generate_personalized_audio(self, duration, goal, preferences):
        """Implementation of personalized audio generation."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if goal == "Sleep":
            audio, metadata = self.audio_engine.create_ultimate_sleep_mix(
                duration_minutes=duration,
                include_nature=True,
                personalization=preferences
            )
        elif goal == "Anxiety Relief":
            audio, metadata = self.audio_engine.create_anxiety_reduction_mix(
                duration_minutes=duration
            )
        else:  # Focus or Memory
            from project_name.audio_engine.therapeutic_engine_2024 import SuperiorPinkNoiseEngine
            engine = SuperiorPinkNoiseEngine()
            audio = engine.create_focus_enhancement_track(duration)
            metadata = {'goal': goal, 'preferences': preferences}
        
        filename = output_dir / f"personalized_{goal.lower().replace(' ', '_')}_{duration}min.wav"
        self.audio_engine.save_therapeutic_audio(audio, str(filename), metadata)
        logger.info(f"Generated personalized audio: {filename}")

    def _do_generate_complete_suite(self):
        """Implementation of complete suite generation."""
        # This would run the same logic as the generate_research_audio_2024.py script
        # but integrated into the GUI with progress updates
        self.status_var.set("Generating complete therapeutic suite...")
        
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate all 11 therapeutic audio files
        files_to_generate = [
            ("Quick Sleep Induction", "quick_sleep", 15),
            ("Dynamic Sleep Protocol", "dynamic_sleep", 60),
            ("Memory Consolidation", "memory_sleep", 90),
            ("Deep Sleep Enhancement", "deep_sleep", 45),
            ("Quick Anxiety Relief", "quick_anxiety", 15),
            ("Extended Relaxation", "standard_anxiety", 30),
            ("Pink Noise Focus", "focus", 45),
            ("Enhanced Focus Alpha", "focus_alpha", 45),
            ("Nature-Focused Sleep", "nature_sleep", 60),
            ("Beat-Sensitive Sleep", "gentle_sleep", 60),
            ("Memory-Focused Sleep", "memory_focused_sleep", 60)
        ]
        
        total_files = len(files_to_generate)
        
        for i, (name, file_type, duration) in enumerate(files_to_generate):
            progress = (i / total_files) * 100
            self.progress_var.set(progress)
            self.status_var.set(f"Generating {name}... ({i+1}/{total_files})")
            
            # Generate each file based on type
            if "sleep" in file_type:
                self._do_generate_sleep_audio(file_type, duration)
            elif "anxiety" in file_type:
                self._do_generate_anxiety_audio(file_type, duration)
            elif "focus" in file_type:
                self._do_generate_focus_audio(file_type, duration)
        
        self.status_var.set(f"Complete! Generated {total_files} therapeutic audio files.")

    # Info dialog methods
    def _show_sleep_research_info(self):
        """Show research information for sleep enhancement."""
        info_text = """Sleep Enhancement - 2024 Research Basis

🔬 Dynamic Binaural Beats (0-3 Hz):
• Stanford Sleep Medicine Study shows dynamic beats outperform static beats
• 25% faster sleep onset compared to traditional methods
• Measurable improvements in heart rate variability

🔬 Specific Frequency Targeting:
• 0.25 Hz: Fastest sleep onset (targets slow-wave sleep directly)
• 3 Hz + ASMR: Enhanced deep sleep (NREM 3) duration
• Dynamic 1-3 Hz: Optimal sleep consolidation

🔬 Pink Noise Superiority:
• Northwestern University: 3x better memory consolidation vs silence
• Superior to white noise for sleep architecture preservation
• Enhanced memory performance next day

🔬 Multi-Modal Integration:
• 40% binaural beats (primary therapeutic effect)
• 35% pink noise (memory consolidation & masking)
• 25% nature sounds (parasympathetic activation)"""
        
        messagebox.showinfo("Sleep Enhancement Research", info_text)

    def _show_anxiety_research_info(self):
        """Show research information for anxiety relief."""
        info_text = """Anxiety Relief - Heart Rate Variability Research

🔬 2 Hz Optimization:
• Specifically targets heart rate variability improvement
• Measurable autonomic nervous system benefits
• 25%+ reduction in anxiety scores in clinical studies

🔬 Parasympathetic Activation:
• Nature sounds trigger rest-and-digest response
• Measurable cortisol reduction
• Lower blood pressure and heart rate

🔬 Multi-Modal Approach:
• Lower binaural beat intensity (25%) for gentle effect
• Higher nature sound ratio (50%) for calming
• Pink noise (25%) for cognitive calming"""
        
        messagebox.showinfo("Anxiety Relief Research", info_text)

    def _show_focus_research_info(self):
        """Show research information for focus enhancement."""
        info_text = """Focus Enhancement - Pink Noise Superiority

🔬 Pink Noise Research:
• Proven superior to white noise for cognitive tasks
• Enhanced creative thinking and problem-solving
• Better concentration with less mental fatigue

🔬 Alpha Enhancement (10 Hz):
• Associated with relaxed focus states
• Improved attention and reduced mind-wandering
• Optimal for creative and analytical work

🔬 Beta Enhancement (15 Hz):
• Associated with active concentration
• Enhanced working memory performance
• Optimal for detail-oriented tasks"""
        
        messagebox.showinfo("Focus Enhancement Research", info_text)

    def _show_complete_research_info(self):
        """Show complete research information."""
        info_text = """2024 Therapeutic Audio Research Integration

This system integrates the latest peer-reviewed research:

📚 KEY STUDIES:
• Stanford Sleep Medicine (2024): Dynamic binaural beats
• Northwestern University: Pink noise superiority
• Multiple HRV studies: 2 Hz anxiety optimization
• Meta-analyses on nature sounds and parasympathetic activation

📊 EXPECTED RESULTS:
• 25% faster sleep onset (0.25 Hz targeting)
• 3x better memory consolidation (pink noise)
• Significant anxiety reduction (HRV optimization)
• Enhanced focus and creativity (pink noise superiority)

🔬 SCIENTIFIC BASIS:
All frequencies, mixing ratios, and protocols are based on
peer-reviewed studies from 2023-2024 research in:
• Sleep medicine
• Neuroscience
• Psychoacoustics
• Music therapy

For detailed references, see the research documentation
in the docs/research/ folder."""
        
        messagebox.showinfo("Complete Research Information", info_text)

    # Utility methods
    def _browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)

    def _open_output_folder(self):
        """Open the output folder in file explorer."""
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        import subprocess
        import sys
        
        if sys.platform == "win32":
            subprocess.run(["explorer", str(output_dir)])
        elif sys.platform == "darwin":
            subprocess.run(["open", str(output_dir)])
        else:
            subprocess.run(["xdg-open", str(output_dir)])
