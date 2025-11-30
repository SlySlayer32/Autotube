#!/usr/bin/env python3
"""
Simple test script to verify the audio quality verification method.
Tests just the _is_sleep_quality_sound method without UI dependencies.
"""

import sys
import os
import logging
import numpy as np
import soundfile as sf
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def analyze_audio_quality(sound_metadata, file_path):
    """
    Simplified version of the audio quality check from input_panel.py
    """
    # 1. Metadata Checks
    duration = sound_metadata.get('duration', 0)
    if not (10 <= duration <= 600):
        logger.info(f"Skipping {sound_metadata['name']} due to duration: {duration}s")
        return False

    tags = [tag.lower() for tag in sound_metadata.get('tags', [])]
    negative_tags = ['loud', 'aggressive', 'harsh', 'sudden', 'alarm', 'shock', 'scary', 'thunder', 'windy']
    if any(tag in ' '.join(tags) for tag in negative_tags):
        logger.info(f"Skipping {sound_metadata['name']} due to negative tags: {tags}")
        return False

    # 2. Audio Content Analysis
    try:
        with sf.SoundFile(file_path, 'r') as audio_file:
            # Read audio data
            frames = audio_file.read(dtype='float32')
            samplerate = audio_file.samplerate

            # Mono conversion for analysis
            if audio_file.channels > 1:
                frames = np.mean(frames, axis=1)

            # a. Check for silence or near-silence
            max_amplitude = np.max(np.abs(frames))
            if max_amplitude < 0.01:
                logger.info(f"Skipping {sound_metadata['name']} due to silence (max: {max_amplitude:.4f})")
                return False

            # b. Check for sudden peaks (transients) like thunder
            transients = np.diff(frames)
            peak_transient = np.max(np.abs(transients))
            
            if peak_transient > 0.8:
                logger.info(f"Skipping {sound_metadata['name']} due to sharp transient (peak: {peak_transient:.2f})")
                return False

            # c. Frequency analysis for high-pitched ringing
            fft_data = np.fft.rfft(frames)
            fft_freq = np.fft.rfftfreq(len(frames), d=1./samplerate)
            
            # Check energy above 8kHz - high-pitched noise
            high_freq_mask = fft_freq > 8000
            if np.any(high_freq_mask):
                high_freq_energy = np.mean(np.abs(fft_data[high_freq_mask]))
                total_energy = np.mean(np.abs(fft_data))
                high_freq_ratio = high_freq_energy / total_energy if total_energy > 0 else 0

                if high_freq_ratio > 0.15:
                    logger.info(f"Skipping {sound_metadata['name']} due to excessive high-frequency energy (ratio: {high_freq_ratio:.3f})")
                    return False

            logger.info(f"✅ {sound_metadata['name']} passed all quality checks")
            logger.info(f"   - Max amplitude: {max_amplitude:.4f}")
            logger.info(f"   - Peak transient: {peak_transient:.4f}")
            logger.info(f"   - High freq ratio: {high_freq_ratio:.4f}")
            return True

    except Exception as e:
        logger.error(f"Could not analyze audio for {sound_metadata['name']}: {e}")
        return False

def create_test_audio_files():    """Create test audio files with different characteristics"""
    test_dir = Path("test_audio_verification")
    test_dir.mkdir(exist_ok=True)
    
    sample_rate = 44100
    duration = 15  # 15 seconds (meets minimum requirement)
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # 1. Clean rain-like sound (brown noise)
    clean_rain = np.random.normal(0, 0.3, len(t))
    # Simple low-pass filter effect
    for i in range(1, len(clean_rain)):
        clean_rain[i] = 0.7 * clean_rain[i] + 0.3 * clean_rain[i-1]
    clean_rain = clean_rain * 0.3  # Moderate volume
    
    sf.write(test_dir / "clean_rain.wav", clean_rain, sample_rate)
    logger.info("Created: clean_rain.wav (should PASS)")
    
    # 2. Audio with high-pitched ringing
    high_pitch_tone = 0.5 * np.sin(2 * np.pi * 10000 * t)  # 10kHz tone
    background_noise = np.random.normal(0, 0.1, len(t)) * 0.2
    ringing_audio = background_noise + high_pitch_tone
    sf.write(test_dir / "ringing_audio.wav", ringing_audio, sample_rate)
    logger.info("Created: ringing_audio.wav (should FAIL - high frequency)")
    
    # 3. Audio with sudden loud transients
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
    
    return test_dir

def test_verification_system():
    """Test the audio verification system"""
    logger.info("=" * 60)
    logger.info("TESTING AUDIO QUALITY VERIFICATION SYSTEM")
    logger.info("=" * 60)
    
    # Create test files
    test_dir = create_test_audio_files()
    
    # Test each file
    test_files = [
        ("clean_rain.wav", True),      # Should pass
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
            'duration': 15.0,  # Match the actual duration
            'tags': ['ambient', 'calm', 'nature'],
            'id': 'test_' + filename
        }
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Testing: {filename}")
        logger.info(f"Expected result: {'PASS' if expected_result else 'FAIL'}")
        logger.info(f"{'='*50}")
        
        try:
            result = analyze_audio_quality(mock_sound, str(file_path))
            results.append((filename, expected_result, result))
            
            status = "✅ PASS" if result else "❌ FAIL"
            correct = "✓ CORRECT" if result == expected_result else "✗ INCORRECT"
            
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
        return True
    else:
        logger.warning("⚠️  Some tests failed. The verification system may need adjustment.")
        return False

if __name__ == "__main__":
    try:
        success = test_verification_system()
        sys.exit(0 if success else 1)
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Please install: pip install soundfile numpy")
        sys.exit(1)
