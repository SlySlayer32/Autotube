#!/usr/bin/env python3
"""
Test script to verify the audio quality verification system.
This script tests the _is_sleep_quality_sound method with various types of audio files.
"""

import sys
import os
import logging
import numpy as np
import soundfile as sf
from pathlib import Path

# Add project path
sys.path.insert(0, str(Path(__file__).parent / "project_name"))

from project_name.gui.panels.input_panel import InputProcessingPanel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MockPanel:
    """Mock panel for testing"""
    def __init__(self):
        self.content_frame = None

def create_test_audio_files():
    """Create test audio files with different characteristics"""
    test_dir = Path("test_audio_verification")
    test_dir.mkdir(exist_ok=True)
    
    sample_rate = 44100
    duration = 5  # 5 seconds
    
    # 1. Clean rain-like sound (brown noise with some filtering)
    t = np.linspace(0, duration, int(sample_rate * duration))
    clean_rain = np.random.normal(0, 0.1, len(t))
    # Apply low-pass filtering to simulate rain
    from scipy import signal
    try:
        b, a = signal.butter(4, 2000 / (sample_rate / 2), 'low')
        clean_rain = signal.filtfilt(b, a, clean_rain)
        clean_rain = clean_rain * 0.3  # Moderate volume
    except ImportError:
        # Fallback without scipy
        clean_rain = clean_rain * 0.3
    
    sf.write(test_dir / "clean_rain.wav", clean_rain, sample_rate)
    logger.info("Created: clean_rain.wav (should PASS)")
    
    # 2. Audio with high-pitched ringing
    high_pitch_tone = 0.5 * np.sin(2 * np.pi * 10000 * t)  # 10kHz tone
    background_noise = np.random.normal(0, 0.1, len(t)) * 0.2
    ringing_audio = background_noise + high_pitch_tone
    sf.write(test_dir / "ringing_audio.wav", ringing_audio, sample_rate)
    logger.info("Created: ringing_audio.wav (should FAIL - high frequency)")
    
    # 3. Audio with sudden loud transients (like thunder)
    transient_audio = np.random.normal(0, 0.1, len(t)) * 0.2
    # Add sudden spikes
    spike_positions = [int(sample_rate * 1.5), int(sample_rate * 3.2)]
    for pos in spike_positions:
        if pos < len(transient_audio):
            transient_audio[pos:pos+100] = 0.9  # Very loud spike
    
    sf.write(test_dir / "thunder_audio.wav", transient_audio, sample_rate)
    logger.info("Created: thunder_audio.wav (should FAIL - transients)")
    
    # 4. Nearly silent audio
    silent_audio = np.random.normal(0, 0.005, len(t))  # Very quiet
    sf.write(test_dir / "silent_audio.wav", silent_audio, sample_rate)
    logger.info("Created: silent_audio.wav (should FAIL - too quiet)")
    
    # 5. Good quality nature sound (multiple frequencies, no harsh sounds)
    nature_sound = (
        0.3 * np.random.normal(0, 0.1, len(t)) +  # Background
        0.1 * np.sin(2 * np.pi * 200 * t) +       # Low rumble
        0.1 * np.sin(2 * np.pi * 800 * t) * np.random.normal(1, 0.3, len(t))  # Varied mid
    )
    nature_sound = np.clip(nature_sound, -0.8, 0.8)
    sf.write(test_dir / "nature_sound.wav", nature_sound, sample_rate)
    logger.info("Created: nature_sound.wav (should PASS)")
    
    return test_dir

def test_verification_system():
    """Test the audio verification system"""
    logger.info("=" * 60)
    logger.info("TESTING AUDIO QUALITY VERIFICATION SYSTEM")
    logger.info("=" * 60)
    
    # Create test files
    test_dir = create_test_audio_files()
    
    # Create mock objects
    mock_panel = MockPanel()
    input_panel = InputProcessingPanel(mock_panel)
    
    # Test each file
    test_files = [
        ("clean_rain.wav", True),      # Should pass
        ("nature_sound.wav", True),    # Should pass
        ("ringing_audio.wav", False),  # Should fail - high frequency
        ("thunder_audio.wav", False),  # Should fail - transients
        ("silent_audio.wav", False),   # Should fail - too quiet
    ]
    
    results = []
    
    for filename, expected_result in test_files:
        file_path = test_dir / filename
        
        # Mock sound metadata
        mock_sound = {
            'name': filename.replace('.wav', ''),
            'duration': 5.0,
            'tags': ['ambient', 'calm', 'nature'],
            'id': 'test_' + filename
        }
        
        logger.info(f"\nTesting: {filename}")
        logger.info(f"Expected result: {'PASS' if expected_result else 'FAIL'}")
        
        try:
            result = input_panel._is_sleep_quality_sound(mock_sound, str(file_path))
            results.append((filename, expected_result, result))
            
            status = "✅ PASS" if result else "❌ FAIL"
            correct = "✓" if result == expected_result else "✗ INCORRECT"
            
            logger.info(f"Actual result: {status} {correct}")
            
        except Exception as e:
            logger.error(f"Error testing {filename}: {e}")
            results.append((filename, expected_result, None))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    correct_count = 0
    total_count = 0
    
    for filename, expected, actual in results:
        if actual is not None:
            total_count += 1
            if actual == expected:
                correct_count += 1
                status = "✅ CORRECT"
            else:
                status = "❌ INCORRECT"
        else:
            status = "⚠️  ERROR"
        
        logger.info(f"{filename:<20} Expected: {'PASS' if expected else 'FAIL':<4} "
                   f"Got: {'PASS' if actual else 'FAIL' if actual is not None else 'ERR':<4} {status}")
    
    logger.info(f"\nAccuracy: {correct_count}/{total_count} = {correct_count/total_count*100:.1f}%")
    
    if correct_count == total_count:
        logger.info("🎉 ALL TESTS PASSED! The verification system is working correctly.")
    else:
        logger.warning("⚠️  Some tests failed. The verification system may need adjustment.")
    
    return correct_count == total_count

if __name__ == "__main__":
    try:
        success = test_verification_system()
        sys.exit(0 if success else 1)
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Please install: pip install scipy soundfile numpy")
        sys.exit(1)
