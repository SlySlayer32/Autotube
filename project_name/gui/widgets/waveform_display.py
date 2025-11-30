"""
Waveform display widget for real-time audio visualization
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import threading
import tempfile
import os

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

class WaveformDisplay(ttk.Frame):
    """Enhanced waveform display with real-time visualization"""
    
    def __init__(self, parent, width=800, height=200):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.current_audio = None
        self.sample_rate = None
        
        if MATPLOTLIB_AVAILABLE:
            self.setup_visualization()
        else:
            self.setup_fallback()
        
    def setup_visualization(self):
        """Setup matplotlib canvas for waveform display"""
        try:
            # Set matplotlib style
            plt.style.use('dark_background')
            
            # Create figure with dark theme
            self.figure = Figure(figsize=(self.width/100, self.height/100), 
                               facecolor='#2b2b2b', edgecolor='none')
            self.ax = self.figure.add_subplot(111, facecolor='#2b2b2b')
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Setup initial display
            self.show_placeholder()
            
        except Exception as e:
            print(f"Matplotlib setup failed: {e}")
            self.setup_fallback()
        
    def setup_fallback(self):
        """Setup fallback display when matplotlib not available"""
        fallback_frame = ttk.Frame(self)
        fallback_frame.pack(fill=tk.BOTH, expand=True)
        
        self.fallback_label = ttk.Label(
            fallback_frame, 
            text="🌊 Waveform Visualization\n(Install matplotlib for enhanced display)",
            justify=tk.CENTER,
            font=("Arial", 12)
        )
        self.fallback_label.pack(expand=True)
        
    def show_placeholder(self):
        """Show placeholder when no audio loaded"""
        if not MATPLOTLIB_AVAILABLE:
            self.fallback_label.config(text="🌊 Load audio to see waveform\n(Install matplotlib for enhanced display)")
            return
            
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, '🎵 Load audio to see waveform', 
                        ha='center', va='center', transform=self.ax.transAxes,
                        color='#888888', fontsize=14)
            self.ax.set_facecolor('#2b2b2b')
            self.canvas.draw()
        except Exception as e:
            print(f"Placeholder display error: {e}")
        
    def load_audio(self, audio_path):
        """Load and display audio waveform"""
        if not SOUNDFILE_AVAILABLE:
            self.show_error("Install soundfile library for audio loading")
            return
            
        try:
            # Load audio file
            audio_data, sample_rate = sf.read(audio_path)
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)  # Convert to mono
                
            self.current_audio = audio_data
            self.sample_rate = sample_rate
            
            # Update display in separate thread
            threading.Thread(target=self._update_waveform, daemon=True).start()
            
        except Exception as e:
            self.show_error(f"Error loading audio: {str(e)}")
            
    def _update_waveform(self):
        """Update waveform display"""
        if not MATPLOTLIB_AVAILABLE:
            if hasattr(self, 'fallback_label'):
                self.fallback_label.config(
                    text=f"🎵 Audio Loaded\nSamples: {len(self.current_audio) if self.current_audio is not None else 0}\nSample Rate: {self.sample_rate}"
                )
            return
            
        if self.current_audio is None:
            return
            
        try:
            # Downsample for display if necessary
            audio = self.current_audio
            if len(audio) > 10000:
                step = len(audio) // 10000
                audio = audio[::step]
                
            # Create time axis
            time = np.linspace(0, len(self.current_audio) / self.sample_rate, len(audio))
            
            # Clear and plot
            self.ax.clear()
            self.ax.plot(time, audio, color='#00ff88', linewidth=0.8, alpha=0.8)
            self.ax.fill_between(time, audio, alpha=0.3, color='#00ff88')
            
            # Styling
            self.ax.set_facecolor('#2b2b2b')
            self.ax.set_xlabel('Time (seconds)', color='white')
            self.ax.set_ylabel('Amplitude', color='white')
            self.ax.tick_params(colors='white')
            self.ax.grid(True, alpha=0.3, color='#555555')
            
            # Set title
            duration = len(self.current_audio) / self.sample_rate
            self.ax.set_title(f'Audio Waveform - Duration: {duration:.1f}s', color='white')
            
            # Update canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Waveform update error: {e}")
            self.show_error(f"Display error: {str(e)}")
        
    def load_generated_audio(self, audio_data, sample_rate):
        """Load generated audio data directly"""
        if isinstance(audio_data, np.ndarray):
            # Handle stereo to mono conversion
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
                
            self.current_audio = audio_data
            self.sample_rate = sample_rate
            threading.Thread(target=self._update_waveform, daemon=True).start()
        else:
            self.show_error("Invalid audio data format")
        
    def show_error(self, message):
        """Show error message"""
        if not MATPLOTLIB_AVAILABLE:
            if hasattr(self, 'fallback_label'):
                self.fallback_label.config(text=f"❌ {message}")
            return
            
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"❌ {message}", 
                        ha='center', va='center', transform=self.ax.transAxes,
                        color='#ff4444', fontsize=12)
            self.ax.set_facecolor('#2b2b2b')
            self.canvas.draw()
        except Exception as e:
            print(f"Error display failed: {e}")
            
    def clear_display(self):
        """Clear the waveform display"""
        self.current_audio = None
        self.sample_rate = None
        self.show_placeholder()
