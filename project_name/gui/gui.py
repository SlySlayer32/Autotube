import io
import logging
import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List

from PIL import Image, ImageTk

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.mix_creator import MixCreator
from project_name.core.processor import QueueHandler, SoundProcessor
from project_name.core.visualizer import Visualizer

# Import enhanced widgets
from .widgets import (
    WaveformDisplay, 
    AudioPlayer, 
    ProgressTracker, 
    AdvancedMixControls, 
    SessionManager
)

logger = logging.getLogger(__name__)


class AudioLibraryScreen:
    def __init__(self, parent):
        self.parent = parent
        self.library_frame = ttk.LabelFrame(parent, text="Audio Library", padding="5")
        self.library_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )

        # File location management
        ttk.Button(
            self.library_frame,
            text="Set Library Location",
            command=self._set_library_location,
        ).grid(row=0, column=0, pady=5)
        self.library_location_var = tk.StringVar(value="Not Set")
        ttk.Label(self.library_frame, textvariable=self.library_location_var).grid(
            row=0, column=1, pady=5
        )

        # File list
        self.file_list = tk.Listbox(self.library_frame, height=10)
        self.file_list.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Audio controls
        controls_frame = ttk.Frame(self.library_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(controls_frame, text="Play", command=self._play_audio).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(controls_frame, text="Pause", command=self._pause_audio).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(controls_frame, text="Stop", command=self._stop_audio).grid(
            row=0, column=2, padx=5
        )

        # Normalization and quality enhancement
        ttk.Button(
            self.library_frame, text="Normalize Files", command=self._normalize_files
        ).grid(row=3, column=0, pady=5)
        ttk.Button(
            self.library_frame, text="Enhance Quality", command=self._enhance_quality
        ).grid(row=3, column=1, pady=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(
            self.library_frame, variable=self.progress_var, mode="determinate"
        ).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

    def _set_library_location(self):
        location = filedialog.askdirectory(title="Select Library Location")
        if location:
            self.library_location_var.set(location)
            self._load_library_files(location)

    def _load_library_files(self, location):
        self.file_list.delete(0, tk.END)
        for file in os.listdir(location):
            if file.endswith((".wav", ".mp3")):
                self.file_list.insert(tk.END, file)

    def _play_audio(self):
        # Placeholder for play functionality
        pass

    def _pause_audio(self):
        # Placeholder for pause functionality
        pass

    def _stop_audio(self):
        # Placeholder for stop functionality
        pass

    def _normalize_files(self):
        # Placeholder for normalization functionality
        pass

    def _enhance_quality(self):
        # Placeholder for quality enhancement functionality
        pass


class SoundToolGUI:
    def __init__(self, root: tk.Tk):
        """Initialize the GUI."""
        self.root = root
        self.root.title("SonicSleep Pro")
        self.root.geometry("1200x800")        # Initialize components
        self.processor = SoundProcessor()
        self.visualizer = Visualizer()
        self.mix_creator = MixCreator()
        self.freesound_api = None  # Will be initialized when API key is provided

        # Initialize enhanced features
        self.current_audio_file = None
        self.current_audio_data = None
        self.session_data = {}

        # Set up logging queue
        self.log_queue = queue.Queue()
        queue_handler = QueueHandler(self.log_queue)
        logger.addHandler(queue_handler)

        # Create main UI elements
        self._create_menu_bar()
        self._create_toolbar()
        self._create_gui()  # This will create and pack self.main_container
        self._create_status_bar()

        self._setup_periodic_callbacks()

    def _create_menu_bar(self):
        """Create the main menu bar."""
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Files...", command=self._load_local_files)
        file_menu.add_command(
            label="Search Freesound...", command=self._search_freesound
        )
        file_menu.add_separator()
        file_menu.add_command(label="Settings...", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences...", command=self._open_settings)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Log", command=self._clear_log)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Refresh", command=self._refresh_view)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Toolbar", command=self._toggle_toolbar)
        view_menu.add_checkbutton(label="Show Status Bar", command=self._toggle_status_bar)
        menubar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_toolbar(self):
        """Create the toolbar."""
        self.toolbar = ttk.Frame(self.root, padding="2")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Load files button
        ttk.Button(
            self.toolbar,
            text="📁 Load Files",
            command=self._load_local_files,
        ).pack(side=tk.LEFT, padx=2)
        
        # Process audio button
        ttk.Button(
            self.toolbar,
            text="⚙️ Process Audio",
            command=self._process_audio,
        ).pack(side=tk.LEFT, padx=2)
        
        # Create mix button
        ttk.Button(
            self.toolbar,
            text="🎵 Create Mix",
            command=self._create_mix,
        ).pack(side=tk.LEFT, padx=2)
        
        # Generate video button
        ttk.Button(
            self.toolbar,
            text="🎬 Generate Video",
            command=self._generate_video,
        ).pack(side=tk.LEFT, padx=2)
        
        # Upload button
        ttk.Button(
            self.toolbar,
            text="☁️ Upload",
            command=self._upload_to_youtube,
        ).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Pipeline button
        ttk.Button(
            self.toolbar,
            text="🚀 Full Pipeline",
            command=self._run_full_pipeline,
        ).pack(side=tk.LEFT, padx=2)
        
        # Content planning button
        ttk.Button(
            self.toolbar,
            text="📅 Plan Content",
            command=self._open_content_planning,
        ).pack(side=tk.LEFT, padx=2)

    def _create_status_bar(self):
        """Create the status bar."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        # Using a simple Frame for the status bar container to avoid LabelFrame border
        status_bar_frame = ttk.Frame(self.root, relief=tk.SUNKEN, padding=2)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(status_bar_frame, textvariable=self.status_var, anchor=tk.W).pack(
            fill=tk.X, padx=5, pady=2
        )

    def _open_settings(self):
        """Placeholder for opening settings dialog."""
        messagebox.showinfo("Settings", "Settings dialog placeholder.")

    def _show_about(self):
        """Placeholder for showing about dialog."""
        messagebox.showinfo(
            "About SonicSleep Pro",
            "SonicSleep Pro - Ambient Audio Processing Tool\nVersion 0.1.0 (GUI WIP)",
        )

    def _create_gui(self):
        """Create the enhanced main GUI elements with advanced features."""
        # Create main notebook for tabbed interface
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create enhanced tabs
        self._create_enhanced_audio_tab()
        self._create_session_management_tab()
        self._create_advanced_mixing_tab()

    def _create_enhanced_audio_tab(self):
        """Create the main audio processing tab with enhanced features."""
        audio_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(audio_frame, text="🎵 Audio Processing")

        # Create main container with padding
        self.main_container = ttk.Frame(audio_frame, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Configure main_container's grid columns and rows to be responsive
        self.main_container.columnconfigure(0, weight=1)  # Left panel column
        self.main_container.columnconfigure(1, weight=2)  # Right panel column (wider)
        self.main_container.rowconfigure(0, weight=1)  # Main content row

        # Create left and right panels
        left_panel = ttk.Frame(self.main_container)
        right_panel = ttk.Frame(self.main_container)

        # Place panels in the main_container grid
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Configure left_panel's grid
        left_panel.rowconfigure(0, weight=1)  # Input section
        left_panel.rowconfigure(1, weight=1)  # Processing section
        left_panel.columnconfigure(0, weight=1)

        # Configure right_panel's grid
        right_panel.rowconfigure(0, weight=1)  # Enhanced visualization
        right_panel.rowconfigure(1, weight=0)  # Audio player
        right_panel.columnconfigure(0, weight=1)

        # Create sections with enhanced features
        self._create_enhanced_input_section(left_panel)
        self._create_enhanced_processing_section(left_panel)
        self._create_enhanced_visualization_section(right_panel)
        self._create_enhanced_player_section(right_panel)

    def _create_session_management_tab(self):
        """Create the session management tab."""
        session_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(session_frame, text="💾 Session Manager")

        # Add session manager widget
        self.session_manager = SessionManager(session_frame)
        self.session_manager.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_advanced_mixing_tab(self):
        """Create the advanced mixing tab."""
        mixing_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(mixing_frame, text="🎛️ Advanced Mixing")

        # Create advanced controls
        self.advanced_controls = AdvancedMixControls(mixing_frame)
        self.advanced_controls.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_enhanced_input_section(self, parent):
        """Create enhanced input section with better file management."""
        input_frame = ttk.LabelFrame(parent, text="📁 Enhanced Input", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # File operations with enhanced feedback
        file_ops_frame = ttk.Frame(input_frame)
        file_ops_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            file_ops_frame, text="Load Local Files", 
            command=self._enhanced_load_local_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            file_ops_frame, text="Load Recent", 
            command=self._load_recent_files
        ).pack(side=tk.LEFT, padx=5)

        # Freesound API section with status
        api_frame = ttk.LabelFrame(input_frame, text="🌐 Freesound API", padding="5")
        api_frame.pack(fill=tk.X, pady=5)

        api_controls = ttk.Frame(api_frame)
        api_controls.pack(fill=tk.X)

        ttk.Label(api_controls, text="API Key:").pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(api_controls, textvariable=self.api_key_var, show="*", width=20)
        api_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            api_controls, text="Search", command=self._enhanced_search_freesound
        ).pack(side=tk.LEFT, padx=5)

        # Enhanced file list with metadata
        list_frame = ttk.LabelFrame(input_frame, text="📋 Audio Files", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Create treeview for enhanced file display
        self.file_tree = ttk.Treeview(list_frame, columns=('Duration', 'Format', 'Size'), height=8)
        self.file_tree.heading('#0', text='Filename')
        self.file_tree.heading('Duration', text='Duration')
        self.file_tree.heading('Format', text='Format') 
        self.file_tree.heading('Size', text='Size')
        
        self.file_tree.column('#0', width=200)
        self.file_tree.column('Duration', width=80)
        self.file_tree.column('Format', width=60)
        self.file_tree.column('Size', width=80)

        # Scrollbar for file tree
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)

        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.file_tree.bind('<<TreeviewSelect>>', self._on_file_select)

    def _create_enhanced_processing_section(self, parent):
        """Create enhanced processing section with progress tracking."""
        process_frame = ttk.LabelFrame(parent, text="⚙️ Enhanced Processing", padding="10")
        process_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Processing controls
        controls_frame = ttk.Frame(process_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            controls_frame, text="🔄 Process Files", 
            command=self._enhanced_process_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            controls_frame, text="🧠 Therapeutic Process", 
            command=self._process_therapeutic
        ).pack(side=tk.LEFT, padx=5)

        # Enhanced progress tracker
        self.processing_progress = ProgressTracker(process_frame)
        self.processing_progress.pack(fill=tk.X, pady=10)

        # Processing options
        options_frame = ttk.LabelFrame(process_frame, text="Processing Options", padding="5")
        options_frame.pack(fill=tk.X, pady=5)

        # Checkboxes for processing options
        self.normalize_var = tk.BooleanVar(value=True)
        self.enhance_var = tk.BooleanVar(value=False)
        self.therapeutic_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(options_frame, text="Normalize Audio", 
                       variable=self.normalize_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Enhance Quality", 
                       variable=self.enhance_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Apply Therapeutic Processing", 
                       variable=self.therapeutic_var).pack(anchor=tk.W)

    def _create_enhanced_visualization_section(self, parent):
        """Create enhanced visualization section with waveform display."""
        viz_frame = ttk.LabelFrame(parent, text="📊 Audio Visualization", padding="5")
        viz_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Add waveform display
        self.waveform_display = WaveformDisplay(viz_frame, width=600, height=250)
        self.waveform_display.pack(fill=tk.BOTH, expand=True, pady=5)

        # Visualization controls
        controls_frame = ttk.Frame(viz_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        ttk.Button(controls_frame, text="Analyze", 
                  command=self._analyze_current_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Zoom Fit", 
                  command=self._zoom_fit_waveform).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Plot", 
                  command=self._export_waveform_plot).pack(side=tk.LEFT, padx=5)

    def _create_enhanced_player_section(self, parent):
        """Create enhanced audio player section."""
        player_frame = ttk.LabelFrame(parent, text="🎧 Audio Player", padding="5")
        player_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Add audio player
        self.audio_player = AudioPlayer(player_frame)
        self.audio_player.pack(fill=tk.X, pady=5)

    # Enhanced functionality methods
    def _enhanced_load_local_files(self):
        """Enhanced file loading with metadata extraction."""
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.ogg *.flac"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            self._load_files_with_metadata(files)

    def _load_files_with_metadata(self, files):
        """Load files and extract metadata for enhanced display."""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        for file_path in files:
            try:
                # Get file info (this is a simplified version - you can enhance with audio library)
                import os
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1]
                
                # Format file size
                if file_size > 1024*1024:
                    size_str = f"{file_size/(1024*1024):.1f} MB"
                else:
                    size_str = f"{file_size/1024:.1f} KB"
                
                # Insert into tree (duration would need audio analysis)
                self.file_tree.insert('', 'end', text=file_name, 
                                    values=('--:--', file_ext, size_str))
                
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")

    def _on_file_select(self, event):
        """Handle file selection in the tree."""
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            filename = item['text']
            # Update current audio file and visualize
            # This would need full implementation with actual file path tracking
            logger.info(f"Selected file: {filename}")

    def _enhanced_search_freesound(self):
        """Enhanced Freesound search with better UI feedback."""
        if not self.api_key_var.get():
            messagebox.showwarning("API Key Missing", "Please enter your Freesound API key.")
            return
        
        # This would show a search dialog - placeholder for now
        messagebox.showinfo("Search", "Enhanced Freesound search dialog would open here.")

    def _enhanced_process_files(self):
        """Enhanced file processing with progress tracking."""
        if not hasattr(self, 'file_tree') or not self.file_tree.get_children():
            messagebox.showwarning("No Files", "Please load some audio files first.")
            return
        
        # Start processing in background thread
        threading.Thread(target=self._process_files_background, daemon=True).start()

    def _process_files_background(self):
        """Background processing with progress updates."""
        try:
            # Update progress tracker
            self.processing_progress.start_progress("Processing audio files...")
            
            # Simulate processing steps
            steps = ["Loading files", "Analyzing audio", "Applying filters", "Saving results"]
            for i, step in enumerate(steps):
                self.processing_progress.update_progress((i+1)/len(steps)*100, step)
                # Simulate processing time
                import time
                time.sleep(1)
            
            self.processing_progress.complete_progress("Processing completed successfully!")
            
        except Exception as e:
            self.processing_progress.error_progress(f"Processing failed: {str(e)}")

    def _process_therapeutic(self):
        """Apply therapeutic audio processing."""
        messagebox.showinfo("Therapeutic Processing", 
                          "Therapeutic audio processing would be applied here.")

    def _analyze_current_audio(self):
        """Analyze currently selected audio and update visualization."""
        if hasattr(self, 'current_audio_data') and self.current_audio_data is not None:
            self.waveform_display.plot_waveform(self.current_audio_data)
        else:
            messagebox.showinfo("No Audio", "Please select an audio file first.")

    def _zoom_fit_waveform(self):
        """Fit waveform display to show entire audio."""
        if hasattr(self, 'waveform_display'):
            # This would implement zoom-to-fit functionality
            logger.info("Zooming waveform to fit")

    def _export_waveform_plot(self):
        """Export the current waveform plot."""
        if hasattr(self, 'waveform_display'):
            filename = filedialog.asksaveasfilename(
                title="Export Waveform Plot",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")]
            )
            if filename:
                # This would implement plot export functionality
                messagebox.showinfo("Export", f"Waveform plot would be saved to {filename}")

    def _load_recent_files(self):
        """Load recently used files."""
        # This would implement recent files functionality
        messagebox.showinfo("Recent Files", "Recent files dialog would open here.")

    def _load_local_files(self):
        """Proxy for legacy load command to use enhanced loader."""
        self._enhanced_load_local_files()

    def _search_freesound(self):
        """Proxy for legacy search command to use enhanced search."""
        self._enhanced_search_freesound()

    def _setup_periodic_callbacks(self):
        """Set up periodic callbacks for updating UI."""
        # Check processor status every second
        self.root.after(1000, self._update_processor_status)

        # Update system resources every 5 seconds
        self.root.after(5000, self._update_system_resources)

    def _update_processor_status(self):
        """Update the processor status in the UI."""
        # Update status message
        if hasattr(self, 'status_var'):
            # Check if processing is active
            if hasattr(self, 'processing_progress') and hasattr(self.processing_progress, 'is_active'):
                if self.processing_progress.is_active():
                    self.status_var.set("Processing audio...")
                else:
                    self.status_var.set("Ready")
            else:
                self.status_var.set("Ready")
        
        # Schedule next update
        self.root.after(1000, self._update_processor_status)

    def _update_system_resources(self):
        """Update system resource usage in the UI."""
        # This could be enhanced to show actual system resources
        # For now, just schedule the next update
        self.root.after(5000, self._update_system_resources)

    # Original methods that may still exist - keeping for compatibility
    def _load_local_files(self):
        """Load local audio files."""
        if hasattr(self, '_enhanced_load_local_files'):
            return self._enhanced_load_local_files()
        
        # Fallback to simple file loading
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.ogg *.flac"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            # Simple file loading
            if hasattr(self, 'file_list'):
                self.file_list.delete(0, tk.END)
                for file in files:
                    import os
                    self.file_list.insert(tk.END, os.path.basename(file))

    def _search_freesound(self):
        """Search Freesound API."""
        if hasattr(self, '_enhanced_search_freesound'):
            return self._enhanced_search_freesound()
        
        # Fallback
        messagebox.showinfo("Freesound", "Freesound search functionality.")

    def _process_files(self):
        """Process audio files."""
        if hasattr(self, '_enhanced_process_files'):
            return self._enhanced_process_files()
        
        # Fallback
        messagebox.showinfo("Processing", "File processing functionality.")

    def _create_mix(self):
        """Create audio mix."""
        messagebox.showinfo("Mix Creation", "Mix creation functionality.")

    def _create_log_section(self, parent):
        """Create log section for compatibility."""
        log_frame = ttk.LabelFrame(parent, text="Log", padding="5")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Simple log display
        self.log_text = tk.Text(log_frame, height=8, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Add some sample log entries
        self.log_text.insert(tk.END, "Enhanced GUI initialized successfully.\n")
        self.log_text.insert(tk.END, "Ready for audio processing.\n")
        self.log_text.config(state=tk.DISABLED)

    def _process_audio(self):
        """Process loaded audio files."""
        messagebox.showinfo(
            "Process Audio",
            "Audio processing will preprocess and analyze loaded files.\n\n"
            "This feature normalizes audio, categorizes clips, and prepares them for mixing."
        )

    def _generate_video(self):
        """Generate video from audio."""
        # Open a dialog to select audio file and options
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Video")
        dialog.geometry("500x300")

        ttk.Label(dialog, text="Generate Video from Audio", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        # Audio file selection
        file_frame = ttk.Frame(dialog)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(file_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        audio_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=audio_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            file_frame,
            text="Browse...",
            command=lambda: audio_var.set(
                filedialog.askopenfilename(
                    title="Select Audio File",
                    filetypes=[
                        ("Audio Files", "*.mp3 *.wav *.flac"),
                        ("All Files", "*.*"),
                    ],
                )
            ),
        ).pack(side=tk.LEFT, padx=2)

        # Options
        options_frame = ttk.LabelFrame(dialog, text="Options", padding="10")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        waveform_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, text="Use Waveform Visualization", variable=waveform_var
        ).pack(anchor=tk.W, pady=5)

        title_var = tk.StringVar()
        ttk.Label(options_frame, text="Video Title:").pack(anchor=tk.W, pady=2)
        ttk.Entry(options_frame, textvariable=title_var, width=40).pack(
            fill=tk.X, pady=2
        )

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def generate():
            if not audio_var.get():
                messagebox.showerror("Error", "Please select an audio file")
                return

            try:
                from project_name.core.video_generator import VideoGenerator

                gen = VideoGenerator()
                if waveform_var.get():
                    video_path = gen.generate_video_with_waveform(audio_var.get())
                else:
                    video_path = gen.generate_video_from_audio(
                        audio_var.get(), title_text=title_var.get() or None
                    )

                if video_path:
                    messagebox.showinfo("Success", f"Video created: {video_path}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to create video")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating video: {e}")

        ttk.Button(button_frame, text="Generate", command=generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def _upload_to_youtube(self):
        """Upload video to YouTube."""
        # Open upload dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Upload to YouTube")
        dialog.geometry("600x400")

        ttk.Label(dialog, text="Upload Video to YouTube", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        # Video file selection
        file_frame = ttk.Frame(dialog)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(file_frame, text="Video File:").pack(side=tk.LEFT, padx=5)
        video_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=video_var, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            file_frame,
            text="Browse...",
            command=lambda: video_var.set(
                filedialog.askopenfilename(
                    title="Select Video File",
                    filetypes=[("Video Files", "*.mp4 *.avi"), ("All Files", "*.*")],
                )
            ),
        ).pack(side=tk.LEFT, padx=2)

        # Metadata
        meta_frame = ttk.LabelFrame(dialog, text="Video Metadata", padding="10")
        meta_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(meta_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=2)
        title_var = tk.StringVar()
        ttk.Entry(meta_frame, textvariable=title_var, width=50).grid(
            row=0, column=1, pady=2, sticky=tk.EW
        )

        ttk.Label(meta_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        desc_text = tk.Text(meta_frame, height=5, width=50)
        desc_text.grid(row=1, column=1, pady=2, sticky=tk.EW)

        ttk.Label(meta_frame, text="Tags:").grid(row=2, column=0, sticky=tk.W, pady=2)
        tags_var = tk.StringVar()
        ttk.Entry(meta_frame, textvariable=tags_var, width=50).grid(
            row=2, column=1, pady=2, sticky=tk.EW
        )

        ttk.Label(meta_frame, text="Privacy:").grid(row=3, column=0, sticky=tk.W, pady=2)
        privacy_var = tk.StringVar(value="private")
        ttk.Combobox(
            meta_frame,
            textvariable=privacy_var,
            values=["public", "private", "unlisted"],
            width=15,
        ).grid(row=3, column=1, sticky=tk.W, pady=2)

        meta_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def upload():
            if not video_var.get():
                messagebox.showerror("Error", "Please select a video file")
                return
            if not title_var.get():
                messagebox.showerror("Error", "Please enter a video title")
                return

            try:
                from project_name.api.youtube_uploader import YouTubeUploader

                uploader = YouTubeUploader()
                description = desc_text.get(1.0, tk.END).strip()
                tags = [t.strip() for t in tags_var.get().split(",") if t.strip()]

                video_id = uploader.upload_video(
                    video_path=video_var.get(),
                    title=title_var.get(),
                    description=description,
                    tags=tags,
                    privacy_status=privacy_var.get(),
                )

                if video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    messagebox.showinfo(
                        "Success", f"Video uploaded successfully!\n\nVideo ID: {video_id}\nURL: {url}"
                    )
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to upload video")
            except Exception as e:
                messagebox.showerror("Error", f"Error uploading video: {e}")

        ttk.Button(button_frame, text="Upload", command=upload).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def _run_full_pipeline(self):
        """Run the complete pipeline."""
        # Open pipeline configuration dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Full Pipeline")
        dialog.geometry("600x500")

        ttk.Label(dialog, text="Full Pipeline Automation", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        # Configuration
        config_frame = ttk.LabelFrame(dialog, text="Configuration", padding="10")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sound type
        ttk.Label(config_frame, text="Sound Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        sound_var = tk.StringVar(value="Rain")
        ttk.Combobox(
            config_frame,
            textvariable=sound_var,
            values=["Rain", "Ocean", "Nature", "Forest", "White Noise"],
            width=15,
        ).grid(row=0, column=1, sticky=tk.W, pady=2)

        # Mix type
        ttk.Label(config_frame, text="Mix Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        mix_var = tk.StringVar(value="sleep")
        ttk.Combobox(
            config_frame,
            textvariable=mix_var,
            values=["sleep", "focus", "relax"],
            width=15,
        ).grid(row=1, column=1, sticky=tk.W, pady=2)

        # Duration
        ttk.Label(config_frame, text="Duration (min):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        duration_var = tk.StringVar(value="60")
        ttk.Entry(config_frame, textvariable=duration_var, width=15).grid(
            row=2, column=1, sticky=tk.W, pady=2
        )

        # Options
        waveform_var = tk.BooleanVar()
        ttk.Checkbutton(
            config_frame, text="Use Waveform Visualization", variable=waveform_var
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        upload_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, text="Upload to YouTube", variable=upload_var).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=2
        )

        # Privacy
        ttk.Label(config_frame, text="Privacy:").grid(row=5, column=0, sticky=tk.W, pady=2)
        privacy_var = tk.StringVar(value="private")
        ttk.Combobox(
            config_frame,
            textvariable=privacy_var,
            values=["public", "private", "unlisted"],
            width=15,
        ).grid(row=5, column=1, sticky=tk.W, pady=2)

        # Progress
        progress_frame = ttk.Frame(dialog)
        progress_frame.pack(fill=tk.X, padx=10, pady=10)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_frame, variable=progress_var, mode="determinate"
        )
        progress_bar.pack(fill=tk.X)

        status_var = tk.StringVar(value="Ready to start")
        ttk.Label(progress_frame, textvariable=status_var).pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def run_pipeline():
            try:
                duration = int(duration_var.get())
                if duration <= 0:
                    raise ValueError("Duration must be positive")

                from project_name.core.orchestrator import AutotubeOrchestrator

                orchestrator = AutotubeOrchestrator()

                status_var.set("Running pipeline...")
                progress_var.set(25)
                self.root.update()

                results = orchestrator.run_full_pipeline(
                    sound_type=sound_var.get(),
                    duration_minutes=duration,
                    mix_type=mix_var.get(),
                    privacy_status=privacy_var.get(),
                    use_waveform=waveform_var.get(),
                    upload=upload_var.get(),
                )

                progress_var.set(100)

                if results["success"]:
                    msg = "Pipeline completed successfully!\n\n"
                    if results["audio_path"]:
                        msg += f"Audio: {results['audio_path']}\n"
                    if results["video_path"]:
                        msg += f"Video: {results['video_path']}\n"
                    if results["video_id"]:
                        msg += f"YouTube ID: {results['video_id']}\n"
                        msg += f"URL: https://www.youtube.com/watch?v={results['video_id']}"

                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                else:
                    msg = "Pipeline failed:\n" + "\n".join(results.get("errors", []))
                    messagebox.showerror("Pipeline Failed", msg)
                    status_var.set("Pipeline failed")

            except Exception as e:
                messagebox.showerror("Error", f"Error running pipeline: {e}")
                status_var.set("Error")

        run_btn = ttk.Button(button_frame, text="Run Pipeline", command=run_pipeline)
        run_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def _open_content_planning(self):
        """Open content planning dialog."""
        # Open content planning dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Content Planning")
        dialog.geometry("800x600")

        ttk.Label(dialog, text="Content Planning", font=("Arial", 12, "bold")).pack(pady=10)

        # Controls
        controls_frame = ttk.Frame(dialog)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(controls_frame, text="Number of Videos:").pack(side=tk.LEFT, padx=5)
        num_videos_var = tk.StringVar(value="7")
        ttk.Spinbox(controls_frame, from_=1, to=30, textvariable=num_videos_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        # Plan display
        plan_frame = ttk.LabelFrame(dialog, text="Content Plan", padding="10")
        plan_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("num", "type", "purpose", "date", "time", "duration")
        tree = ttk.Treeview(plan_frame, columns=columns, show="headings")

        tree.heading("num", text="#")
        tree.heading("type", text="Sound Type")
        tree.heading("purpose", text="Purpose")
        tree.heading("date", text="Date")
        tree.heading("time", text="Time")
        tree.heading("duration", text="Duration")

        tree.column("num", width=40)
        tree.column("type", width=120)
        tree.column("purpose", width=80)
        tree.column("date", width=100)
        tree.column("time", width=80)
        tree.column("duration", width=80)

        scrollbar = ttk.Scrollbar(plan_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def generate_plan():
            try:
                num_videos = int(num_videos_var.get())
                from project_name.core.orchestrator import AutotubeOrchestrator

                orchestrator = AutotubeOrchestrator()
                plan = orchestrator.plan_content(num_videos=num_videos)

                # Clear tree
                for item in tree.get_children():
                    tree.delete(item)

                # Add items
                for item in plan:
                    tree.insert(
                        "",
                        tk.END,
                        values=(
                            item["video_number"],
                            item["sound_type"],
                            item["purpose"],
                            item["scheduled_date"],
                            item["optimal_time"],
                            f"{item['duration_hours']}h",
                        ),
                    )

                messagebox.showinfo("Success", f"Generated plan for {num_videos} videos")

            except Exception as e:
                messagebox.showerror("Error", f"Error generating plan: {e}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Generate Plan", command=generate_plan).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(
            side=tk.LEFT, padx=5
        )

    def _clear_log(self):
        """Clear the log display."""
        if hasattr(self, "log_text"):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)

    def _refresh_view(self):
        """Refresh the current view."""
        self.status_var.set("View refreshed")

    def _toggle_toolbar(self):
        """Toggle toolbar visibility."""
        if hasattr(self, "toolbar"):
            if self.toolbar.winfo_viewable():
                self.toolbar.pack_forget()
            else:
                self.toolbar.pack(side=tk.TOP, fill=tk.X, before=self.main_notebook)

    def _toggle_status_bar(self):
        """Toggle status bar visibility."""
        # Find status bar frame
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame) and widget.cget("relief") == tk.SUNKEN:
                if widget.winfo_viewable():
                    widget.pack_forget()
                else:
                    widget.pack(side=tk.BOTTOM, fill=tk.X)
                break
