"""
Session management widget for saving/loading work
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
from datetime import datetime
from pathlib import Path

class SessionManager(ttk.Frame):
    """Session management for saving/loading work"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.sessions_dir = Path("sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session = None
        
        self.setup_session_interface()
        self.load_recent_sessions()
        
    def setup_session_interface(self):
        """Setup session management interface"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="💾 Session Management", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Current session display
        self.session_label = ttk.Label(header_frame, text="No session loaded", 
                                     foreground="gray", font=("Arial", 10))
        self.session_label.pack(side=tk.RIGHT)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Primary buttons
        primary_buttons = ttk.Frame(button_frame)
        primary_buttons.pack(fill=tk.X)
        
        ttk.Button(primary_buttons, text="📁 New Session", 
                  command=self.new_session, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(primary_buttons, text="💾 Save Session", 
                  command=self.save_session, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(primary_buttons, text="📂 Load Session", 
                  command=self.load_session, width=15).pack(side=tk.LEFT, padx=2)
        
        # Secondary buttons
        secondary_buttons = ttk.Frame(button_frame)
        secondary_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(secondary_buttons, text="📤 Export Session", 
                  command=self.export_session, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(secondary_buttons, text="📥 Import Session", 
                  command=self.import_session, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(secondary_buttons, text="🗑️ Delete Session", 
                  command=self.delete_session, width=15).pack(side=tk.LEFT, padx=2)
        
        # Recent sessions
        recent_frame = ttk.LabelFrame(self, text="Recent Sessions", padding=10)
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # Create listbox for recent sessions
        listbox_frame = ttk.Frame(recent_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.sessions_listbox = tk.Listbox(listbox_frame, height=8, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.sessions_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sessions_listbox.yview)
        
        self.sessions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to load
        self.sessions_listbox.bind("<Double-Button-1>", self.load_selected_session)
        
        # Session info display
        info_frame = ttk.LabelFrame(self, text="Session Information", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=4, font=("Consolas", 9), 
                               bg="#f8f8f8", state=tk.DISABLED, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Notes section
        notes_frame = ttk.LabelFrame(self, text="Session Notes", padding=10)
        notes_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        self.notes_text = tk.Text(notes_frame, height=3, font=("Arial", 10), wrap=tk.WORD)
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        self.notes_text.config(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind notes changes
        self.notes_text.bind("<KeyRelease>", self.update_session_notes)
        
    def new_session(self):
        """Create new session"""
        name = simpledialog.askstring("New Session", "Enter session name:")
        if name:
            self.current_session = {
                'name': name,
                'created': datetime.now().isoformat(),
                'modified': datetime.now().isoformat(),
                'parameters': {},
                'generated_files': [],
                'notes': '',
                'version': '1.0'
            }
            self.session_label.config(text=f"Session: {name} (unsaved)")
            self.update_session_info()
            self.notes_text.delete(1.0, tk.END)
            
    def save_session(self):
        """Save current session"""
        if not self.current_session:
            messagebox.showwarning("No Session", "Please create a new session first.")
            return
            
        # Update notes
        self.current_session['notes'] = self.notes_text.get(1.0, tk.END).strip()
        
        # Generate filename
        name = self.current_session['name']
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{safe_name}_{timestamp}.json"
        filepath = self.sessions_dir / filename
        
        # Update modification time
        self.current_session['modified'] = datetime.now().isoformat()
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.current_session, f, indent=2)
            messagebox.showinfo("Success", f"Session saved: {filename}")
            self.session_label.config(text=f"Session: {self.current_session['name']} (saved)")
            self.load_recent_sessions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
            
    def load_session(self):
        """Load session from file"""
        filepath = filedialog.askopenfilename(
            initialdir=self.sessions_dir,
            title="Load Session",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self._load_session_file(filepath)
            
    def load_selected_session(self, event=None):
        """Load selected session from listbox"""
        selection = self.sessions_listbox.curselection()
        if selection:
            filename = self.sessions_listbox.get(selection[0]).split(' - ')[0]
            
            # Find the actual file
            for session_file in self.sessions_dir.glob("*.json"):
                if session_file.name.startswith(filename) or filename in session_file.name:
                    self._load_session_file(session_file)
                    break
                    
    def _load_session_file(self, filepath):
        """Load session from file path"""
        try:
            with open(filepath, 'r') as f:
                self.current_session = json.load(f)
                
            self.session_label.config(text=f"Session: {self.current_session['name']} (loaded)")
            self.update_session_info()
            
            # Load notes
            notes = self.current_session.get('notes', '')
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, notes)
            
            messagebox.showinfo("Success", "Session loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")
            
    def export_session(self):
        """Export session to custom location"""
        if not self.current_session:
            messagebox.showwarning("No Session", "No session to export.")
            return
            
        # Suggest filename
        name = self.current_session['name']
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        default_name = f"{safe_name}_export.json"
        
        filepath = filedialog.asksaveasfilename(
            initialfilename=default_name,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Session"
        )
        
        if filepath:
            try:
                # Update export info
                export_session = self.current_session.copy()
                export_session['exported'] = datetime.now().isoformat()
                export_session['notes'] = self.notes_text.get(1.0, tk.END).strip()
                
                with open(filepath, 'w') as f:
                    json.dump(export_session, f, indent=2)
                messagebox.showinfo("Success", f"Session exported: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export session: {str(e)}")
                
    def import_session(self):
        """Import session from external file"""
        filepath = filedialog.askopenfilename(
            title="Import Session",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    imported_session = json.load(f)
                    
                # Add import info
                imported_session['imported'] = datetime.now().isoformat()
                imported_session['original_file'] = str(filepath)
                
                # Save to sessions directory
                name = imported_session.get('name', 'Imported Session')
                safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{safe_name}_imported_{timestamp}.json"
                
                session_filepath = self.sessions_dir / filename
                with open(session_filepath, 'w') as f:
                    json.dump(imported_session, f, indent=2)
                    
                messagebox.showinfo("Success", f"Session imported and saved as: {filename}")
                self.load_recent_sessions()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import session: {str(e)}")
                
    def delete_session(self):
        """Delete selected session"""
        selection = self.sessions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a session to delete.")
            return
            
        filename = self.sessions_listbox.get(selection[0]).split(' - ')[0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete session '{filename}'?"):
            try:
                # Find and delete the file
                for session_file in self.sessions_dir.glob("*.json"):
                    if session_file.name.startswith(filename) or filename in session_file.name:
                        session_file.unlink()
                        break
                        
                self.load_recent_sessions()
                messagebox.showinfo("Success", "Session deleted.")
                
                # Clear current session if it was deleted
                if self.current_session and self.current_session['name'] in filename:
                    self.current_session = None
                    self.session_label.config(text="No session loaded")
                    self.update_session_info()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete session: {str(e)}")
                
    def load_recent_sessions(self):
        """Load recent sessions into listbox"""
        self.sessions_listbox.delete(0, tk.END)
        
        try:
            session_files = list(self.sessions_dir.glob("*.json"))
            session_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for session_file in session_files[:20]:  # Show last 20 sessions
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    name = session_data.get('name', session_file.stem)
                    modified = session_data.get('modified', '')
                    
                    if modified:
                        try:
                            mod_time = datetime.fromisoformat(modified)
                            time_str = mod_time.strftime('%Y-%m-%d %H:%M')
                        except:
                            time_str = modified[:16]  # Fallback
                    else:
                        time_str = "Unknown"
                        
                    display_text = f"{name} - {time_str}"
                    self.sessions_listbox.insert(tk.END, display_text)
                    
                except Exception as e:
                    # Skip corrupted session files
                    print(f"Skipping corrupted session file {session_file}: {e}")
                    continue
                
        except Exception as e:
            print(f"Error loading recent sessions: {e}")
            
    def update_session_info(self):
        """Update session information display"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if self.current_session:
            info = f"""Session: {self.current_session['name']}
Created: {self._format_datetime(self.current_session.get('created', ''))}
Modified: {self._format_datetime(self.current_session.get('modified', ''))}
Generated Files: {len(self.current_session.get('generated_files', []))}
Parameters Saved: {'Yes' if self.current_session.get('parameters') else 'No'}
Version: {self.current_session.get('version', '1.0')}"""
        else:
            info = "No session loaded.\n\nCreate a new session or load an existing one to track your therapeutic audio generation work."
            
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)
        
    def update_session_notes(self, event=None):
        """Update session notes when text changes"""
        if self.current_session:
            notes = self.notes_text.get(1.0, tk.END).strip()
            self.current_session['notes'] = notes
            # Mark as modified
            self.session_label.config(text=f"Session: {self.current_session['name']} (modified)")
            
    def _format_datetime(self, datetime_str):
        """Format datetime string for display"""
        if not datetime_str:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(datetime_str)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime_str
            
    def get_current_session(self):
        """Get current session data"""
        return self.current_session
        
    def update_session_parameters(self, parameters):
        """Update session with current parameters"""
        if self.current_session:
            self.current_session['parameters'] = parameters.copy()
            self.current_session['modified'] = datetime.now().isoformat()
            self.session_label.config(text=f"Session: {self.current_session['name']} (modified)")
            self.update_session_info()
            
    def add_generated_file(self, filepath, parameters):
        """Add generated file to session"""
        if self.current_session:
            file_info = {
                'filepath': str(filepath),
                'filename': Path(filepath).name,
                'generated': datetime.now().isoformat(),
                'parameters': parameters.copy(),
                'size_mb': round(Path(filepath).stat().st_size / (1024 * 1024), 2) if Path(filepath).exists() else 0
            }
            
            if 'generated_files' not in self.current_session:
                self.current_session['generated_files'] = []
                
            self.current_session['generated_files'].append(file_info)
            self.current_session['modified'] = datetime.now().isoformat()
            self.update_session_info()
            
    def get_session_files(self):
        """Get list of files generated in current session"""
        if self.current_session:
            return self.current_session.get('generated_files', [])
        return []
