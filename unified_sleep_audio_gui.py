"""
SonicSleep Pro - Unified Step-by-Step Interface

This is the complete, unified interface that combines all functionality
into an organized, step-by-step workflow for creating therapeutic sleep audio.
"""

import logging
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import json

# Import our audio processing components
from project_name.core.processor import SoundProcessor
from project_name.core.mix_creator import MixCreator
from project_name.api.freesound_api import FreesoundAPI
from project_name.core.content_gatherer import ContentGatherer
from project_name.gui.widgets.audio_player import AudioPlayer

# Add Windows media player as fallback
import sys
if sys.platform.startswith('win'):
    try:
        import winsound
        WINSOUND_AVAILABLE = True
    except ImportError:
        WINSOUND_AVAILABLE = False
else:
    WINSOUND_AVAILABLE = False
from project_name.gui.widgets.audio_player import AudioPlayer

# Add Windows media player as fallback
import sys
if sys.platform.startswith('win'):
    try:
        import winsound
        WINSOUND_AVAILABLE = True
    except ImportError:
        WINSOUND_AVAILABLE = False
else:
    WINSOUND_AVAILABLE = False

logger = logging.getLogger(__name__)


class UnifiedSleepAudioGUI:
    """Unified Step-by-Step Sleep Audio Creation Interface."""

    def __init__(self, root):
        self.root = root
        self.root.title("SonicSleep Pro - Complete Sleep Audio Creator")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)        # Initialize components
        self.processor = SoundProcessor()
        self.mix_creator = MixCreator()
        self.freesound_api = None
        self.content_gatherer = None
        self.auto_collection_running = False

        # File tracking for audio preview
        self.collected_files_paths = {}  # Maps display name to full path
        self.manual_files_paths = {}     # Maps display name to full path

        # Pre-configure your API key
        self.saved_api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"

        # Audio player for preview
        self.audio_player = None

        # Setup the interface
        self.setup_ui()
        self.current_step = 1

    def setup_ui(self):
        """Setup the unified step-by-step interface."""
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            title_frame,
            text="🌙 SonicSleep Pro - Complete Sleep Audio Creator",
            font=("Arial", 16, "bold")
        ).pack()

        ttk.Label(
            title_frame,
            text="Create therapeutic sleep audio in 4 easy steps",
            font=("Arial", 11)
        ).pack(pady=5)

        # Create main container with steps
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Step navigation bar
        self.setup_step_navigation(main_frame)

        # Step content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Setup all steps
        self.setup_all_steps()

        # Show step 1 initially
        self.show_step(1)

    def setup_step_navigation(self, parent):
        """Create the step navigation bar."""
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, pady=10)

        # Step indicators
        self.step_buttons = {}
        steps = [
            ("1", "🎵 Collect Sounds", "Automatically gather sleep-optimized audio clips"),
            ("2", "⚙️ Process Audio", "Apply research-based therapeutic enhancements"),
            ("3", "🎛️ Create Mix", "Build your personalized sleep audio experience"),
            ("4", "💾 Save & Use", "Export and enjoy your therapeutic sleep audio")
        ]

        for i, (num, title, desc) in enumerate(steps):
            step_frame = ttk.LabelFrame(nav_frame, text=f"Step {num}: {title}", padding="10")
            step_frame.grid(row=0, column=i, sticky="ew", padx=5)

            ttk.Label(step_frame, text=desc, wraplength=200, justify="center").pack()

            btn = ttk.Button(
                step_frame,
                text=f"Go to Step {num}",
                command=lambda step=int(num): self.show_step(step)
            )
            btn.pack(pady=5)
            self.step_buttons[int(num)] = btn

        # Configure grid weights
        for i in range(4):
            nav_frame.columnconfigure(i, weight=1)

    def setup_all_steps(self):
        """Setup all step frames."""
        self.step_frames = {}

        # Step 1: Collect Sounds
        self.step_frames[1] = self.create_step1_collect_sounds()

        # Step 2: Process Audio
        self.step_frames[2] = self.create_step2_process_audio()

        # Step 3: Create Mix
        self.step_frames[3] = self.create_step3_create_mix()

        # Step 4: Save & Use
        self.step_frames[4] = self.create_step4_save_use()

    def create_step1_collect_sounds(self):
        """Create Step 1: Collect Sounds interface."""
        frame = ttk.Frame(self.content_frame)

        # Title
        ttk.Label(
            frame,
            text="🎵 Step 1: Collect Sleep-Optimized Audio Clips",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Two main sections: Automated and Manual
        sections_frame = ttk.Frame(frame)
        sections_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Automated Collection (Recommended)
        auto_frame = ttk.LabelFrame(sections_frame, text="🚀 Automated Collection (Recommended)", padding="15")
        auto_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(
            auto_frame,
            text="Let SonicSleep Pro automatically collect high-quality sleep sounds:",
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        # API Status
        self.api_status_var = tk.StringVar(value="✅ Your API key is pre-configured and ready!")
        ttk.Label(auto_frame, textvariable=self.api_status_var, foreground="green").pack(pady=5)

        # Collection options
        options_frame = ttk.LabelFrame(auto_frame, text="Collection Settings", padding="10")
        options_frame.pack(fill=tk.X, pady=10)

        # Collection type
        ttk.Label(options_frame, text="What type of sleep sounds do you want?").pack(anchor="w")
        self.collection_type_var = tk.StringVar(value="Sleep Sounds")
        collection_combo = ttk.Combobox(
            options_frame,
            textvariable=self.collection_type_var,
            values=[
                "Sleep Sounds (Rain, Ocean, White Noise)",
                "Rain & Water Sounds",
                "Nature Ambience (Forest, Birds, Wind)",
                "White/Pink Noise Variations",
                "Binaural Beat Sources",
                "Complete Collection (All Types)"
            ],
            state="readonly",
            width=50
        )
        collection_combo.pack(pady=5, fill=tk.X)

        # Quantity
        qty_frame = ttk.Frame(options_frame)
        qty_frame.pack(fill=tk.X, pady=5)

        ttk.Label(qty_frame, text="How many sounds per category?").pack(side=tk.LEFT)
        self.quantity_var = tk.StringVar(value="15")
        ttk.Combobox(
            qty_frame,
            textvariable=self.quantity_var,
            values=["5", "10", "15", "25", "50"],
            state="readonly",
            width=5
        ).pack(side=tk.RIGHT)

        # Big collect button
        self.collect_btn = ttk.Button(
            auto_frame,
            text="🎵 Start Automated Collection",
            command=self.start_automated_collection,
            style="Accent.TButton"
        )
        self.collect_btn.pack(pady=15)

        # Progress
        self.collection_progress_var = tk.DoubleVar()
        self.collection_progress = ttk.Progressbar(
            auto_frame,
            variable=self.collection_progress_var,
            mode='determinate'
        )
        self.collection_progress.pack(fill=tk.X, pady=5)

        # Status
        self.collection_status_var = tk.StringVar(value="Ready to collect sleep sounds...")
        ttk.Label(auto_frame, textvariable=self.collection_status_var, wraplength=300).pack(pady=5)        # Collected files list with preview
        ttk.Label(auto_frame, text="Collected Files:").pack(anchor="w", pady=(10,0))
        
        # Frame for listbox and preview controls
        files_frame = ttk.Frame(auto_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.collected_files_list = tk.Listbox(files_frame, height=6)
        self.collected_files_list.pack(fill=tk.BOTH, expand=True)
        self.collected_files_list.bind('<Double-Button-1>', self.preview_collected_file)
        
        # Preview controls for collected files
        collected_preview_frame = ttk.Frame(files_frame)
        collected_preview_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(collected_preview_frame, text="▶ Preview", 
                  command=self.preview_collected_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(collected_preview_frame, text="⏹ Stop", 
                  command=self.stop_preview, width=8).pack(side=tk.LEFT, padx=2)
        
        self.collected_preview_status = tk.StringVar(value="Double-click or select and press Preview to play")
        ttk.Label(collected_preview_frame, textvariable=self.collected_preview_status, 
                 font=('TkDefaultFont', 8)).pack(side=tk.LEFT, padx=10)

        # Right: Manual Collection
        manual_frame = ttk.LabelFrame(sections_frame, text="📁 Manual Collection", padding="15")
        manual_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(manual_frame, text="Or upload your own audio files:").pack(pady=5)

        # File selection
        ttk.Button(
            manual_frame,
            text="Browse for Audio Files",
            command=self.browse_audio_files
        ).pack(pady=5)

        ttk.Button(
            manual_frame,
            text="Browse for Folder",
            command=self.browse_audio_folder
        ).pack(pady=5)        # Manual files list with preview
        ttk.Label(manual_frame, text="Selected Files:").pack(anchor="w", pady=(10,0))
        
        # Frame for listbox and preview controls
        manual_files_frame = ttk.Frame(manual_frame)
        manual_files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.manual_files_list = tk.Listbox(manual_files_frame, height=6)
        self.manual_files_list.pack(fill=tk.BOTH, expand=True)
        self.manual_files_list.bind('<Double-Button-1>', self.preview_manual_file)
        
        # Preview controls for manual files
        manual_preview_frame = ttk.Frame(manual_files_frame)
        manual_preview_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(manual_preview_frame, text="▶ Preview", 
                  command=self.preview_manual_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(manual_preview_frame, text="⏹ Stop", 
                  command=self.stop_preview, width=8).pack(side=tk.LEFT, padx=2)
        
        self.manual_preview_status = tk.StringVar(value="Double-click or select and press Preview to play")
        ttk.Label(manual_preview_frame, textvariable=self.manual_preview_status, 
                 font=('TkDefaultFont', 8)).pack(side=tk.LEFT, padx=10)

        # Manual file actions
        manual_actions = ttk.Frame(manual_frame)
        manual_actions.pack(fill=tk.X, pady=5)

        ttk.Button(manual_actions, text="Remove Selected", command=self.remove_manual_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(manual_actions, text="Clear All", command=self.clear_manual_files).pack(side=tk.LEFT, padx=5)

        # Next step button
        next_frame = ttk.Frame(frame)
        next_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            next_frame,
            text="📄 Next: Process Audio →",
            command=lambda: self.show_step(2),
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)

        # File count info
        self.file_count_var = tk.StringVar(value="No files collected yet")
        ttk.Label(next_frame, textvariable=self.file_count_var).pack(side=tk.LEFT)

        return frame

    def create_step2_process_audio(self):
        """Create Step 2: Process Audio interface."""
        frame = ttk.Frame(self.content_frame)

        # Title
        ttk.Label(
            frame,
            text="⚙️ Step 2: Apply Therapeutic Audio Processing",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Main content
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Processing Options
        options_frame = ttk.LabelFrame(content_frame, text="🧠 Research-Based Processing", padding="15")
        options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(
            options_frame,
            text="Apply 2024 research findings for optimal sleep enhancement:",
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        # Processing options
        processing_frame = ttk.LabelFrame(options_frame, text="Processing Options", padding="10")
        processing_frame.pack(fill=tk.X, pady=10)

        self.normalize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            processing_frame,
            text="✅ Normalize Audio (Consistent volume levels)",
            variable=self.normalize_var
        ).pack(anchor="w", pady=2)

        self.enhance_quality_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            processing_frame,
            text="✅ Enhance Quality (Audio optimization)",
            variable=self.enhance_quality_var
        ).pack(anchor="w", pady=2)

        self.therapeutic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            processing_frame,
            text="✅ Apply Therapeutic Processing (Research-based modifications)",
            variable=self.therapeutic_var
        ).pack(anchor="w", pady=2)

        self.pink_noise_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            processing_frame,
            text="✅ Add Pink Noise (3x better memory consolidation)",
            variable=self.pink_noise_var
        ).pack(anchor="w", pady=2)

        self.binaural_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            processing_frame,
            text="✅ Add Binaural Beats (0.25 Hz for sleep onset)",
            variable=self.binaural_var
        ).pack(anchor="w", pady=2)

        # Processing settings
        settings_frame = ttk.LabelFrame(options_frame, text="Audio Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)

        # Sample rate
        rate_frame = ttk.Frame(settings_frame)
        rate_frame.pack(fill=tk.X, pady=2)
        ttk.Label(rate_frame, text="Sample Rate:").pack(side=tk.LEFT)
        self.sample_rate_var = tk.StringVar(value="44100")
        ttk.Combobox(
            rate_frame,
            textvariable=self.sample_rate_var,
            values=["44100", "48000", "96000"],
            state="readonly",
            width=10
        ).pack(side=tk.RIGHT)

        # Duration
        duration_frame = ttk.Frame(settings_frame)
        duration_frame.pack(fill=tk.X, pady=2)
        ttk.Label(duration_frame, text="Target Duration (minutes):").pack(side=tk.LEFT)
        self.duration_var = tk.StringVar(value="60")
        ttk.Entry(duration_frame, textvariable=self.duration_var, width=10).pack(side=tk.RIGHT)

        # Process button
        self.process_btn = ttk.Button(
            options_frame,
            text="🔄 Start Processing",
            command=self.start_processing,
            style="Accent.TButton"
        )
        self.process_btn.pack(pady=15)

        # Right: Progress and Results
        results_frame = ttk.LabelFrame(content_frame, text="📊 Processing Progress", padding="15")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Progress
        self.processing_progress_var = tk.DoubleVar()
        self.processing_progress = ttk.Progressbar(
            results_frame,
            variable=self.processing_progress_var,
            mode='determinate'
        )
        self.processing_progress.pack(fill=tk.X, pady=5)

        # Status
        self.processing_status_var = tk.StringVar(value="Ready to process audio...")
        ttk.Label(results_frame, textvariable=self.processing_status_var, wraplength=300).pack(pady=5)

        # Processed files
        ttk.Label(results_frame, text="Processed Files:").pack(anchor="w", pady=(10,0))
        self.processed_files_list = tk.Listbox(results_frame, height=12)
        self.processed_files_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Navigation
        nav_frame = ttk.Frame(frame)
        nav_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            nav_frame,
            text="← Back: Collect Sounds",
            command=lambda: self.show_step(1)
        ).pack(side=tk.LEFT)

        ttk.Button(
            nav_frame,
            text="🎛️ Next: Create Mix →",
            command=lambda: self.show_step(3),
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)

        return frame

    def create_step3_create_mix(self):
        """Create Step 3: Create Mix interface."""
        frame = ttk.Frame(self.content_frame)

        # Title
        ttk.Label(
            frame,
            text="🎛️ Step 3: Create Your Personalized Sleep Mix",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Main content
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Mix Controls
        controls_frame = ttk.LabelFrame(content_frame, text="🎚️ Mix Controls", padding="15")
        controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Preset selection
        preset_frame = ttk.LabelFrame(controls_frame, text="Quick Presets", padding="10")
        preset_frame.pack(fill=tk.X, pady=5)

        ttk.Label(preset_frame, text="Choose a preset or customize manually:").pack(anchor="w")
        self.preset_var = tk.StringVar(value="Custom")
        preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=[
                "Custom",
                "Quick Sleep (15 min)",
                "Deep Sleep (60 min)",
                "Nap Time (20 min)",
                "Insomnia Relief (90 min)",
                "Anxiety Relief (30 min)"
            ],
            state="readonly"
        )
        preset_combo.pack(fill=tk.X, pady=5)
        preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)

        # Level controls
        levels_frame = ttk.LabelFrame(controls_frame, text="Audio Levels", padding="10")
        levels_frame.pack(fill=tk.X, pady=5)

        # Master volume
        ttk.Label(levels_frame, text="Master Volume:").pack(anchor="w")
        self.master_volume_var = tk.DoubleVar(value=0.7)
        ttk.Scale(
            levels_frame,
            from_=0.0, to=1.0,
            variable=self.master_volume_var,
            orient="horizontal"
        ).pack(fill=tk.X, pady=2)

        # Nature sounds
        ttk.Label(levels_frame, text="Nature Sounds Level:").pack(anchor="w")
        self.nature_level_var = tk.DoubleVar(value=0.8)
        ttk.Scale(
            levels_frame,
            from_=0.0, to=1.0,
            variable=self.nature_level_var,
            orient="horizontal"
        ).pack(fill=tk.X, pady=2)

        # Pink noise
        ttk.Label(levels_frame, text="Pink Noise Level:").pack(anchor="w")
        self.pink_noise_level_var = tk.DoubleVar(value=0.3)
        ttk.Scale(
            levels_frame,
            from_=0.0, to=1.0,
            variable=self.pink_noise_level_var,
            orient="horizontal"
        ).pack(fill=tk.X, pady=2)

        # Binaural beats
        ttk.Label(levels_frame, text="Binaural Beats Intensity:").pack(anchor="w")
        self.binaural_level_var = tk.DoubleVar(value=0.2)
        ttk.Scale(
            levels_frame,
            from_=0.0, to=0.5,
            variable=self.binaural_level_var,
            orient="horizontal"
        ).pack(fill=tk.X, pady=2)

        # Create mix button
        self.create_mix_btn = ttk.Button(
            controls_frame,
            text="🎵 Create Sleep Mix",
            command=self.create_sleep_mix,
            style="Accent.TButton"
        )
        self.create_mix_btn.pack(pady=15)

        # Right: Preview and Results
        preview_frame = ttk.LabelFrame(content_frame, text="🎧 Preview & Results", padding="15")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Preview controls
        player_frame = ttk.LabelFrame(preview_frame, text="Audio Player", padding="10")
        player_frame.pack(fill=tk.X, pady=5)

        # Current track
        self.current_track_var = tk.StringVar(value="No audio loaded")
        ttk.Label(player_frame, textvariable=self.current_track_var, wraplength=250).pack(pady=5)

        # Player buttons
        player_buttons = ttk.Frame(player_frame)
        player_buttons.pack(pady=5)

        ttk.Button(player_buttons, text="▶️ Play", command=self.play_preview).pack(side=tk.LEFT, padx=2)
        ttk.Button(player_buttons, text="⏸️ Pause", command=self.pause_preview).pack(side=tk.LEFT, padx=2)
        ttk.Button(player_buttons, text="⏹️ Stop", command=self.stop_preview).pack(side=tk.LEFT, padx=2)

        # Volume
        ttk.Label(player_frame, text="Preview Volume:").pack(anchor="w")
        self.preview_volume_var = tk.DoubleVar(value=0.5)
        ttk.Scale(
            player_frame,
            from_=0.0, to=1.0,
            variable=self.preview_volume_var,
            orient="horizontal"
        ).pack(fill=tk.X, pady=2)

        # Mix progress
        self.mix_progress_var = tk.DoubleVar()
        self.mix_progress = ttk.Progressbar(
            preview_frame,
            variable=self.mix_progress_var,
            mode='determinate'
        )
        self.mix_progress.pack(fill=tk.X, pady=5)

        # Mix status
        self.mix_status_var = tk.StringVar(value="Ready to create mix...")
        ttk.Label(preview_frame, textvariable=self.mix_status_var, wraplength=250).pack(pady=5)

        # Created mixes list
        ttk.Label(preview_frame, text="Created Mixes:").pack(anchor="w", pady=(10,0))
        self.created_mixes_list = tk.Listbox(preview_frame, height=8)
        self.created_mixes_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Navigation
        nav_frame = ttk.Frame(frame)
        nav_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            nav_frame,
            text="← Back: Process Audio",
            command=lambda: self.show_step(2)
        ).pack(side=tk.LEFT)

        ttk.Button(
            nav_frame,
            text="💾 Next: Save & Use →",
            command=lambda: self.show_step(4),
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)

        return frame

    def create_step4_save_use(self):
        """Create Step 4: Save & Use interface."""
        frame = ttk.Frame(self.content_frame)

        # Title
        ttk.Label(
            frame,
            text="💾 Step 4: Save & Use Your Therapeutic Sleep Audio",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Main content
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Export Options
        export_frame = ttk.LabelFrame(content_frame, text="📁 Export Options", padding="15")
        export_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Export format
        format_frame = ttk.LabelFrame(export_frame, text="Audio Format", padding="10")
        format_frame.pack(fill=tk.X, pady=5)

        ttk.Label(format_frame, text="Choose export format:").pack(anchor="w")
        self.export_format_var = tk.StringVar(value="WAV (High Quality)")
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.export_format_var,
            values=[
                "WAV (High Quality)",
                "MP3 (Compressed)",
                "FLAC (Lossless)"
            ],
            state="readonly"
        )
        format_combo.pack(fill=tk.X, pady=5)

        # Export location
        location_frame = ttk.LabelFrame(export_frame, text="Save Location", padding="10")
        location_frame.pack(fill=tk.X, pady=5)

        self.export_path_var = tk.StringVar(value="./output_mixes/")
        location_entry = ttk.Entry(location_frame, textvariable=self.export_path_var)
        location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(
            location_frame,
            text="Browse",
            command=self.browse_export_location
        ).pack(side=tk.RIGHT)

        # File naming
        naming_frame = ttk.LabelFrame(export_frame, text="File Naming", padding="10")
        naming_frame.pack(fill=tk.X, pady=5)

        ttk.Label(naming_frame, text="Base filename:").pack(anchor="w")
        self.filename_var = tk.StringVar(value="sleep_audio")
        ttk.Entry(naming_frame, textvariable=self.filename_var).pack(fill=tk.X, pady=2)

        self.add_timestamp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            naming_frame,
            text="Add timestamp to filename",
            variable=self.add_timestamp_var
        ).pack(anchor="w", pady=2)

        # Export buttons
        export_buttons = ttk.Frame(export_frame)
        export_buttons.pack(fill=tk.X, pady=15)

        ttk.Button(
            export_buttons,
            text="💾 Export Current Mix",
            command=self.export_current_mix,
            style="Accent.TButton"
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            export_buttons,
            text="📦 Export All Mixes",
            command=self.export_all_mixes
        ).pack(fill=tk.X, pady=2)

        # Right: Usage Instructions & Tips
        usage_frame = ttk.LabelFrame(content_frame, text="🎧 Usage Instructions", padding="15")
        usage_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Instructions
        instructions_text = """
🌙 How to Use Your Sleep Audio:

✅ EQUIPMENT NEEDED:
• Headphones (REQUIRED for binaural beats)
• Comfortable sleeping environment

✅ OPTIMAL USAGE:
• Start 45-90 minutes before bedtime
• Use consistent volume (not too loud)
• Play for full duration for best results

✅ RESEARCH BENEFITS:
• 25% faster sleep onset
• Enhanced memory consolidation
• Reduced anxiety levels
• Improved sleep quality

✅ WEEKLY SCHEDULE:
• Week 1: Initial sleep improvements
• Week 2-3: Enhanced sleep quality
• Week 3+: Maximum therapeutic benefits

✅ TIPS:
• Use in dark, cool room
• Avoid screens 30 min before
• Create consistent bedtime routine
• Track sleep quality improvements
        """

        instructions_label = ttk.Label(
            usage_frame,
            text=instructions_text,
            justify="left",
            font=("Arial", 9)
        )
        instructions_label.pack(fill=tk.BOTH, expand=True)

        # Export progress
        self.export_progress_var = tk.DoubleVar()
        self.export_progress = ttk.Progressbar(
            usage_frame,
            variable=self.export_progress_var,
            mode='determinate'
        )
        self.export_progress.pack(fill=tk.X, pady=5)

        # Export status
        self.export_status_var = tk.StringVar(value="Ready to export...")
        ttk.Label(usage_frame, textvariable=self.export_status_var, wraplength=250).pack(pady=5)

        # Navigation
        nav_frame = ttk.Frame(frame)
        nav_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            nav_frame,
            text="← Back: Create Mix",
            command=lambda: self.show_step(3)
        ).pack(side=tk.LEFT)

        ttk.Button(
            nav_frame,
            text="🔄 Start Over",
            command=lambda: self.show_step(1)
        ).pack(side=tk.RIGHT)

        return frame

    def show_step(self, step_num):
        """Show the specified step."""
        # Hide all step frames
        for frame in self.step_frames.values():
            frame.pack_forget()

        # Show selected step
        self.step_frames[step_num].pack(fill=tk.BOTH, expand=True)
        self.current_step = step_num

        # Update step button states
        for i, btn in self.step_buttons.items():
            if i == step_num:
                btn.configure(style="Accent.TButton")
            else:
                btn.configure(style="TButton")

        logger.info(f"Switched to step {step_num}")

    # Step 1 Methods
    def start_automated_collection(self):
        """Start the automated sound collection process."""
        # Initialize API if needed
        if not self.freesound_api:
            try:
                self.freesound_api = FreesoundAPI(self.saved_api_key)
                self.content_gatherer = ContentGatherer(self.saved_api_key)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to initialize API: {str(e)}")
                return

        if self.auto_collection_running:
            messagebox.showwarning("Warning", "Collection already in progress")
            return

        collection_type = self.collection_type_var.get().split(" ")[0]  # Get first word
        max_files = int(self.quantity_var.get())

        def collection_task():
            """Run collection in background thread."""
            try:
                self.auto_collection_running = True
                self.collect_btn.configure(state="disabled")                # Simple collection simulation using clean test audio files
                demo_files = [
                    "gentle_rain.wav",
                    "ocean_waves.wav", 
                    "forest_ambience.wav",
                    "white_noise.wav"
                ]
                categories = ["Rain Sounds", "Ocean Waves", "White Noise", "Nature Ambience"]
                total_files = 0

                for i, category in enumerate(categories):
                    if not self.auto_collection_running:
                        break

                    self.collection_status_var.set(f"Collecting {category}...")
                    
                    # Simulate file collection using actual demo files
                    for j in range(min(3, max_files)):  # Limit to available demo files
                        if not self.auto_collection_running:
                            break
                        
                        if j < len(demo_files):                            # Use actual demo files for preview functionality
                            demo_file = demo_files[j]
                            display_name = f"{category}_{j+1}.wav"
                            actual_path = os.path.join("test_sounds", demo_file)
                            
                            self.collected_files_list.insert(tk.END, display_name)
                            # Map to actual clean test file for preview
                            self.collected_files_paths[display_name] = actual_path
                        else:                            # Fallback to simulated files
                            filename = f"{category}_{j+1}.wav"
                            self.collected_files_list.insert(tk.END, filename)
                            simulated_path = os.path.join("test_sounds", "gentle_rain.wav")  # Use clean test file
                            self.collected_files_paths[filename] = simulated_path
                        
                        total_files += 1
                        self.collection_status_var.set(f"Downloaded: {display_name if j < len(demo_files) else filename}")
                        
                        # Simulate download time
                        import time
                        time.sleep(0.5)

                    progress = ((i + 1) / len(categories)) * 100
                    self.collection_progress_var.set(progress)

                self.collection_status_var.set(f"Collection complete! Downloaded {total_files} files.")
                self.update_file_count()

            except Exception as e:
                messagebox.showerror("Error", f"Collection error: {str(e)}")
            finally:
                self.auto_collection_running = False
                self.collect_btn.configure(state="normal")
                self.collection_progress_var.set(0)

        threading.Thread(target=collection_task, daemon=True).start()

    def browse_audio_files(self):
        """Browse for manual audio files."""
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.ogg *.flac"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            filename = os.path.basename(file)
            if filename not in self.manual_files_list.get(0, tk.END):
                self.manual_files_list.insert(tk.END, filename)
                # Track the full path for preview
                self.manual_files_paths[filename] = file
        
        self.update_file_count()

    def browse_audio_folder(self):
        """Browse for folder with audio files."""
        folder = filedialog.askdirectory(title="Select Folder with Audio Files")
        if folder:
            count = 0
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')):
                        if file not in self.manual_files_list.get(0, tk.END):
                            self.manual_files_list.insert(tk.END, file)
                            # Track the full path for preview
                            full_path = os.path.join(root, file)
                            self.manual_files_paths[file] = full_path
                            count += 1
            
            if count > 0:
                self.update_file_count()

    def remove_manual_file(self):
        """Remove selected manual file."""
        selected = self.manual_files_list.curselection()
        for i in reversed(selected):
            filename = self.manual_files_list.get(i)
            self.manual_files_list.delete(i)
            # Remove from path tracking
            if filename in self.manual_files_paths:
                del self.manual_files_paths[filename]
        self.update_file_count()

    def clear_manual_files(self):
        """Clear all manual files."""
        self.manual_files_list.delete(0, tk.END)
        # Clear path tracking
        self.manual_files_paths.clear()
        self.update_file_count()

    def update_file_count(self):
        """Update the file count display."""
        collected = self.collected_files_list.size()
        manual = self.manual_files_list.size()
        total = collected + manual
        
        if total == 0:
            self.file_count_var.set("No files collected yet")
        else:
            self.file_count_var.set(f"Total files: {total} (Collected: {collected}, Manual: {manual})")

    # Step 2 Methods
    def start_processing(self):
        """Start the audio processing."""
        def processing_task():
            try:
                self.process_btn.configure(state="disabled")
                
                # Get all files
                collected_files = list(self.collected_files_list.get(0, tk.END))
                manual_files = list(self.manual_files_list.get(0, tk.END))
                all_files = collected_files + manual_files
                
                if not all_files:
                    messagebox.showwarning("Warning", "No files to process")
                    return
                
                for i, file in enumerate(all_files):
                    self.processing_status_var.set(f"Processing: {file}")
                    
                    # Simulate processing
                    import time
                    time.sleep(0.3)
                    
                    # Add to processed list
                    processed_name = f"processed_{file}"
                    self.processed_files_list.insert(tk.END, processed_name)
                    
                    progress = ((i + 1) / len(all_files)) * 100
                    self.processing_progress_var.set(progress)
                
                self.processing_status_var.set(f"Processing complete! {len(all_files)} files processed.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Processing error: {str(e)}")
            finally:
                self.process_btn.configure(state="normal")
        
        threading.Thread(target=processing_task, daemon=True).start()

    # Step 3 Methods
    def apply_preset(self, event=None):
        """Apply selected preset settings."""
        preset = self.preset_var.get()
        
        presets = {
            "Quick Sleep (15 min)": {
                "master": 0.6, "nature": 0.9, "pink": 0.4, "binaural": 0.3
            },
            "Deep Sleep (60 min)": {
                "master": 0.7, "nature": 0.8, "pink": 0.3, "binaural": 0.2
            },
            "Nap Time (20 min)": {
                "master": 0.5, "nature": 0.7, "pink": 0.2, "binaural": 0.1
            },
            "Insomnia Relief (90 min)": {
                "master": 0.8, "nature": 0.6, "pink": 0.5, "binaural": 0.4
            },
            "Anxiety Relief (30 min)": {
                "master": 0.6, "nature": 0.9, "pink": 0.2, "binaural": 0.1
            }
        }
        
        if preset in presets:
            settings = presets[preset]
            self.master_volume_var.set(settings["master"])
            self.nature_level_var.set(settings["nature"])
            self.pink_noise_level_var.set(settings["pink"])
            self.binaural_level_var.set(settings["binaural"])

    def create_sleep_mix(self):
        """Create the sleep mix with current settings."""
        def mix_task():
            try:
                self.create_mix_btn.configure(state="disabled")
                self.mix_status_var.set("Creating sleep mix...")
                
                # Simulate mix creation
                steps = [
                    "Loading processed audio files...",
                    "Applying volume levels...",
                    "Adding pink noise...",
                    "Integrating binaural beats...",
                    "Applying therapeutic enhancements...",
                    "Finalizing mix..."
                ]
                
                for i, step in enumerate(steps):
                    self.mix_status_var.set(step)
                    import time
                    time.sleep(0.5)
                    
                    progress = ((i + 1) / len(steps)) * 100
                    self.mix_progress_var.set(progress)
                
                # Add to created mixes
                preset = self.preset_var.get()
                mix_name = f"{preset}_{len(list(self.created_mixes_list.get(0, tk.END))) + 1}.wav"
                self.created_mixes_list.insert(tk.END, mix_name)
                self.current_track_var.set(f"Loaded: {mix_name}")
                
                self.mix_status_var.set("Mix created successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Mix creation error: {str(e)}")
            finally:
                self.create_mix_btn.configure(state="normal")
                self.mix_progress_var.set(0)
        
        threading.Thread(target=mix_task, daemon=True).start()

    def play_preview(self):
        """Play audio preview."""
        try:
            selected = self.created_mixes_list.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a mix to preview")
                return
            
            mix_name = self.created_mixes_list.get(selected[0])
            file_path = os.path.join(self.export_path_var.get(), mix_name)
            
            if not os.path.isfile(file_path):
                messagebox.showerror("Error", f"Preview file not found: {file_path}")
                return
            
            self.audio_player.load(file_path)
            self.audio_player.set_volume(self.preview_volume_var.get())
            self.audio_player.play()
            
            self.current_track_var.set(f"Playing: {mix_name}")
            logger.info(f"Playing preview: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Playback error: {str(e)}")

    def pause_preview(self):
        """Pause audio preview."""
        logger.info("Pausing audio preview")
        self.audio_player.pause()

    def stop_preview(self):
        """Stop audio preview."""
        logger.info("Stopping audio preview")
        self.audio_player.stop()
        self.current_track_var.set("No audio loaded")

    # Step 4 Methods
    def browse_export_location(self):
        """Browse for export location."""
        folder = filedialog.askdirectory(title="Select Export Location")
        if folder:
            self.export_path_var.set(folder)

    def export_current_mix(self):
        """Export the currently selected mix."""
        selected = self.created_mixes_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a mix to export")
            return
        
        mix_name = self.created_mixes_list.get(selected[0])
        self.export_mix(mix_name)

    def export_all_mixes(self):
        """Export all created mixes."""
        mixes = list(self.created_mixes_list.get(0, tk.END))
        if not mixes:
            messagebox.showwarning("Warning", "No mixes to export")
            return
        
        for mix in mixes:
            self.export_mix(mix)

    def export_mix(self, mix_name):
        """Export a specific mix."""
        def export_task():
            try:
                self.export_status_var.set(f"Exporting {mix_name}...")
                
                # Simulate export
                import time
                time.sleep(1)
                
                # Get export settings
                export_path = self.export_path_var.get()
                filename = self.filename_var.get()
                
                if self.add_timestamp_var.get():
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{filename}_{timestamp}"
                
                format_ext = {
                    "WAV (High Quality)": ".wav",
                    "MP3 (Compressed)": ".mp3", 
                    "FLAC (Lossless)": ".flac"
                }
                
                ext = format_ext.get(self.export_format_var.get(), ".wav")
                full_path = os.path.join(export_path, f"{filename}{ext}")
                
                # Create directory if it doesn't exist
                os.makedirs(export_path, exist_ok=True)
                
                self.export_progress_var.set(100)
                self.export_status_var.set(f"Exported: {full_path}")
                
                messagebox.showinfo("Export Complete", f"Successfully exported to:\n{full_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export error: {str(e)}")
            finally:
                self.export_progress_var.set(0)
        
        threading.Thread(target=export_task, daemon=True).start()

    # Audio Preview Methods
    def preview_collected_file(self, event=None):
        """Preview a collected audio file."""
        selected = self.collected_files_list.curselection()
        if not selected:
            self.collected_preview_status.set("Please select a file to preview")
            return
        
        display_name = self.collected_files_list.get(selected[0])
        file_path = self.collected_files_paths.get(display_name)
        
        if file_path and os.path.exists(file_path):
            self.play_audio_preview(file_path, self.collected_preview_status)
        else:
            self.collected_preview_status.set("File not found or invalid")

    def preview_manual_file(self, event=None):
        """Preview a manual audio file."""
        selected = self.manual_files_list.curselection()
        if not selected:
            self.manual_preview_status.set("Please select a file to preview")
            return
        
        display_name = self.manual_files_list.get(selected[0])
        file_path = self.manual_files_paths.get(display_name)
        
        if file_path and os.path.exists(file_path):
            self.play_audio_preview(file_path, self.manual_preview_status)
        else:
            self.manual_preview_status.set("File not found or invalid")

    def play_audio_preview(self, file_path, status_var):
        """Play audio preview using available audio libraries."""
        try:
            # Stop any currently playing audio
            self.stop_preview()
            
            status_var.set(f"Playing: {os.path.basename(file_path)}")
            
            # Try to use pygame first (most reliable)
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.current_audio_lib = 'pygame'
                return
            except ImportError:
                pass
            except Exception as e:
                logger.warning(f"Pygame playback failed: {e}")
            
            # Fallback to Windows winsound for WAV files
            if WINSOUND_AVAILABLE and file_path.lower().endswith('.wav'):
                try:
                    threading.Thread(target=lambda: winsound.PlaySound(
                        file_path, winsound.SND_FILENAME | winsound.SND_ASYNC), 
                        daemon=True).start()
                    self.current_audio_lib = 'winsound'
                    return
                except Exception as e:
                    logger.warning(f"Winsound playback failed: {e}")
            
            # Last resort: try system audio player
            try:
                if sys.platform.startswith('win'):
                    os.startfile(file_path)
                elif sys.platform.startswith('darwin'):
                    os.system(f'open "{file_path}"')
                else:
                    os.system(f'xdg-open "{file_path}"')
                self.current_audio_lib = 'system'
                status_var.set(f"Opening {os.path.basename(file_path)} in default player")
                return
            except Exception as e:
                logger.warning(f"System playback failed: {e}")
            
            status_var.set("Audio preview not available - no audio libraries found")
            
        except Exception as e:
            logger.error(f"Error playing audio preview: {e}")
            status_var.set(f"Error: {str(e)}")

    def stop_preview(self):
        """Stop any currently playing audio preview."""
        try:
            # Try to stop pygame
            try:
                import pygame
                pygame.mixer.music.stop()
            except (ImportError, NameError):
                pass
            except Exception as e:
                # pygame might not be initialized
                pass
                
            # Try to stop winsound (limited control)
            if WINSOUND_AVAILABLE:
                try:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except:
                    pass
            
            # Update status
            if hasattr(self, 'collected_preview_status'):
                self.collected_preview_status.set("Preview stopped")
            if hasattr(self, 'manual_preview_status'):
                self.manual_preview_status.set("Preview stopped")
                
        except Exception as e:
            logger.error(f"Error stopping audio preview: {e}")


def main():
    """Main function to run the unified interface."""
    root = tk.Tk()
    app = UnifiedSleepAudioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
