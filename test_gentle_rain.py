#!/usr/bin/env python3
"""
Test the verification system on the actual gentle_rain.wav file
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
    Audio quality check from input_panel.py
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
            high_freq_energy = np.mean(np.abs(fft_data[fft_freq > 8000]))
            total_energy = np.mean(np.abs(fft_data))
            high_freq_ratio = high_freq_energy / total_energy if total_energy > 0 else 0

            # Also check for dominant single frequencies (like sine waves)
            # Find peaks in frequency spectrum
            fft_magnitude = np.abs(fft_data)
            max_freq_peak = np.max(fft_magnitude)
            mean_freq_energy = np.mean(fft_magnitude)
            peak_ratio = max_freq_peak / mean_freq_energy if mean_freq_energy > 0 else 0

            logger.info(f"Audio analysis for {sound_metadata['name']}:")
            logger.info(f"   - Max amplitude: {max_amplitude:.4f}")
            logger.info(f"   - Peak transient: {peak_transient:.4f}")
            logger.info(f"   - High freq ratio (>8kHz): {high_freq_ratio:.4f}")
            logger.info(f"   - Peak frequency ratio: {peak_ratio:.2f}")

            if high_freq_ratio > 0.4:
                logger.info(f"❌ Rejecting due to excessive high-frequency energy")
                return False
                
            # Check for dominant single frequencies (like pure tones)
            if peak_ratio > 100:  # Very dominant single frequency
                logger.info(f"❌ Rejecting due to dominant single frequency (likely sine wave)")
                return False

            logger.info(f"✅ {sound_metadata['name']} passed all quality checks")
            return True

    except Exception as e:
        logger.error(f"Could not analyze audio for {sound_metadata['name']}: {e}")
        return False

def main():
    """Test on actual gentle_rain.wav file"""
    logger.info("Testing Audio Verification on gentle_rain.wav")
    logger.info("=" * 60)
    
    file_path = Path("test_sounds/gentle_rain.wav")
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return False
    
    # Get actual file info
    with sf.SoundFile(file_path, 'r') as audio_file:
        duration = len(audio_file) / audio_file.samplerate
        channels = audio_file.channels
        samplerate = audio_file.samplerate
    
    logger.info(f"File info: {duration:.1f}s, {channels} channels, {samplerate}Hz")
      # Mock sound metadata with longer duration to test audio analysis
    mock_sound = {
        'name': 'gentle_rain',
        'duration': 15.0,  # Override to test audio content
        'tags': ['rain', 'nature', 'ambient'],
        'id': 'test_gentle_rain'
    }
    
    result = analyze_audio_quality(mock_sound, str(file_path))
    
    logger.info("\n" + "=" * 60)
    if result:
        logger.info("✅ VERDICT: gentle_rain.wav PASSED verification")
        logger.info("This file would be accepted by the automated collection system")
    else:
        logger.info("❌ VERDICT: gentle_rain.wav FAILED verification")
        logger.info("This file would be rejected by the automated collection system")
        logger.info("This explains why you heard high-pitched ringing!")
    
    return result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
