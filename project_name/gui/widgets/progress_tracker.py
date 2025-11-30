"""
Progress tracking widget with detailed status
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime

class ProgressTracker(ttk.Frame):
    """Enhanced progress tracking with detailed status"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.current_task = None
        self.is_active = False
        self.start_time = None
        
        self.setup_progress_interface()
        
    def setup_progress_interface(self):
        """Setup progress tracking interface"""
        # Main progress frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Task label
        self.task_label = ttk.Label(main_frame, text="Ready", font=("Arial", 10, "bold"))
        self.task_label.pack(anchor=tk.W)
        
        # Progress bar frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var, 
            maximum=100, 
            length=400, 
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Percentage label
        self.percentage_label = ttk.Label(progress_frame, text="0%", width=5)
        self.percentage_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="", foreground="gray")
        self.status_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Time label
        self.time_label = ttk.Label(status_frame, text="", foreground="gray")
        self.time_label.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Detailed info frame (initially hidden)
        self.detail_frame = ttk.LabelFrame(self, text="Generation Details", padding=10)
        
        # Create details text widget with scrollbar
        text_frame = ttk.Frame(self.detail_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(
            text_frame, 
            height=6, 
            width=60, 
            font=("Consolas", 9), 
            bg="#f0f0f0",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.config(yscrollcommand=scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons for details
        detail_controls = ttk.Frame(self.detail_frame)
        detail_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            detail_controls, 
            text="Clear Log", 
            command=self.clear_details,
            width=10
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            detail_controls, 
            text="Hide Details", 
            command=self.hide_details,
            width=12
        ).pack(side=tk.RIGHT)
        
    def start_task(self, task_name, show_details=False):
        """Start tracking a new task"""
        self.current_task = task_name
        self.is_active = True
        self.start_time = time.time()
        
        self.task_label.config(text=f"🔄 {task_name}")
        self.progress_var.set(0)
        self.percentage_label.config(text="0%")
        self.status_label.config(text="Initializing...")
        self.time_label.config(text="00:00")
        
        if show_details:
            self.show_details()
            self.add_detail(f"Starting task: {task_name}")
        else:
            self.hide_details()
            
    def update_progress(self, percentage, status="", detail=""):
        """Update progress percentage and status"""
        if not self.is_active:
            return
            
        # Clamp percentage to valid range
        percentage = max(0, min(100, percentage))
        
        self.progress_var.set(percentage)
        self.percentage_label.config(text=f"{percentage:.0f}%")
        
        if status:
            self.status_label.config(text=status)
            
        # Update elapsed time
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.time_label.config(text=self._format_time(elapsed))
            
        if detail:
            self.add_detail(detail)
            
    def add_detail(self, message):
        """Add detailed progress message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        detail_msg = f"[{timestamp}] {message}\n"
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.insert(tk.END, detail_msg)
        self.details_text.see(tk.END)
        self.details_text.config(state=tk.DISABLED)
        
    def complete_task(self, success=True, message=""):
        """Complete the current task"""
        if not self.is_active:
            return
            
        self.is_active = False
        
        # Calculate total time
        total_time = ""
        if self.start_time:
            elapsed = time.time() - self.start_time
            total_time = f" ({self._format_time(elapsed)})"
        
        if success:
            self.task_label.config(text=f"✅ {self.current_task} - Complete{total_time}")
            self.progress_var.set(100)
            self.percentage_label.config(text="100%")
            self.status_label.config(text=message or "Task completed successfully!")
            self.add_detail("✅ Task completed successfully!")
        else:
            self.task_label.config(text=f"❌ {self.current_task} - Failed{total_time}")
            self.status_label.config(text=message or "Task failed!")
            self.add_detail(f"❌ Task failed: {message}")
            
        # Auto-hide details after 5 seconds (but only if not explicitly shown)
        if self.detail_frame.winfo_viewable():
            threading.Timer(5.0, self.hide_details).start()
        
    def show_details(self):
        """Show details panel"""
        self.detail_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
    def hide_details(self):
        """Hide details panel"""
        self.detail_frame.pack_forget()
        
    def clear_details(self):
        """Clear details log"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)
        
    def reset(self):
        """Reset progress tracker"""
        self.is_active = False
        self.current_task = None
        self.start_time = None
        
        self.task_label.config(text="Ready")
        self.progress_var.set(0)
        self.percentage_label.config(text="0%")
        self.status_label.config(text="")
        self.time_label.config(text="")
        self.hide_details()
        self.clear_details()
        
    def _format_time(self, seconds):
        """Format time as MM:SS"""
        try:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes:02d}:{seconds:02d}"
        except:
            return "00:00"
            
    def set_indeterminate(self):
        """Set progress bar to indeterminate mode"""
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start()
        self.percentage_label.config(text="")
        
    def set_determinate(self):
        """Set progress bar to determinate mode"""
        self.progress_bar.stop()
        self.progress_bar.config(mode='determinate')
        
    def is_task_active(self):
        """Check if a task is currently active"""
        return self.is_active
