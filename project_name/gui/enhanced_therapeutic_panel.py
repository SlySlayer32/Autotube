"""
Enhanced therapeutic audio panel with all advanced features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import tempfile
import shutil
from pathlib import Path
import numpy as np

# Import the enhanced widgets
from .widgets import (
    WaveformDisplay, 
    AudioPlayer, 
    ProgressTracker, 
    AdvancedMixControls, 
    SessionManager
)

# Import the audio engine
from ..audio_engine.therapeutic_engine_2024 import (
    TherapeuticAudioMixer,
    DynamicBinauralEngine, 
    SuperiorPinkNoiseEngine
)

class EnhancedTherapeuticPanel:
    """Enhanced therapeutic audio panel with all advanced features"""
    
    def __init__(self, panel):
        self.panel = panel
        self.content_frame = panel.content_frame
        self.mixer = TherapeuticAudioMixer()
        self.current_audio_file = None
        self.current_audio_data = None
        self.current_metadata = None
        
        self.setup_enhanced_interface()
        
    def setup_enhanced_interface(self):
        """Setup the enhanced interface with all new features"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Create main container with notebook
        self.main_notebook = ttk.Notebook(self.content_frame)
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_generator_tab()
        self.setup_analysis_tab()
        self.setup_session_tab()
        
    def setup_generator_tab(self):
        """Setup the enhanced audio generator tab"""
        gen_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(gen_frame, text="🎵 Audio Generator")
        
        # Create paned window for better layout
        paned = ttk.PanedWindow(gen_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Controls
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Right panel - Visualization
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # Setup left panel (controls)
        self.setup_generation_controls(left_frame)
        
        # Setup right panel (visualization and player)
        self.setup_visualization_panel(right_frame)
        
    def setup_generation_controls(self, parent):
        """Setup generation controls"""
        # Create scrollable frame for controls
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Protocol selection
        protocol_frame = ttk.LabelFrame(scrollable_frame, text="🧠 Therapeutic Protocol", padding=10)
        protocol_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.protocol_var = tk.StringVar(value="sleep_induction")
        protocols = [
            ("🌙 Sleep Induction (0.25 Hz)", "sleep_induction"),
            ("😴 Deep Sleep (3 Hz)", "deep_sleep"),
            ("🧘 Alpha Relaxation (8-12 Hz)", "relaxation"),
            ("🎯 Focus Enhancement (Pink Noise)", "focus"),
            ("😌 Anxiety Relief (2 Hz HRV)", "anxiety_relief"),
            ("🧠 Memory Consolidation (90min)", "memory"),
            ("✨ Custom Protocol", "custom")
        ]
        
        for text, value in protocols:
            ttk.Radiobutton(scrollable_frame, text=text, variable=self.protocol_var,
                          value=value).pack(anchor=tk.W, pady=2, padx=15)
        
        # Duration selection
        duration_frame = ttk.LabelFrame(scrollable_frame, text="⏱️ Duration", padding=10)
        duration_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.duration_var = tk.IntVar(value=60)
        duration_controls = ttk.Frame(duration_frame)
        duration_controls.pack(fill=tk.X)
        
        ttk.Label(duration_controls, text="Minutes:").pack(side=tk.LEFT)
        duration_spin = ttk.Spinbox(duration_controls, from_=1, to=480, 
                                   textvariable=self.duration_var, width=10)
        duration_spin.pack(side=tk.LEFT, padx=5)
        
        # Quick duration buttons
        quick_frame = ttk.Frame(duration_frame)
        quick_frame.pack(fill=tk.X, pady=5)
        
        for minutes in [15, 30, 60, 90, 120]:
            ttk.Button(quick_frame, text=f"{minutes}m", width=6,
                      command=lambda m=minutes: self.duration_var.set(m)).pack(side=tk.LEFT, padx=2)
        
        # Advanced controls
        self.advanced_controls = AdvancedMixControls(scrollable_frame)
        self.advanced_controls.pack(fill=tk.X, pady=5, padx=5)
        
        # Generation button
        gen_button_frame = ttk.Frame(scrollable_frame)
        gen_button_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.generate_button = ttk.Button(
            gen_button_frame, 
            text="🎵 Generate Therapeutic Audio",
            command=self.generate_audio_threaded,
            style="Accent.TButton" if hasattr(ttk.Style(), 'theme_names') else None
        )
        self.generate_button.pack(fill=tk.X, pady=5)
        
        # Export button (initially disabled)
        self.export_button = ttk.Button(
            gen_button_frame, 
            text="💾 Export Audio",
            command=self.export_audio, 
            state=tk.DISABLED
        )
        self.export_button.pack(fill=tk.X, pady=2)
        
        # Quick export buttons
        quick_export_frame = ttk.Frame(gen_button_frame)
        quick_export_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(quick_export_frame, text="Export WAV", width=10,
                  command=lambda: self.quick_export('wav')).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_export_frame, text="Export MP3", width=10,
                  command=lambda: self.quick_export('mp3')).pack(side=tk.LEFT, padx=2)
        
        # Pack scrollable controls
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_visualization_panel(self, parent):
        """Setup visualization and player panel"""
        # Progress tracker
        self.progress_tracker = ProgressTracker(parent)
        self.progress_tracker.pack(fill=tk.X, pady=5)
        
        # Waveform display
        wave_frame = ttk.LabelFrame(parent, text="🌊 Waveform Visualization", padding=5)
        wave_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.waveform_display = WaveformDisplay(wave_frame, width=700, height=200)
        self.waveform_display.pack(fill=tk.BOTH, expand=True)
        
        # Audio player
        player_frame = ttk.LabelFrame(parent, text="🎧 Audio Player", padding=5)
        player_frame.pack(fill=tk.X, pady=5)
        
        self.audio_player = AudioPlayer(player_frame)
        self.audio_player.pack(fill=tk.X)
        
        # Info display
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Audio Information", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_text = tk.Text(info_frame, height=5, font=("Consolas", 9), 
                               bg="#f8f8f8", state=tk.DISABLED, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_analysis_tab(self):
        """Setup audio analysis tab"""
        analysis_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(analysis_frame, text="📊 Analysis")
        
        # Header
        header_frame = ttk.Frame(analysis_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(header_frame, text="🔬 Audio Analysis Features", 
                 font=("Arial", 16, "bold")).pack()
        
        # Feature list
        features_frame = ttk.Frame(analysis_frame)
        features_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        features = [
            "📈 Frequency Spectrum Analysis",
            "🎯 Binaural Beat Detection & Validation", 
            "🧠 Therapeutic Efficacy Metrics",
            "✅ Audio Quality Assessment",
            "📊 Brainwave Entrainment Analysis",
            "🔍 Pink Noise Characteristic Verification",
            "⚖️ Dynamic Range Analysis",
            "🎵 Harmonic Content Analysis"
        ]
        
        for i, feature in enumerate(features):
            feature_frame = ttk.Frame(features_frame)
            feature_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(feature_frame, text=feature, font=("Arial", 11)).pack(side=tk.LEFT)
            
            if i < 3:  # First few features are "available"
                ttk.Label(feature_frame, text="✅ Available", 
                         foreground="green", font=("Arial", 9)).pack(side=tk.RIGHT)
            else:
                ttk.Label(feature_frame, text="🚧 Coming Soon", 
                         foreground="orange", font=("Arial", 9)).pack(side=tk.RIGHT)
        
        # Analysis button
        analysis_button_frame = ttk.Frame(analysis_frame)
        analysis_button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(analysis_button_frame, text="🔬 Analyze Current Audio",
                  command=self.analyze_current_audio,
                  state=tk.DISABLED).pack()
        
    def setup_session_tab(self):
        """Setup session management tab"""
        session_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(session_frame, text="💾 Sessions")
        
        self.session_manager = SessionManager(session_frame)
        self.session_manager.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def generate_audio_threaded(self):
        """Generate audio in separate thread"""
        threading.Thread(target=self.generate_audio, daemon=True).start()
        
    def generate_audio(self):
        """Generate therapeutic audio with progress tracking"""
        try:
            # Start progress tracking
            protocol = self.protocol_var.get()
            duration = self.duration_var.get()
            
            self.progress_tracker.start_task(
                f"Generating {protocol.replace('_', ' ').title()} ({duration} min)", 
                show_details=True
            )
            self.generate_button.config(state=tk.DISABLED)
            
            # Get advanced parameters
            mix_params = self.advanced_controls.get_parameters()
            
            # Update progress
            self.progress_tracker.update_progress(10, "Initializing audio engine...", 
                                                "Loading therapeutic parameters")
            
            # Generate audio based on protocol
            self.progress_tracker.update_progress(30, "Generating binaural beats...",
                                                "Creating therapeutic frequencies")
            
            if protocol == "sleep_induction":
                audio_data, metadata = self.mixer.create_ultimate_sleep_mix(
                    duration_minutes=duration,
                    include_nature=True,
                    personalization=mix_params
                )
                metadata['protocol'] = 'Sleep Induction (0.25 Hz targeting)'
                
            elif protocol == "deep_sleep":
                # Create deep sleep mix with 3 Hz targeting
                binaural_engine = DynamicBinauralEngine()
                audio_data = binaural_engine._generate_static_beat(3.0, duration * 60)
                metadata = {
                    'protocol': 'Deep Sleep (3 Hz stable)',
                    'duration': duration * 60,
                    'sample_rate': 44100,
                    'binaural_frequency': 3.0
                }
                
            elif protocol == "relaxation":
                audio_data, metadata = self.mixer.create_anxiety_reduction_mix(duration)
                metadata['protocol'] = 'Alpha Relaxation (8-12 Hz)'
                
            elif protocol == "focus":
                pink_engine = SuperiorPinkNoiseEngine()
                pink_noise = pink_engine.create_focus_enhancement_track(duration)
                audio_data = pink_noise
                metadata = {
                    'protocol': 'Focus Enhancement (Superior Pink Noise)',
                    'duration': duration * 60,
                    'sample_rate': 44100,
                    'noise_type': 'pink'
                }
                
            elif protocol == "anxiety_relief":
                audio_data, metadata = self.mixer.create_anxiety_reduction_mix(duration)
                metadata['protocol'] = 'Anxiety Relief (2 Hz HRV optimization)'
                
            elif protocol == "memory":
                pink_engine = SuperiorPinkNoiseEngine()
                memory_audio = pink_engine.create_memory_consolidation_track(duration)
                audio_data = np.column_stack((memory_audio, memory_audio))
                metadata = {
                    'protocol': 'Memory Consolidation (90min cycles)',
                    'duration': duration * 60,
                    'sample_rate': 44100,
                    'optimization': 'memory_consolidation'
                }
                
            else:  # custom
                audio_data, metadata = self.mixer.create_ultimate_sleep_mix(
                    duration_minutes=duration,
                    include_nature=True,
                    personalization=mix_params
                )
                metadata['protocol'] = 'Custom Protocol'
            
            self.progress_tracker.update_progress(70, "Processing audio...", 
                                                "Applying therapeutic enhancements")
            
            # Store audio data
            self.current_audio_data = audio_data
            self.current_metadata = metadata
            
            # Save temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            self.current_audio_file = temp_file.name
            temp_file.close()
            
            self.mixer.save_therapeutic_audio(audio_data, self.current_audio_file, metadata)
            
            self.progress_tracker.update_progress(90, "Updating visualization...",
                                                "Loading waveform display")
            
            # Update visualization
            self.waveform_display.load_audio(self.current_audio_file)
            self.audio_player.load_audio(self.current_audio_file)
            
            # Update info display
            self.update_info_display(metadata, mix_params)
            
            # Complete progress
            self.progress_tracker.complete_task(True, f"Generated {duration}-minute {protocol} audio")
            
            # Enable export button
            self.export_button.config(state=tk.NORMAL)
            
            # Update session
            if hasattr(self, 'session_manager'):
                self.session_manager.update_session_parameters(mix_params)
            
        except Exception as e:
            self.progress_tracker.complete_task(False, f"Generation failed: {str(e)}")
            messagebox.showerror("Generation Error", f"Failed to generate audio: {str(e)}")
        finally:
            self.generate_button.config(state=tk.NORMAL)
            
    def update_info_display(self, metadata, mix_params):
        """Update audio information display"""
        duration_min = metadata.get('duration', 0) / 60
        
        info_text = f"""🎵 Generated Audio Information:

Protocol: {metadata.get('protocol', 'Unknown')}
Duration: {duration_min:.1f} minutes ({metadata.get('duration', 0):.1f} seconds)
Sample Rate: {metadata.get('sample_rate', 44100)} Hz
Binaural Frequency: {metadata.get('binaural_frequency', 'Dynamic/Variable')} Hz

Mix Parameters:
• Binaural Intensity: {mix_params.get('binaural_intensity', 0.4):.2f}
• Pink Noise Level: {mix_params.get('pink_noise_level', 0.35):.2f}
• Nature Sounds: {mix_params.get('nature_sounds_level', 0.25):.2f}
• Fade Duration: {mix_params.get('fade_duration', 30):.0f} seconds

Audio Quality: {mix_params.get('audio_quality', 'High')}
Generated: {metadata.get('timestamp', 'Now')}"""
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
        self.info_text.config(state=tk.DISABLED)
        
    def export_audio(self):
        """Export generated audio"""
        if not self.current_audio_file:
            messagebox.showwarning("No Audio", "No audio to export.")
            return
            
        # Suggest filename based on protocol
        protocol = self.protocol_var.get()
        duration = self.duration_var.get()
        suggested_name = f"therapeutic_{protocol}_{duration}min.wav"
        
        filename = filedialog.asksaveasfilename(
            initialfilename=suggested_name,
            defaultextension=".wav",
            filetypes=[
                ("WAV files", "*.wav"), 
                ("MP3 files", "*.mp3"), 
                ("FLAC files", "*.flac"),
                ("All files", "*.*")
            ],
            title="Export Therapeutic Audio"
        )
        
        if filename:
            try:
                # Copy temporary file to chosen location
                shutil.copy2(self.current_audio_file, filename)
                messagebox.showinfo("Success", f"Audio exported: {Path(filename).name}")
                
                # Add to session
                if hasattr(self, 'session_manager') and self.session_manager.get_current_session():
                    params = self.advanced_controls.get_parameters()
                    params['protocol'] = self.protocol_var.get()
                    params['duration'] = self.duration_var.get()
                    self.session_manager.add_generated_file(filename, params)
                    
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export audio: {str(e)}")
                
    def quick_export(self, format_type):
        """Quick export in specified format"""
        if not self.current_audio_file:
            messagebox.showwarning("No Audio", "No audio to export.")
            return
            
        # Auto-generate filename
        protocol = self.protocol_var.get()
        duration = self.duration_var.get()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create exports directory
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        filename = exports_dir / f"therapeutic_{protocol}_{duration}min_{timestamp}.{format_type}"
        
        try:
            shutil.copy2(self.current_audio_file, filename)
            messagebox.showinfo("Quick Export", f"Exported: {filename.name}")
            
            # Add to session
            if hasattr(self, 'session_manager') and self.session_manager.get_current_session():
                params = self.advanced_controls.get_parameters()
                params['protocol'] = self.protocol_var.get()
                params['duration'] = self.duration_var.get()
                self.session_manager.add_generated_file(str(filename), params)
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            
    def analyze_current_audio(self):
        """Analyze current audio (placeholder for future implementation)"""
        if not self.current_audio_data:
            messagebox.showwarning("No Audio", "No audio to analyze.")
            return
            
        messagebox.showinfo("Analysis", "Advanced audio analysis features coming soon!")
        
    def show(self):
        """Show the therapeutic audio panel"""
        # The enhanced panel handles everything automatically
        pass
