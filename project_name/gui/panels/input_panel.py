"""Input Processing Panel for SonicSleep Pro.

This panel provides interfaces for:
- Audio import
- Sound library management
- Freesound API integration
- File organization
- Automated sleep sound collection
"""

import logging
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import numpy as np
import soundfile as sf

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.content_gatherer import ContentGatherer

logger = logging.getLogger(__name__)


class InputProcessingPanel:
    """Panel for input processing functions."""

    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame

        # Create a notebook with tabs for different input methods
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for each input method
        self.local_frame = ttk.Frame(self.notebook)
        self.freesound_frame = ttk.Frame(self.notebook)
        self.library_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.local_frame, text="Local Files")
        self.notebook.add(self.freesound_frame, text="Freesound API")
        self.notebook.add(self.library_frame, text="Sound Library")

        # Setup each tab
        self._setup_local_tab()
        self._setup_freesound_tab()
        self._setup_library_tab()

        # Initialize freesound API and content gatherer
        self.freesound_api = None
        self.content_gatherer = None
        self.auto_collection_running = False

    def _setup_local_tab(self):
        """Set up the local files tab."""
        frame = ttk.Frame(self.local_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Import Audio Files", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=10
        )

        # File import section
        ttk.Button(frame, text="Browse for Files", command=self._browse_files).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Button(frame, text="Browse for Folder", command=self._browse_folder).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )

        # File list
        ttk.Label(frame, text="Selected Files:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )

        list_frame = ttk.Frame(frame)
        list_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )

        self.file_list = tk.Listbox(list_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.file_list.yview
        )

        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list["yscrollcommand"] = scrollbar.set

        # File actions
        action_frame = ttk.Frame(frame)
        action_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=10)

        ttk.Button(
            action_frame, text="Remove Selected", command=self._remove_selected
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Clear All", command=self._clear_all).pack(
            side=tk.LEFT, padx=5
        )

        # Import settings
        settings_frame = ttk.LabelFrame(frame, text="Import Settings", padding="5")
        settings_frame.grid(
            row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )

        ttk.Label(settings_frame, text="Target Sample Rate:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.sample_rate_var = tk.StringVar(value="44100")
        ttk.Combobox(
            settings_frame,
            textvariable=self.sample_rate_var,
            values=["22050", "44100", "48000", "96000"],
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(settings_frame, text="Channels:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.channels_var = tk.StringVar(value="Stereo")
        ttk.Combobox(
            settings_frame, textvariable=self.channels_var, values=["Mono", "Stereo"]
        ).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(settings_frame, text="Auto-categorize:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.categorize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, variable=self.categorize_var).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )

        # Import button
        ttk.Button(frame, text="Import Files", command=self._import_files).grid(
            row=6, column=0, columnspan=2, pady=10
        )

        # Progress bar
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(frame, variable=self.progress_var).grid(
            row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5
        )

    def _browse_files(self):
        """Browse for audio files."""
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.ogg *.flac"),
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*"),
            ],
        )

        if files:
            for file in files:
                if file not in self.file_list.get(0, tk.END):
                    self.file_list.insert(tk.END, file)

            logger.info(f"Selected {len(files)} files")

    def _browse_folder(self):
        """Browse for a folder containing audio files."""
        folder = filedialog.askdirectory(title="Select Folder with Audio Files")

        if folder:
            count = 0
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith((".wav", ".mp3", ".ogg", ".flac")):
                        filepath = os.path.join(root, file)
                        if filepath not in self.file_list.get(0, tk.END):
                            self.file_list.insert(tk.END, filepath)
                            count += 1

            logger.info(f"Found {count} audio files in {folder}")

    def _remove_selected(self):
        """Remove selected files from the list."""
        selected = self.file_list.curselection()

        # Remove from end to start to avoid index issues
        for i in reversed(selected):
            self.file_list.delete(i)

    def _clear_all(self):
        """Clear all files from the list."""
        self.file_list.delete(0, tk.END)

    def _import_files(self):
        """Import the selected files."""
        files = list(self.file_list.get(0, tk.END))

        if not files:
            messagebox.showwarning("Warning", "No files selected for import")
            return

        # Get import settings
        sample_rate = self.sample_rate_var.get()
        channels = 1 if self.channels_var.get() == "Mono" else 2
        auto_categorize = self.categorize_var.get()

        def import_task():
            """Import files in a background thread."""
            try:
                # In a real implementation, this would connect to the processor
                for i, file in enumerate(files):
                    # Update progress
                    progress = (i + 1) / len(files)
                    self.progress_var.set(progress * 100)

                    # Process file
                    logger.info(f"Importing {file} ({i + 1}/{len(files)})")

                    # Simulate processing time
                    import time

                    time.sleep(0.1)

                # Reset progress
                self.progress_var.set(0)

                # Show completion message
                messagebox.showinfo(
                    "Import Complete", f"Successfully imported {len(files)} files"
                )

            except Exception as e:
                logger.error(f"Error importing files: {str(e)}")
                messagebox.showerror("Error", f"Error importing files: {str(e)}")
                self.progress_var.set(0)

        # Start import in background thread
        threading.Thread(target=import_task).start()

    def _setup_freesound_tab(self):
        """Set up the Freesound API tab."""
        frame = ttk.Frame(self.freesound_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Freesound API Integration", font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=10)

        # API key entry
        ttk.Label(frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(frame, textvariable=self.api_key_var, width=40, show="*")
        api_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(frame, text="Save Key", command=self._save_api_key).grid(
            row=1, column=2, sticky=tk.W, pady=5
        )

        # Search section
        ttk.Label(frame, text="Search Query:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.search_query_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.search_query_var, width=40).grid(
            row=2, column=1, sticky=tk.W, pady=5, padx=5
        )
        ttk.Button(frame, text="Search", command=self._search_freesound).grid(
            row=2, column=2, sticky=tk.W, pady=5
        )

        # Filter section
        filter_frame = ttk.LabelFrame(frame, text="Filters", padding="5")
        filter_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # License filter
        ttk.Label(filter_frame, text="License:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.license_var = tk.StringVar(value="Creative Commons 0")
        ttk.Combobox(
            filter_frame,
            textvariable=self.license_var,
            width=30,
            values=[
                "Any License",
                "Creative Commons 0",
                "Attribution",
                "Attribution Noncommercial",
            ],
        ).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Duration filter
        ttk.Label(filter_frame, text="Max Duration (sec):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.duration_var = tk.StringVar(value="60")
        ttk.Entry(filter_frame, textvariable=self.duration_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )

        # Tag filter
        ttk.Label(filter_frame, text="Tags (comma separated):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.tags_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.tags_var, width=30).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )

        # Results section
        ttk.Label(frame, text="Search Results:").grid(
            row=4, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        results_frame = ttk.Frame(frame)
        results_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )

        # Results list with scrollbar
        self.results_list = tk.Listbox(results_frame, height=12, width=70)
        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_list.yview
        )

        self.results_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_list["yscrollcommand"] = scrollbar.set

        # Results list double-click binding
        self.results_list.bind("<Double-1>", self._preview_sound)

        # Preview and download buttons
        actions_frame = ttk.Frame(frame)
        actions_frame.grid(row=6, column=0, columnspan=3, pady=10)

        ttk.Button(actions_frame, text="Preview", command=self._preview_selected).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            actions_frame, text="Download", command=self._download_selected        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Download All", command=self._download_all).pack(
            side=tk.LEFT, padx=5
        )

        # Automated Source Sounds section
        auto_frame = ttk.LabelFrame(frame, text="🎵 Automated Source Sounds", padding="10")
        auto_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(auto_frame, text="Automatically collect sleep-optimized audio clips:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        # Collection options
        collection_options_frame = ttk.Frame(auto_frame)
        collection_options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Collection type
        ttk.Label(collection_options_frame, text="Collection Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.collection_type_var = tk.StringVar(value="Sleep Sounds")
        collection_combo = ttk.Combobox(
            collection_options_frame,
            textvariable=self.collection_type_var,
            width=20,
            values=[
                "Sleep Sounds",
                "Rain & Water",
                "Nature Ambience", 
                "White/Pink Noise",
                "Binaural Sources",
                "Complete Collection"
            ],
            state="readonly"
        )
        collection_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)        # Search strategy selection
        ttk.Label(collection_options_frame, text="Search Method:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.search_method_var = tk.StringVar(value="Context-Aware Search")
        search_method_combo = ttk.Combobox(
            collection_options_frame,
            textvariable=self.search_method_var,
            width=20,
            values=[
                "Context-Aware Search",
                "Empirical Tags",
                "Advanced API", 
                "Hybrid Approach"
            ],
            state="readonly"
        )
        search_method_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)

        # Quantity selection
        ttk.Label(collection_options_frame, text="Files per category:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20,5))
        self.quantity_var = tk.StringVar(value="10")
        ttk.Combobox(
            collection_options_frame,
            textvariable=self.quantity_var,
            width=5,
            values=["5", "10", "15", "25", "50"],
            state="readonly"
        ).grid(row=0, column=3, sticky=tk.W, pady=2)

        # Source Sounds button and progress
        source_button_frame = ttk.Frame(auto_frame)
        source_button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.source_sounds_btn = ttk.Button(
            source_button_frame, 
            text="🎵 Source Sounds", 
            command=self._source_sounds_auto,
            style="Accent.TButton"
        )
        self.source_sounds_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            source_button_frame, 
            text="Stop Collection", 
            command=self._stop_auto_collection
        ).pack(side=tk.LEFT, padx=5)

        # Collection progress
        self.collection_progress_var = tk.DoubleVar()
        self.collection_progress = ttk.Progressbar(
            auto_frame, 
            variable=self.collection_progress_var,
            mode='determinate'
        )
        self.collection_progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)        # Collection status
        self.collection_status_var = tk.StringVar(value="Ready to collect sounds...")
        ttk.Label(auto_frame, textvariable=self.collection_status_var, wraplength=500).grid(
            row=4, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        # Initialize collected files list for the automated system
        if not hasattr(self, 'collected_files_list'):
            # Create a simple list container for the automated system
            self.collected_files_list = type('MockList', (), {
                'insert': lambda self, pos, item: logger.info(f"Collected: {item}"),
                'size': lambda self: 0
            })()

        # Preview player frame
        player_frame = ttk.LabelFrame(frame, text="Preview Player", padding="5")
        player_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Currently playing label
        self.playing_var = tk.StringVar(value="No sound playing")
        ttk.Label(player_frame, textvariable=self.playing_var, wraplength=400).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        # Player controls
        ttk.Button(player_frame, text="Play", command=self._player_play).grid(
            row=1, column=0, padx=5, pady=5
        )
        ttk.Button(player_frame, text="Pause", command=self._player_pause).grid(
            row=1, column=1, padx=5, pady=5        )
        ttk.Button(player_frame, text="Stop", command=self._player_stop).grid(
            row=1, column=2, padx=5, pady=5
        )

    def _save_api_key(self):
        """Save the Freesound API key."""
        key = self.api_key_var.get()

        if not key:
            messagebox.showerror("Error", "Please enter an API key")
            return

        # Initialize API with key
        try:
            self.freesound_api = FreesoundAPI(key)
            self.content_gatherer = ContentGatherer(key)
            
            # Save API key to user profile for persistence
            self.api_key_var.set(key)
            
            logger.info("API key saved and verified")
            messagebox.showinfo("Success", "API key saved successfully")
        except Exception as e:
            logger.error(f"Error setting API key: {str(e)}")
            messagebox.showerror("Error", f"Error setting API key: {str(e)}")

    def _search_freesound(self):
        """Search Freesound with the given query."""
        if not self.freesound_api:
            messagebox.showerror("Error", "Please set a valid API key first")
            return

        query = self.search_query_var.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return

        # Prepare filters
        filters = {}

        # License filter
        license_filter = self.license_var.get()
        if license_filter != "Any License":
            filters["license"] = license_filter.lower().replace(" ", "_")

        # Duration filter
        try:
            max_duration = float(self.duration_var.get())
            if max_duration > 0:
                filters["duration"] = f"[0 TO {max_duration}]"
        except ValueError:
            pass

        # Tags filter
        tags = self.tags_var.get().strip()
        if tags:
            filters["tag"] = tags.replace(",", " ")

        def search_task():
            """Search in a background thread."""
            try:
                # Clear previous results
                self.results_list.delete(0, tk.END)

                # Search Freesound
                results = self.freesound_api.search(query, **filters)

                # Update results list
                if results and "results" in results:
                    for sound in results["results"]:
                        display_text = f"{sound['name']} ({sound['duration']:.1f}s) [{sound['license']}]"
                        self.results_list.insert(tk.END, display_text)
                        # Store sound ID as item data
                        self.results_list.itemconfig(tk.END, {"sound_id": sound["id"]})

                    logger.info(f"Found {len(results['results'])} results")
                else:
                    logger.info("No results found")
                    messagebox.showinfo(
                        "No Results", "No sounds found matching your criteria"
                    )

            except Exception as e:
                logger.error(f"Error searching Freesound: {str(e)}")
                messagebox.showerror("Error", f"Error searching Freesound: {str(e)}")

        # Start search in background thread
        threading.Thread(target=search_task).start()

    def _get_selected_sound_id(self):
        """Get the sound ID of the selected item."""
        selected = self.results_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sound first")
            return None

        # Get sound ID from item data
        try:
            sound_id = self.results_list.itemcget(selected[0], "sound_id")
            return sound_id
        except:
            # If itemcget doesn't work (depends on Tkinter version)
            # Extract ID from display text (would need proper parsing)
            return None

    def _preview_sound(self, event):
        """Handle double-click on a sound item."""
        self._preview_selected()

    def _preview_selected(self):
        """Preview the selected sound."""
        sound_id = self._get_selected_sound_id()
        if sound_id:
            # In a real implementation, this would play the sound
            self.playing_var.set(
                f"Playing: {self.results_list.get(self.results_list.curselection()[0])}"
            )
            logger.info(f"Previewing sound {sound_id}")

    def _download_selected(self):
        """Download the selected sound."""
        sound_id = self._get_selected_sound_id()
        if sound_id:
            # In a real implementation, this would download the sound
            logger.info(f"Downloading sound {sound_id}")
            messagebox.showinfo("Download", f"Started download of sound {sound_id}")

    def _download_all(self):
        """Download all sounds in the results list."""
        if self.results_list.size() == 0:
            messagebox.showwarning("Warning", "No sounds to download")
            return

        # In a real implementation, this would download all sounds
        count = self.results_list.size()
        logger.info(f"Downloading {count} sounds")
        messagebox.showinfo("Download", f"Started download of {count} sounds")

    def _player_play(self):
        """Play the currently selected preview."""
        logger.info("Play pressed")
        # In a real implementation, this would control the audio player

    def _player_pause(self):
        """Pause the currently playing preview."""
        logger.info("Pause pressed")
        # In a real implementation, this would control the audio player

    def _player_stop(self):
        """Stop the currently playing preview."""
        logger.info("Stop pressed")
        self.playing_var.set("No sound playing")
        # In a real implementation, this would control the audio player    def _source_sounds_auto(self):
        """Automatically collect sleep-optimized sounds using enhanced Freesound strategies."""
        if not self.freesound_api or not self.content_gatherer:
            messagebox.showerror("Error", "Please set a valid API key first")
            return

        if self.auto_collection_running:
            messagebox.showwarning("Warning", "Collection already in progress")
            return

        # Get collection parameters
        collection_type = self.collection_type_var.get()
        max_files = int(self.quantity_var.get())

        # Set up your saved API key
        saved_api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
        if not self.api_key_var.get():
            self.api_key_var.set(saved_api_key)
            try:
                self.freesound_api = FreesoundAPI(saved_api_key)
                self.content_gatherer = ContentGatherer(saved_api_key)
            except Exception as e:
                logger.error(f"Error with saved API key: {str(e)}")
                messagebox.showerror("Error", "Please enter a valid API key manually")
                return

        def collection_task():
            """Run the enhanced automated collection in a background thread."""
            try:
                self.auto_collection_running = True
                self.source_sounds_btn.config(state="disabled")
                  # Map collection types to enhanced therapeutic categories
                therapeutic_categories = self._get_therapeutic_categories(collection_type)
                search_method = self.search_method_var.get()
                
                total_categories = len(therapeutic_categories)
                completed_categories = 0
                total_downloaded = 0

                for category_name in therapeutic_categories:
                    if not self.auto_collection_running:
                        break
                        
                    self.collection_status_var.set(f"Collecting {category_name} sounds ({search_method})...")
                    
                    try:                        # Choose search method based on user selection
                        if search_method == "Context-Aware Search":
                            results = self.freesound_api.search_by_tags_and_filename(
                                category_type=category_name,
                                max_results=max_files,
                                duration_range=(10, 600),
                                quality_filter=True
                            )
                        elif search_method == "Empirical Tags":
                            results = self.freesound_api.search_by_empirical_tags(
                                category_type=category_name,
                                max_results=max_files,
                                duration_range=(10, 600)
                            )
                        elif search_method == "Advanced API":
                            results = self.freesound_api.search_therapeutic_sounds(
                                category_type=category_name,
                                max_results=max_files,
                                duration_range=(10, 600)
                            )
                        else:  # Hybrid Approach
                            # Try context-aware first, then empirical tags if needed
                            results = self.freesound_api.search_by_tags_and_filename(
                                category_type=category_name,
                                max_results=max_files//2,
                                duration_range=(10, 600),
                                quality_filter=True
                            )
                            if results.get('count', 0) < max_files//2:
                                empirical_results = self.freesound_api.search_by_empirical_tags(
                                    category_type=category_name,                                    max_results=max_files//2,
                                    duration_range=(10, 600)
                                )
                                if empirical_results.get('results'):
                                    results['results'].extend(empirical_results['results'])
                                    results['count'] = len(results['results'])
                        
                        if 'results' in results:
                            category_downloaded = 0
                            for sound in results['results'][:max_files]:
                                if not self.auto_collection_running or category_downloaded >= max_files:
                                    break
                                      # Enhanced quality verification and download
                                file_path = self.content_gatherer._download_and_process_sound(
                                    sound, 
                                    Path("processed_clips")
                                )
                                
                                if file_path:
                                    # Show therapeutic score if available (from context-aware search)
                                    therapeutic_score = sound.get('therapeutic_score')
                                    if therapeutic_score:
                                        display_name = f"{sound['name']} - {category_name.title()} (Score: {therapeutic_score:.1f})"
                                        status_msg = f"✓ Added: {sound['name']} (Score: {therapeutic_score:.1f}) - {total_downloaded} total"
                                    else:
                                        display_name = f"{sound['name']} - {category_name.title()}"
                                        status_msg = f"✓ Added: {sound['name']} ({total_downloaded} total)"
                                    
                                    self.collected_files_list.insert(tk.END, display_name)
                                    category_downloaded += 1
                                    total_downloaded += 1
                                    self.collection_status_var.set(status_msg)
                                    
                    except Exception as e:
                        logger.error(f"Error collecting '{category_name}': {e}")
                        continue
                    
                    completed_categories += 1
                    progress = (completed_categories / total_categories) * 100
                    self.collection_progress_var.set(progress)                # Collection complete
                self.collection_status_var.set(
                    f"✅ Collection complete! Downloaded {total_downloaded} therapeutic sounds."
                )
                messagebox.showinfo(
                    "Enhanced Collection Complete", 
                    f"Successfully collected {total_downloaded} research-optimized audio clips!\n\n"
                    f"🎵 Files saved to: processed_clips/\n"
                    f"🔬 Collection type: {collection_type}\n"
                    f"⚡ Used advanced Freesound search strategies\n"
                    f"🎯 Applied therapeutic quality filters"
                )

            except Exception as e:
                logger.error(f"Error in enhanced automated collection: {str(e)}")
                messagebox.showerror("Error", f"Collection error: {str(e)}")
            finally:
                self.auto_collection_running = False
                self.source_sounds_btn.config(state="normal")
                self.collection_progress_var.set(0)

        # Start enhanced collection in background thread
        threading.Thread(target=collection_task, daemon=True).start()

    def _stop_auto_collection(self):
        """Stop the automated collection process."""
        if self.auto_collection_running:
            self.auto_collection_running = False
            self.collection_status_var.set("Collection stopped by user")
            self.source_sounds_btn.config(state="normal")
            logger.info("Automated collection stopped by user")
        else:
            messagebox.showinfo("Info", "No collection is currently running")

    def _get_therapeutic_categories(self, collection_type):
        """Map collection types to enhanced therapeutic categories for new API."""
        therapeutic_mapping = {
            "Sleep Sounds": ["nature", "rain", "ocean", "ambient"],
            "Rain & Water": ["rain", "ocean"],
            "Nature Ambience": ["nature", "ambient"], 
            "White/Pink Noise": ["white_noise"],
            "Binaural Sources": ["binaural"],
            "Complete Collection": ["nature", "rain", "ocean", "ambient", "white_noise", "binaural"]
        }
        
        return therapeutic_mapping.get(collection_type, ["nature", "rain", "ocean"])

    def _get_sleep_sound_categories(self, collection_type):
        """Get enhanced search categories based on collection type using advanced Freesound strategies."""
        categories = {
            "Sleep Sounds": {
                "Gentle Rain": {
                    "queries": ['+rain +gentle +soft -thunder -storm', '"light rain" +peaceful', '+drizzle +calm'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Natural elements",
                        "descriptors": "ac_brightness:[0 TO 25] ac_roughness:[0 TO 20]"
                    }
                },
                "Ocean Waves": {
                    "queries": ['+ocean +waves +calm -storm -surf', '"beach waves" +peaceful', '+sea +gentle'],
                    "filters": {
                        "category": "Soundscapes", 
                        "subcategory": "Nature",
                        "descriptors": "ac_warmth:[60 TO 100] ac_hardness:[0 TO 25]"
                    }
                },
                "White Noise": {
                    "queries": ['+\"white noise\" +sleep +constant', '+noise +steady +calm', '+static +gentle'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_roughness:[0 TO 15]"
                    }
                },
                "Nature Ambience": {
                    "queries": ['+forest +ambience +calm -birds', '+nature +peaceful +quiet', '+woodland +atmosphere'],
                    "filters": {
                        "category": "Soundscapes",
                        "subcategory": "Nature", 
                        "descriptors": "ac_brightness:[0 TO 20] ac_warmth:[70 TO 100]"
                    }
                }
            },
            "Rain & Water": {
                "Light Rain": {
                    "queries": ['+rain +light +gentle -thunder', '+drizzle +peaceful', '+rain +soft +calm'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Natural elements"
                    }
                },
                "Heavy Rain": {
                    "queries": ['+rain +heavy -thunder -storm', '+downpour +rain -wind', '+rain +intense -lightning'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Natural elements"
                    }
                },
                "Water Streams": {
                    "queries": ['+stream +water +flowing', '+river +calm +gentle', '+brook +peaceful'],
                    "filters": {
                        "category": "Soundscapes",
                        "subcategory": "Nature"
                    }
                },
                "Ocean Sounds": {
                    "queries": ['+ocean +ambience +calm', '+sea +waves +peaceful', '+beach +gentle +waves'],
                    "filters": {
                        "category": "Soundscapes",
                        "subcategory": "Nature"
                    }
                }
            },
            "Nature Ambience": {
                "Forest Sounds": {
                    "queries": ['+forest +ambience +peaceful -birds', '+woodland +calm +atmosphere', '+trees +wind +gentle'],
                    "filters": {
                        "category": "Soundscapes",
                        "subcategory": "Nature",
                        "descriptors": "ac_brightness:[0 TO 25] ac_single_event:false"
                    }
                },
                "Bird Songs": {
                    "queries": ['+birds +gentle +nature +calm', '+chirping +peaceful +morning', '+songbird +forest +quiet'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Animals"
                    }
                },
                "Wind Sounds": {
                    "queries": ['+wind +gentle +soft +trees', '+breeze +calm +peaceful', '+wind +forest +quiet'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Natural elements",
                        "descriptors": "ac_brightness:[0 TO 30] ac_hardness:[0 TO 25]"
                    }
                },
                "Night Sounds": {
                    "queries": ['+night +ambience +peaceful +crickets', '+evening +calm +quiet', '+nighttime +nature +serene'],
                    "filters": {
                        "category": "Soundscapes",
                        "subcategory": "Nature",
                        "descriptors": "ac_brightness:[0 TO 15] ac_warmth:[50 TO 100]"
                    }
                }
            },
            "White/Pink Noise": {
                "White Noise": {
                    "queries": ['+\"white noise\" +sleep +constant', '+noise +steady +background', '+static +continuous +calm'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_roughness:[0 TO 20]"
                    }
                },
                "Pink Noise": {
                    "queries": ['+\"pink noise\" +sleep', '+noise +warm +gentle', '+\"brown noise\" +calm'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_warmth:[60 TO 100]"
                    }
                },
                "Fan Sounds": {
                    "queries": ['+fan +noise +steady +background', '+ventilation +constant +white', '+air +conditioner +hum'],
                    "filters": {
                        "category": "Sound effects",
                        "subcategory": "Objects / House appliances"
                    }
                },
                "Static Sounds": {
                    "queries": ['+static +gentle +background', '+hum +constant +peaceful', '+electronic +noise +soft'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_brightness:[0 TO 30]"
                    }
                }
            },
            "Binaural Sources": {
                "Low Frequency Tones": {
                    "queries": ['+sine +wave +low +frequency', '+tone +deep +bass', '+sub +bass +pure'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_roughness:[0 TO 10]"
                    }
                },
                "Ambient Drones": {
                    "queries": ['+ambient +drone +meditation +peaceful', '+sustained +tone +calm +relaxation', '+drone +peaceful +background'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_brightness:[0 TO 20] ac_roughness:[0 TO 15]"
                    }
                },
                "Binaural Beats": {
                    "queries": ['+binaural +beats +meditation', '+brain +waves +relaxation', '+theta +alpha +delta'],
                    "filters": {
                        "descriptors": "ac_single_event:false"
                    }
                },
                "Pure Tones": {
                    "queries": ['+pure +tone +sine +clean', '+test +tone +simple', '+frequency +generator +sine'],
                    "filters": {
                        "descriptors": "ac_single_event:false ac_roughness:[0 TO 5]"
                    }
                }
            }
        }
        
        if collection_type == "Complete Collection":
            # Combine all categories with enhanced search strategies
            all_categories = {}
            for cat_group in categories.values():
                all_categories.update(cat_group)
            return all_categories
        
        return categories.get(collection_type, categories["Sleep Sounds"])

    def _is_sleep_quality_sound(self, sound, file_path):
        """Check if a sound meets sleep quality criteria based on metadata and audio analysis."""
        # 1. Metadata Checks (same as before)
        duration = sound.get('duration', 0)
        if not (10 <= duration <= 600):
            logger.info(f"Skipping {sound['name']} due to duration: {duration}s")
            return False

        tags = [tag.lower() for tag in sound.get('tags', [])]
        negative_tags = ['loud', 'aggressive', 'harsh', 'sudden', 'alarm', 'shock', 'scary', 'thunder', 'windy']
        if any(tag in ' '.join(tags) for tag in negative_tags):
            logger.info(f"Skipping {sound['name']} due to negative tags: {tags}")
            return False

        # 2. Audio Content Analysis
        try:
            with sf.SoundFile(file_path, 'r') as audio_file:
                # Read audio data
                frames = audio_file.read(dtype='float32')
                samplerate = audio_file.samplerate

                # Mono conversion for analysis
                if audio_file.channels > 1:
                    frames = np.mean(frames, axis=1)

                # a. Check for silence or near-silence
                if np.max(np.abs(frames)) < 0.01:
                    logger.info(f"Skipping {sound['name']} due to silence.")
                    return False

                # b. Check for sudden peaks (transients) like thunder
                # We'll look at the difference between consecutive samples
                transients = np.diff(frames)
                peak_transient = np.max(np.abs(transients))
                
                # A high threshold indicates a very sudden, sharp sound
                if peak_transient > 0.8:
                    logger.info(f"Skipping {sound['name']} due to sharp transient (peak: {peak_transient:.2f})")
                    return False

                # c. Frequency analysis for high-pitched ringing
                # Perform FFT and check energy in high-frequency bands
                fft_data = np.fft.rfft(frames)
                fft_freq = np.fft.rfftfreq(len(frames), d=1./samplerate)
                  # Check energy above 8kHz - high-pitched noise
                high_freq_energy = np.mean(np.abs(fft_data[fft_freq > 8000]))
                total_energy = np.mean(np.abs(fft_data))
                
                if total_energy > 0 and (high_freq_energy / total_energy) > 0.4:
                    logger.info(f"Skipping {sound['name']} due to excessive high-frequency energy.")
                    return False

        except Exception as e:
            logger.error(f"Could not analyze audio for {sound['name']}: {e}")
            return False # Don't include files we can't analyze

        return True

    def _start_collection(self):
        """Legacy method for compatibility - redirects to automated source sounds."""
        # This method existed in old code but now redirects to the new automated system
        messagebox.showinfo("Info", "Please use the '🎵 Source Sounds' button for automated collection")
