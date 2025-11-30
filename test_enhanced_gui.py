#!/usr/bin/env python3
"""
Test script for the enhanced GUI with all advanced features
"""

import sys
import tkinter as tk
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from project_name.gui.gui import SoundToolGUI
    
    def test_enhanced_gui():
        """Test the enhanced GUI"""
        print("🚀 Launching Enhanced SonicSleep Pro GUI...")
        print("✨ Features included:")
        print("   - Tabbed interface with Audio Processing, Session Manager, Advanced Mixing")
        print("   - Real-time waveform visualization")
        print("   - Enhanced audio player with controls")
        print("   - Progress tracking with detailed status")
        print("   - Advanced mix controls with EQ and effects")
        print("   - Session management (save/load/export)")
        print("   - Enhanced file management with metadata")
        print("")
        
        root = tk.Tk()
        app = SoundToolGUI(root)
        
        # Set window title and icon
        root.title("SonicSleep Pro - Enhanced GUI")
        
        # Start the application
        root.mainloop()
        
    if __name__ == "__main__":
        test_enhanced_gui()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure all dependencies are installed:")
    print("   pip install numpy scipy matplotlib pygame soundfile")
    print("   pip install tkinter")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the console for detailed error information.")
