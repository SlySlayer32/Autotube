#!/usr/bin/env python3
"""
Test script for the new GUI therapeutic audio integration
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_gui_integration():
    """Test that the GUI integration works correctly"""
    print("🖥️ Testing GUI Integration for 2024 Research Features")
    print("=" * 60)
    
    try:
        # Test imports
        print("Testing imports...")
        from project_name.gui.main import main
        from project_name.gui.panels.therapeutic_panel import TherapeuticAudioPanel
        from project_name.audio_engine.therapeutic_engine_2024 import TherapeuticAudioMixer
        print("✓ All imports successful")
        
        # Test engine initialization
        print("Testing audio engine initialization...")
        mixer = TherapeuticAudioMixer(sample_rate=44100)
        print("✓ Audio engine initialized successfully")
        
        print("\n🎉 GUI integration test passed!")
        print("\nTo launch the GUI with the new therapeutic features:")
        print("1. Run: python -m project_name.gui.main")
        print("2. Click on '🧠 Therapeutic Audio' in the sidebar")
        print("3. Explore the research-based features:")
        print("   • Sleep Enhancement (0.25 Hz, 3 Hz, dynamic protocols)")
        print("   • Anxiety Relief (HRV optimization)")
        print("   • Focus Enhancement (pink noise superiority)")
        print("   • Personalized Audio (individual preferences)")
        print("   • Advanced Settings (batch generation)")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install numpy scipy soundfile tkinter")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def launch_gui():
    """Launch the GUI directly"""
    print("🚀 Launching SonicSleep Pro with 2024 Research Features...")
    
    try:
        from project_name.gui.main import main
        main()
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        print("Try running: python -m project_name.gui.main")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test and launch GUI with 2024 research features")
    parser.add_argument("--test", action="store_true", help="Run tests only")
    parser.add_argument("--launch", action="store_true", help="Launch GUI directly")
    
    args = parser.parse_args()
    
    if args.test:
        success = test_gui_integration()
        sys.exit(0 if success else 1)
    elif args.launch:
        launch_gui()
    else:
        # Default: test first, then ask about launching
        if test_gui_integration():
            response = input("\nWould you like to launch the GUI now? (y/n): ")
            if response.lower() in ['y', 'yes']:
                launch_gui()
        else:
            sys.exit(1)
