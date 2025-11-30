#!/usr/bin/env python3
"""
Test script to verify audio preview functionality
"""

import os
import sys
import tkinter as tk

# Test if pygame is available
try:
    import pygame
    pygame.mixer.init()
    print("✓ Pygame is available and initialized")
    PYGAME_AVAILABLE = True
except ImportError:
    print("✗ Pygame is not available")
    PYGAME_AVAILABLE = False
except Exception as e:
    print(f"✗ Pygame initialization failed: {e}")
    PYGAME_AVAILABLE = False

# Test if winsound is available
try:
    import winsound
    print("✓ Winsound is available")
    WINSOUND_AVAILABLE = True
except ImportError:
    print("✗ Winsound is not available")
    WINSOUND_AVAILABLE = False

# Check for demo files
demo_dir = "demo_mixes"
if os.path.exists(demo_dir):
    demo_files = [f for f in os.listdir(demo_dir) if f.endswith(('.wav', '.mp3'))]
    print(f"✓ Found {len(demo_files)} demo audio files:")
    for file in demo_files:
        print(f"  - {file}")
else:
    print("✗ Demo directory not found")

# Test audio playback with pygame
if PYGAME_AVAILABLE and demo_files:
    test_file = os.path.join(demo_dir, demo_files[0])
    print(f"\nTesting audio playback with {test_file}...")
    
    try:
        pygame.mixer.music.load(test_file)
        print("✓ Audio file loaded successfully")
        print("  (You can run pygame.mixer.music.play() to test playback)")
    except Exception as e:
        print(f"✗ Failed to load audio file: {e}")

print("\n=== Audio Preview Test Summary ===")
print(f"Pygame available: {PYGAME_AVAILABLE}")
print(f"Winsound available: {WINSOUND_AVAILABLE}")
print(f"Demo files available: {len(demo_files) if 'demo_files' in locals() else 0}")

if PYGAME_AVAILABLE and demo_files:
    print("✓ Audio preview should work!")
elif WINSOUND_AVAILABLE and any(f.endswith('.wav') for f in demo_files):
    print("⚠ Limited audio preview available (WAV files only)")
else:
    print("✗ Audio preview may have issues")
