#!/usr/bin/env python3
"""
Simple test of audio preview functionality
"""

import os
import sys
import time

# Add the project directory to path
sys.path.insert(0, os.path.abspath('.'))

def test_audio_preview():
    """Test audio preview methods independently"""
    
    # Test pygame audio playback
    try:
        import pygame
        pygame.mixer.init()
        
        demo_file = os.path.join("demo_mixes", "focus_session.wav")
        if os.path.exists(demo_file):
            print(f"Testing audio playback of {demo_file}...")
            
            pygame.mixer.music.load(demo_file)
            pygame.mixer.music.play()
            
            print("Audio should be playing now for 3 seconds...")
            time.sleep(3)
            
            pygame.mixer.music.stop()
            print("Audio stopped.")
            
            return True
            
    except Exception as e:
        print(f"Error testing audio: {e}")
        return False

    return False

if __name__ == "__main__":
    success = test_audio_preview()
    print(f"Audio test {'passed' if success else 'failed'}")
