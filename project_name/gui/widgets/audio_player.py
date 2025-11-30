"""
Audio player widget with real-time controls
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from pathlib import Path

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

class AudioPlayer(ttk.Frame):
    """Enhanced audio player with real-time controls"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        self.position = 0
        self.duration = 0
        self.update_running = True
        
        # Initialize pygame mixer
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
                self.audio_available = True
            except Exception as e:
                print(f"Pygame mixer init failed: {e}")
                self.audio_available = False
        else:
            self.audio_available = False
        
        self.setup_player_interface()
        
        # Start position update thread
        if self.audio_available:
            self.update_thread = threading.Thread(target=self._update_position, daemon=True)
            self.update_thread.start()
        
    def setup_player_interface(self):
        """Setup the audio player interface"""
        # Main control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Play/Pause button
        self.play_button = ttk.Button(
            control_frame, 
            text="▶ Play", 
            command=self.toggle_playback, 
            width=12,
            state=tk.NORMAL if self.audio_available else tk.DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        # Stop button
        self.stop_button = ttk.Button(
            control_frame, 
            text="⏹ Stop", 
            command=self.stop_playback, 
            width=12,
            state=tk.NORMAL if self.audio_available else tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        # Position frame
        position_frame = ttk.Frame(self)
        position_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Time display
        self.time_label = ttk.Label(position_frame, text="00:00 / 00:00")
        self.time_label.pack(side=tk.LEFT)
        
        # Position slider
        self.position_var = tk.DoubleVar()
        self.position_slider = ttk.Scale(
            position_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL, 
            variable=self.position_var,
            command=self.seek_position,
            state=tk.NORMAL if self.audio_available else tk.DISABLED
        )
        self.position_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Volume frame
        volume_frame = ttk.Frame(self)
        volume_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(volume_frame, text="🔊").pack(side=tk.LEFT)
        
        # Volume slider
        self.volume_var = tk.DoubleVar(value=70)
        volume_slider = ttk.Scale(
            volume_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL, 
            variable=self.volume_var,
            command=self.set_volume, 
            length=100,
            state=tk.NORMAL if self.audio_available else tk.DISABLED
        )
        volume_slider.pack(side=tk.LEFT, padx=5)
        
        # Status label
        status_text = "No audio loaded"
        if not self.audio_available:
            status_text = "Audio playback unavailable (install pygame)"
            
        self.status_label = ttk.Label(self, text=status_text, foreground="gray")
        self.status_label.pack(pady=2)
        
    def load_audio(self, file_path):
        """Load audio file for playback"""
        if not self.audio_available:
            self.status_label.config(text="Audio playback unavailable")
            return
            
        try:
            self.current_file = str(file_path)
            
            # Stop any current playback
            self.stop_playback()
            
            # Load the file
            pygame.mixer.music.load(self.current_file)
            
            # Get file info
            self.duration = self._get_audio_duration(file_path)
            
            filename = Path(file_path).name
            self.status_label.config(text=f"Loaded: {filename}")
            
            # Reset position
            self.position = 0
            self.position_var.set(0)
            
            # Enable controls
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            print(f"Audio load error: {e}")
            
    def _get_audio_duration(self, file_path):
        """Get audio file duration"""
        if not SOUNDFILE_AVAILABLE:
            return 60  # Default duration if soundfile not available
            
        try:
            info = sf.info(file_path)
            return info.duration
        except Exception as e:
            print(f"Duration detection error: {e}")
            return 60  # Default duration
            
    def toggle_playback(self):
        """Toggle play/pause"""
        if not self.audio_available or not self.current_file:
            return
            
        try:
            if self.is_playing:
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.play_button.config(text="⏸ Pause")
                    self.is_paused = False
                else:
                    pygame.mixer.music.pause()
                    self.play_button.config(text="▶ Play")
                    self.is_paused = True
            else:
                pygame.mixer.music.play()
                self.play_button.config(text="⏸ Pause")
                self.is_playing = True
                self.is_paused = False
                
        except Exception as e:
            self.status_label.config(text=f"Playback error: {str(e)}")
            print(f"Playback error: {e}")
            
    def stop_playback(self):
        """Stop playback"""
        if not self.audio_available:
            return
            
        try:
            pygame.mixer.music.stop()
            self.play_button.config(text="▶ Play")
            self.is_playing = False
            self.is_paused = False
            self.position = 0
            self.position_var.set(0)
            
        except Exception as e:
            print(f"Stop playback error: {e}")
        
    def set_volume(self, value):
        """Set playback volume"""
        if not self.audio_available:
            return
            
        try:
            self.volume = float(value) / 100
            pygame.mixer.music.set_volume(self.volume)
        except Exception as e:
            print(f"Volume set error: {e}")
        
    def seek_position(self, value):
        """Seek to position (limited support in pygame)"""
        # Note: pygame doesn't support seeking well, this is mostly visual
        try:
            if self.duration > 0:
                target_position = (float(value) / 100) * self.duration
                # For now, just update the visual position
                # Full seeking would require a different audio library
        except Exception as e:
            print(f"Seek error: {e}")
        
    def _update_position(self):
        """Update position display in background thread"""
        while self.update_running:
            try:
                if self.is_playing and not self.is_paused and self.audio_available:
                    # Check if music is still playing
                    if pygame.mixer.music.get_busy():
                        self.position += 0.1
                        if self.duration > 0:
                            progress = min((self.position / self.duration) * 100, 100)
                            self.position_var.set(progress)
                            
                        # Update time display
                        current_time = self._format_time(self.position)
                        total_time = self._format_time(self.duration)
                        self.time_label.config(text=f"{current_time} / {total_time}")
                        
                    else:
                        # Song ended
                        if self.is_playing:
                            self.stop_playback()
                            
            except Exception as e:
                print(f"Position update error: {e}")
                
            time.sleep(0.1)
            
    def _format_time(self, seconds):
        """Format time as MM:SS"""
        try:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes:02d}:{seconds:02d}"
        except:
            return "00:00"
            
    def destroy(self):
        """Clean up when widget is destroyed"""
        self.update_running = False
        if self.audio_available:
            try:
                pygame.mixer.music.stop()
            except:
                pass
        super().destroy()
        
    def is_audio_available(self):
        """Check if audio playback is available"""
        return self.audio_available
