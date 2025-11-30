#!/usr/bin/env python3
"""
Quick test to launch the GUI and verify the Freesound tab is accessible.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_freesound_tab():
    """Test that the Freesound tab loads correctly."""
    print("🎵 Testing Freesound Tab Accessibility")
    print("=" * 50)
    
    try:
        # Import the GUI components
        from project_name.gui.panels.input_panel import InputProcessingPanel
        print("✅ InputProcessingPanel imported successfully")
        
        # Test that the required attributes exist
        import tkinter as tk
        from tkinter import ttk
        
        # Create a minimal test environment
        root = tk.Tk()
        root.title("Test - SonicSleep Pro Freesound Tab")
        root.geometry("800x600")
        
        # Create a mock panel container
        class MockPanel:
            def __init__(self, parent):
                self.content_frame = ttk.Frame(parent)
                self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the panel
        mock_panel = MockPanel(root)
        input_panel = InputProcessingPanel(mock_panel)
        
        print("✅ InputProcessingPanel created successfully")
        print("✅ Freesound tab should be visible in the GUI")
        print()
        print("📋 Available tabs:")
        for i in range(input_panel.notebook.index("end")):
            tab_text = input_panel.notebook.tab(i, "text")
            print(f"   {i+1}. {tab_text}")
        
        print()
        print("🎵 To test the Source Sounds feature:")
        print("   1. Click on the 'Freesound API' tab")
        print("   2. Your API key will be auto-loaded when you click '🎵 Source Sounds'")
        print("   3. Select a collection type (e.g., 'Sleep Sounds')")
        print("   4. Choose quantity (start with 5 for testing)")
        print("   5. Click '🎵 Source Sounds' to begin automated collection")
        
        # Keep the window open for testing
        print()
        print("🖥️  GUI window opened for testing. Close the window when done.")
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_freesound_tab()
