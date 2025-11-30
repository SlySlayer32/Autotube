"""
Advanced mixing controls for fine-tuning audio generation
"""

import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

class AdvancedMixControls(ttk.Frame):
    """Advanced mixing controls for fine-tuning audio generation"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Default parameters based on research
        self.mix_parameters = {
            'binaural_intensity': 0.4,
            'pink_noise_level': 0.35,
            'nature_sounds_level': 0.25,
            'fade_duration': 30,
            'variation_amount': 0.2,
            'eq_bass': 0.0,
            'eq_mid': 0.0,
            'eq_treble': 0.0,
            'stereo_width': 1.0,
            'dynamic_range': 0.8,
            'carrier_frequency': 200.0,
            'modulation_rate': 0.05
        }
        
        # Store slider variables for updates
        self.slider_vars = {}
        
        self.setup_controls()
        
    def setup_controls(self):
        """Setup advanced control interface"""
        # Create notebook for organized controls
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Audio Levels Tab
        self.setup_levels_tab()
        
        # EQ & Effects Tab  
        self.setup_eq_tab()
        
        # Advanced Tab
        self.setup_advanced_tab()
        
        # Presets Tab
        self.setup_presets_tab()
        
    def setup_levels_tab(self):
        """Setup audio levels control tab"""
        levels_frame = ttk.Frame(self.notebook)
        self.notebook.add(levels_frame, text="🎚️ Levels")
        
        # Create scrollable frame
        canvas = tk.Canvas(levels_frame)
        scrollbar = ttk.Scrollbar(levels_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Component levels
        ttk.Label(scrollable_frame, text="Audio Component Levels", 
                 font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        self.create_slider_control(scrollable_frame, "Binaural Beats Intensity", 
                                 "binaural_intensity", 0.0, 1.0, 0.01,
                                 "Controls the volume of binaural beats")
        
        self.create_slider_control(scrollable_frame, "Pink Noise Level", 
                                 "pink_noise_level", 0.0, 1.0, 0.01,
                                 "Background pink noise for masking and memory")
        
        self.create_slider_control(scrollable_frame, "Nature Sounds Level", 
                                 "nature_sounds_level", 0.0, 1.0, 0.01,
                                 "Rain and ambient nature sounds")
        
        # Timing controls
        ttk.Label(scrollable_frame, text="Timing & Dynamics", 
                 font=("Arial", 12, "bold")).pack(pady=(20, 5))
        
        self.create_slider_control(scrollable_frame, "Fade Duration (seconds)", 
                                 "fade_duration", 5, 120, 1,
                                 "How long fade-in/out transitions take")
        
        self.create_slider_control(scrollable_frame, "Variation Amount", 
                                 "variation_amount", 0.0, 1.0, 0.01,
                                 "How much the audio varies over time")
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_eq_tab(self):
        """Setup EQ and effects control tab"""
        eq_frame = ttk.Frame(self.notebook)
        self.notebook.add(eq_frame, text="🎛️ EQ & Effects")
        
        # EQ Controls
        eq_label = ttk.Label(eq_frame, text="3-Band Equalizer", font=("Arial", 12, "bold"))
        eq_label.pack(pady=(10, 5))
        
        ttk.Label(eq_frame, text="Adjust frequency response for different therapeutic effects",
                 foreground="gray").pack(pady=(0, 10))
        
        self.create_slider_control(eq_frame, "Bass (-12 to +12 dB)", 
                                 "eq_bass", -12, 12, 0.5,
                                 "Low frequencies (20-200 Hz)")
        
        self.create_slider_control(eq_frame, "Mid (-12 to +12 dB)", 
                                 "eq_mid", -12, 12, 0.5,
                                 "Mid frequencies (200-2000 Hz)")
        
        self.create_slider_control(eq_frame, "Treble (-12 to +12 dB)", 
                                 "eq_treble", -12, 12, 0.5,
                                 "High frequencies (2000+ Hz)")
        
        # Effects
        effects_label = ttk.Label(eq_frame, text="Spatial Effects", font=("Arial", 12, "bold"))
        effects_label.pack(pady=(20, 5))
        
        self.create_slider_control(eq_frame, "Stereo Width", 
                                 "stereo_width", 0.0, 2.0, 0.1,
                                 "Controls stereo field width (1.0 = normal)")
        
        self.create_slider_control(eq_frame, "Dynamic Range", 
                                 "dynamic_range", 0.1, 1.0, 0.05,
                                 "Controls how compressed the audio is")
        
    def setup_advanced_tab(self):
        """Setup advanced control tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="⚙️ Advanced")
        
        # Binaural Beat Parameters
        binaural_label = ttk.Label(advanced_frame, text="Binaural Beat Parameters", 
                                 font=("Arial", 12, "bold"))
        binaural_label.pack(pady=(10, 5))
        
        self.create_slider_control(advanced_frame, "Carrier Frequency (Hz)", 
                                 "carrier_frequency", 50, 500, 10,
                                 "Base frequency for binaural beats")
        
        self.create_slider_control(advanced_frame, "Modulation Rate (Hz)", 
                                 "modulation_rate", 0.01, 0.2, 0.01,
                                 "How fast dynamic beats change")
        
        # Custom frequency input
        custom_frame = ttk.LabelFrame(advanced_frame, text="Custom Binaural Frequency", 
                                    padding=10)
        custom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        freq_frame = ttk.Frame(custom_frame)
        freq_frame.pack(fill=tk.X)
        
        ttk.Label(freq_frame, text="Target Frequency (Hz):").pack(side=tk.LEFT)
        self.custom_freq_var = tk.StringVar(value="8.0")
        freq_entry = ttk.Entry(freq_frame, textvariable=self.custom_freq_var, width=10)
        freq_entry.pack(side=tk.RIGHT)
        
        ttk.Label(custom_frame, text="Common frequencies: 0.25 (sleep), 3 (deep sleep), 8 (alpha), 10 (focus)",
                 foreground="gray", font=("Arial", 8)).pack(pady=(5, 0))
        
        # Quality settings
        quality_frame = ttk.LabelFrame(advanced_frame, text="Audio Quality", padding=10)
        quality_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.quality_var = tk.StringVar(value="high")
        ttk.Radiobutton(quality_frame, text="🔊 High Quality (44.1 kHz)", 
                       variable=self.quality_var, value="high").pack(anchor=tk.W)
        ttk.Radiobutton(quality_frame, text="📱 Standard Quality (22 kHz)", 
                       variable=self.quality_var, value="standard").pack(anchor=tk.W)
        ttk.Radiobutton(quality_frame, text="💽 Low Quality (11 kHz)", 
                       variable=self.quality_var, value="low").pack(anchor=tk.W)
        
    def setup_presets_tab(self):
        """Setup presets management tab"""
        presets_frame = ttk.Frame(self.notebook)
        self.notebook.add(presets_frame, text="📋 Presets")
        
        # Built-in presets
        builtin_frame = ttk.LabelFrame(presets_frame, text="Built-in Presets", padding=10)
        builtin_frame.pack(fill=tk.X, padx=10, pady=10)
        
        preset_buttons_frame = ttk.Frame(builtin_frame)
        preset_buttons_frame.pack(fill=tk.X)
        
        presets = [
            ("🌙 Sleep Optimized", "sleep"),
            ("🎯 Focus Enhanced", "focus"), 
            ("🧘 Deep Relaxation", "relax"),
            ("📚 Memory Study", "memory"),
            ("😌 Anxiety Relief", "anxiety"),
            ("🔄 Reset to Default", "default")
        ]
        
        for i, (text, preset_name) in enumerate(presets):
            row = i // 2
            col = i % 2
            
            btn = ttk.Button(
                preset_buttons_frame, 
                text=text, 
                command=lambda p=preset_name: self.load_preset(p),
                width=20
            )
            btn.grid(row=row, column=col, padx=5, pady=2, sticky="ew")
            
        preset_buttons_frame.columnconfigure(0, weight=1)
        preset_buttons_frame.columnconfigure(1, weight=1)
        
        # Custom presets
        custom_frame = ttk.LabelFrame(presets_frame, text="Custom Presets", padding=10)
        custom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Preset name entry
        name_frame = ttk.Frame(custom_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Preset Name:").pack(side=tk.LEFT)
        self.preset_name_var = tk.StringVar()
        preset_name_entry = ttk.Entry(name_frame, textvariable=self.preset_name_var)
        preset_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Save/Load buttons
        buttons_frame = ttk.Frame(custom_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_frame, text="💾 Save Preset", 
                  command=self.save_custom_preset).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="📂 Load Preset", 
                  command=self.load_custom_preset).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="🗑️ Delete Preset", 
                  command=self.delete_custom_preset).pack(side=tk.LEFT, padx=2)
        
        # Preset list
        list_frame = ttk.Frame(custom_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preset_listbox = tk.Listbox(list_frame, height=5)
        preset_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.preset_listbox.config(yscrollcommand=preset_scrollbar.set)
        preset_scrollbar.config(command=self.preset_listbox.yview)
        
        self.preset_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preset_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load custom presets
        self.load_custom_presets_list()
        
    def create_slider_control(self, parent, label, param_key, min_val, max_val, resolution, tooltip=""):
        """Create a labeled slider control with tooltip"""
        # Main frame
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Label with current value
        value_var = tk.StringVar()
        current_val = self.mix_parameters.get(param_key, min_val)
        value_var.set(f"{label}: {current_val:.2f}")
        
        label_widget = ttk.Label(frame, textvariable=value_var)
        label_widget.pack(anchor=tk.W)
        
        # Tooltip if provided
        if tooltip:
            tooltip_label = ttk.Label(frame, text=f"ℹ️ {tooltip}", 
                                    foreground="gray", font=("Arial", 8))
            tooltip_label.pack(anchor=tk.W, padx=(10, 0))
          # Slider
        slider_var = tk.DoubleVar(value=current_val)
        slider = ttk.Scale(
            frame, 
            from_=min_val, 
            to=max_val, 
            orient=tk.HORIZONTAL, 
            variable=slider_var
        )
        slider.pack(fill=tk.X, pady=(2, 0))
        
        # Store slider variable for updates
        self.slider_vars[param_key] = (slider_var, value_var, label)
        
        # Update function
        def update_value(*args):
            val = slider_var.get()
            self.mix_parameters[param_key] = val
            value_var.set(f"{label}: {val:.2f}")
            
        slider_var.trace('w', update_value)
        
        return slider_var
        
    def load_preset(self, preset_name):
        """Load predefined settings preset"""
        presets = {
            "sleep": {
                'binaural_intensity': 0.2,
                'pink_noise_level': 0.5,
                'nature_sounds_level': 0.3,
                'fade_duration': 60,
                'variation_amount': 0.1,
                'eq_bass': 2.0,
                'eq_mid': -1.0,
                'eq_treble': -3.0,
                'stereo_width': 0.8,
                'dynamic_range': 0.6,
                'carrier_frequency': 150.0,
                'modulation_rate': 0.02
            },
            "focus": {
                'binaural_intensity': 0.4,
                'pink_noise_level': 0.6,
                'nature_sounds_level': 0.0,
                'fade_duration': 15,
                'variation_amount': 0.3,
                'eq_bass': 0.0,
                'eq_mid': 1.0,
                'eq_treble': 0.5,
                'stereo_width': 1.2,
                'dynamic_range': 0.9,
                'carrier_frequency': 200.0,
                'modulation_rate': 0.05
            },
            "relax": {
                'binaural_intensity': 0.3,
                'pink_noise_level': 0.3,
                'nature_sounds_level': 0.4,
                'fade_duration': 45,
                'variation_amount': 0.2,
                'eq_bass': 1.0,
                'eq_mid': 0.5,
                'eq_treble': -1.0,
                'stereo_width': 1.0,
                'dynamic_range': 0.7,
                'carrier_frequency': 180.0,
                'modulation_rate': 0.03
            },
            "memory": {
                'binaural_intensity': 0.25,
                'pink_noise_level': 0.6,
                'nature_sounds_level': 0.15,
                'fade_duration': 30,
                'variation_amount': 0.15,
                'eq_bass': 0.5,
                'eq_mid': 0.0,
                'eq_treble': -0.5,
                'stereo_width': 1.0,
                'dynamic_range': 0.8,
                'carrier_frequency': 160.0,
                'modulation_rate': 0.02
            },
            "anxiety": {
                'binaural_intensity': 0.2,
                'pink_noise_level': 0.25,
                'nature_sounds_level': 0.55,
                'fade_duration': 60,
                'variation_amount': 0.1,
                'eq_bass': 1.5,
                'eq_mid': 0.0,
                'eq_treble': -2.0,
                'stereo_width': 0.9,
                'dynamic_range': 0.6,
                'carrier_frequency': 140.0,
                'modulation_rate': 0.02
            },
            "default": {
                'binaural_intensity': 0.4,
                'pink_noise_level': 0.35,
                'nature_sounds_level': 0.25,
                'fade_duration': 30,
                'variation_amount': 0.2,
                'eq_bass': 0.0,
                'eq_mid': 0.0,
                'eq_treble': 0.0,
                'stereo_width': 1.0,
                'dynamic_range': 0.8,
                'carrier_frequency': 200.0,
                'modulation_rate': 0.05
            }
        }
        
        if preset_name in presets:
            self.mix_parameters.update(presets[preset_name])
            self.update_all_sliders()
            
    def update_all_sliders(self):
        """Update all slider displays to reflect current parameters"""
        for param_key, (slider_var, value_var, label) in self.slider_vars.items():
            if param_key in self.mix_parameters:
                val = self.mix_parameters[param_key]
                slider_var.set(val)
                value_var.set(f"{label}: {val:.2f}")
                
    def save_custom_preset(self):
        """Save current settings as custom preset"""
        name = self.preset_name_var.get().strip()
        if not name:
            tk.messagebox.showwarning("No Name", "Please enter a preset name.")
            return
            
        presets_dir = Path("presets")
        presets_dir.mkdir(exist_ok=True)
        
        preset_file = presets_dir / f"{name}.json"
        
        try:
            with open(preset_file, 'w') as f:
                json.dump(self.mix_parameters, f, indent=2)
            tk.messagebox.showinfo("Success", f"Preset '{name}' saved successfully!")
            self.load_custom_presets_list()
            self.preset_name_var.set("")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save preset: {str(e)}")
            
    def load_custom_preset(self):
        """Load selected custom preset"""
        selection = self.preset_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("No Selection", "Please select a preset to load.")
            return
            
        preset_name = self.preset_listbox.get(selection[0])
        preset_file = Path("presets") / f"{preset_name}.json"
        
        try:
            with open(preset_file, 'r') as f:
                preset_data = json.load(f)
            self.mix_parameters.update(preset_data)
            self.update_all_sliders()
            tk.messagebox.showinfo("Success", f"Preset '{preset_name}' loaded successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load preset: {str(e)}")
            
    def delete_custom_preset(self):
        """Delete selected custom preset"""
        selection = self.preset_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("No Selection", "Please select a preset to delete.")
            return
            
        preset_name = self.preset_listbox.get(selection[0])
        
        if tk.messagebox.askyesno("Confirm Delete", f"Delete preset '{preset_name}'?"):
            preset_file = Path("presets") / f"{preset_name}.json"
            try:
                preset_file.unlink()
                self.load_custom_presets_list()
                tk.messagebox.showinfo("Success", f"Preset '{preset_name}' deleted.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to delete preset: {str(e)}")
                
    def load_custom_presets_list(self):
        """Load custom presets into listbox"""
        self.preset_listbox.delete(0, tk.END)
        
        presets_dir = Path("presets")
        if presets_dir.exists():
            for preset_file in presets_dir.glob("*.json"):
                self.preset_listbox.insert(tk.END, preset_file.stem)
        
    def get_parameters(self):
        """Get current mix parameters"""
        params = self.mix_parameters.copy()
        
        # Add custom frequency if specified
        try:
            custom_freq = float(self.custom_freq_var.get())
            params['custom_binaural_frequency'] = custom_freq
        except:
            pass
            
        # Add quality setting
        params['audio_quality'] = self.quality_var.get()
        
        return params
        
    def reset_all_settings(self):
        """Reset all settings to defaults"""
        self.load_preset("default")
