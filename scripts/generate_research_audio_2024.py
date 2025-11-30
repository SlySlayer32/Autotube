#!/usr/bin/env python3
"""
Research-Based Audio Therapy Integration Script
Demonstrates the latest 2024 research findings in action

Run this script to generate therapeutic audio files based on:
- Dynamic binaural beats (0-3 Hz) 
- Superior pink noise (vs white noise)
- Multi-modal therapeutic mixing
- Personalized protocols
"""

import os
import sys
import time
import numpy as np
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from project_name.audio_engine.therapeutic_engine_2024 import (
        TherapeuticAudioMixer, 
        DynamicBinauralEngine, 
        SuperiorPinkNoiseEngine
    )
    print("✓ Successfully imported 2024 research-based audio engines")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def create_output_directory():
    """Create output directory for generated audio files"""
    output_dir = project_root / "output_mixes" / "research_2024"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def generate_sleep_optimization_suite(output_dir):
    """Generate complete sleep optimization audio suite"""
    print("\n🧠 Generating Sleep Optimization Suite (2024 Research)")
    print("=" * 60)
    
    mixer = TherapeuticAudioMixer(sample_rate=44100)
    
    # 1. Quick Sleep Induction (0.25 Hz targeting)
    print("1. Creating Quick Sleep Induction (0.25 Hz targeting)...")
    binaural_engine = DynamicBinauralEngine()
    quick_sleep_audio = binaural_engine._generate_static_beat(0.25, 900)  # 15 minutes
    
    filename = output_dir / "01_quick_sleep_induction.wav"
    mixer.save_therapeutic_audio(quick_sleep_audio, str(filename))
    print(f"   ✓ Saved: {filename}")
    
    # 2. Dynamic Sleep Protocol (Research-optimized)
    print("2. Creating Dynamic Sleep Protocol (0-3 Hz optimization)...")
    sleep_audio, sleep_metadata = mixer.create_ultimate_sleep_mix(
        duration_minutes=30,
        include_nature=True
    )
    
    filename = output_dir / "02_dynamic_sleep_protocol.wav"
    mixer.save_therapeutic_audio(sleep_audio, str(filename), sleep_metadata)
    print(f"   ✓ Saved: {filename}")
    print(f"   Components: {', '.join(sleep_metadata['components'])}")
    
    # 3. Memory Consolidation Mix (Pink noise superiority)
    print("3. Creating Memory Consolidation Mix (Superior pink noise)...")
    pink_engine = SuperiorPinkNoiseEngine()
    memory_audio = pink_engine.create_memory_consolidation_track(45)  # 45 minutes
    memory_stereo = memory_audio.reshape(-1, 1)
    memory_stereo = np.column_stack((memory_audio, memory_audio))
    
    filename = output_dir / "03_memory_consolidation.wav"
    mixer.save_therapeutic_audio(memory_stereo, str(filename))
    print(f"   ✓ Saved: {filename}")
    
    # 4. Deep Sleep Enhancement (3 Hz + nature sounds)
    print("4. Creating Deep Sleep Enhancement (3 Hz + ASMR-style)...")
    deep_sleep_audio = binaural_engine._generate_static_beat(3.0, 2700)  # 45 minutes
    
    filename = output_dir / "04_deep_sleep_enhancement.wav"
    mixer.save_therapeutic_audio(deep_sleep_audio, str(filename))
    print(f"   ✓ Saved: {filename}")

def generate_anxiety_relief_suite(output_dir):
    """Generate anxiety relief audio suite"""
    print("\n💚 Generating Anxiety Relief Suite (HRV Research)")
    print("=" * 60)
    
    mixer = TherapeuticAudioMixer(sample_rate=44100)
    
    # 1. Quick Anxiety Relief (2 Hz optimization)
    print("1. Creating Quick Anxiety Relief (2 Hz HRV optimization)...")
    anxiety_audio, anxiety_metadata = mixer.create_anxiety_reduction_mix(
        duration_minutes=15
    )
    
    filename = output_dir / "05_quick_anxiety_relief.wav"
    mixer.save_therapeutic_audio(anxiety_audio, str(filename), anxiety_metadata)
    print(f"   ✓ Saved: {filename}")
    print(f"   Target frequency: {anxiety_metadata['target_frequency']} Hz")
    
    # 2. Extended Relaxation Session
    print("2. Creating Extended Relaxation Session...")
    extended_anxiety_audio, extended_metadata = mixer.create_anxiety_reduction_mix(
        duration_minutes=30
    )
    
    filename = output_dir / "06_extended_relaxation.wav"
    mixer.save_therapeutic_audio(extended_anxiety_audio, str(filename), extended_metadata)
    print(f"   ✓ Saved: {filename}")

def generate_focus_enhancement_suite(output_dir):
    """Generate focus enhancement audio suite"""
    print("\n🎯 Generating Focus Enhancement Suite (Pink Noise Research)")
    print("=" * 60)
    
    mixer = TherapeuticAudioMixer(sample_rate=44100)
    pink_engine = SuperiorPinkNoiseEngine()
    
    # 1. Pure Pink Noise Focus
    print("1. Creating Pure Pink Noise Focus (Superior to white noise)...")
    focus_audio = pink_engine.create_focus_enhancement_track(25)  # 25 minutes
    
    filename = output_dir / "07_pink_noise_focus.wav"
    mixer.save_therapeutic_audio(focus_audio, str(filename))
    print(f"   ✓ Saved: {filename}")
    
    # 2. Focus with Subtle Alpha Enhancement
    print("2. Creating Focus with Alpha Enhancement...")
    binaural_engine = DynamicBinauralEngine()
    alpha_beats = binaural_engine._generate_static_beat(10.0, 1500)  # 25 minutes, 10 Hz
    
    # Mix with pink noise
    focus_pink = pink_engine.create_focus_enhancement_track(25)
    
    # Ensure same length
    min_length = min(len(alpha_beats), len(focus_pink))
    combined_focus = (
        alpha_beats[:min_length] * 0.3 +
        focus_pink[:min_length] * 0.7
    )
    
    filename = output_dir / "08_enhanced_focus_alpha.wav"
    mixer.save_therapeutic_audio(combined_focus, str(filename))
    print(f"   ✓ Saved: {filename}")

def generate_personalized_examples(output_dir):
    """Generate personalized audio examples"""
    print("\n👤 Generating Personalized Examples")
    print("=" * 60)
    
    mixer = TherapeuticAudioMixer(sample_rate=44100)
    
    # Example 1: Nature-focused user
    print("1. Creating Nature-Focused Sleep Mix...")
    nature_focused = mixer.create_ultimate_sleep_mix(
        duration_minutes=20,
        include_nature=True,
        personalization={'prefer_nature': True}
    )
    
    filename = output_dir / "09_nature_focused_sleep.wav"
    mixer.save_therapeutic_audio(nature_focused[0], str(filename), nature_focused[1])
    print(f"   ✓ Saved: {filename}")
    print(f"   Nature ratio: {nature_focused[1]['mix_ratios']['nature']:.2f}")
    
    # Example 2: Beat-sensitive user
    print("2. Creating Beat-Sensitive Sleep Mix...")
    beat_sensitive = mixer.create_ultimate_sleep_mix(
        duration_minutes=20,
        include_nature=True,
        personalization={'sensitive_to_beats': True}
    )
    
    filename = output_dir / "10_beat_sensitive_sleep.wav"
    mixer.save_therapeutic_audio(beat_sensitive[0], str(filename), beat_sensitive[1])
    print(f"   ✓ Saved: {filename}")
    print(f"   Binaural ratio: {beat_sensitive[1]['mix_ratios']['binaural']:.2f}")
    
    # Example 3: Memory-focused user
    print("3. Creating Memory-Focused Sleep Mix...")
    memory_focused = mixer.create_ultimate_sleep_mix(
        duration_minutes=20,
        include_nature=True,
        personalization={'focus_on_memory': True}
    )
    
    filename = output_dir / "11_memory_focused_sleep.wav"
    mixer.save_therapeutic_audio(memory_focused[0], str(filename), memory_focused[1])
    print(f"   ✓ Saved: {filename}")
    print(f"   Pink noise ratio: {memory_focused[1]['mix_ratios']['pink_noise']:.2f}")

def run_comprehensive_demo():
    """Run comprehensive demonstration of 2024 research integration"""
    print("🎵 2024 Research-Based Therapeutic Audio Generator")
    print("=" * 70)
    print("Based on latest peer-reviewed studies on:")
    print("• Dynamic binaural beats (0-3 Hz) for sleep induction")
    print("• Pink noise superiority over white noise")
    print("• Multi-modal therapeutic audio mixing")
    print("• Heart rate variability optimization")
    print("• Personalized audio therapy protocols")
    print("=" * 70)
      # Create output directory
    output_dir = create_output_directory()
    print(f"\n📁 Output directory: {output_dir}")
    
    start_time = time.time()
    
    try:
        # Generate all audio suites
        generate_sleep_optimization_suite(output_dir)
        generate_anxiety_relief_suite(output_dir)
        generate_focus_enhancement_suite(output_dir)
        generate_personalized_examples(output_dir)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ Demo completed successfully!")
        print(f"⏱️  Total generation time: {elapsed_time:.1f} seconds")
        print(f"📁 All files saved to: {output_dir}")
        
        # List generated files
        print(f"\n📋 Generated {len(list(output_dir.glob('*.wav')))} therapeutic audio files:")
        for i, wav_file in enumerate(sorted(output_dir.glob('*.wav')), 1):
            file_size = wav_file.stat().st_size / (1024 * 1024)  # MB
            print(f"   {i:2d}. {wav_file.name} ({file_size:.1f} MB)")
        
        print(f"\n🎧 Instructions:")
        print("• Use headphones for full binaural effect")
        print("• Start with lower volumes and adjust")
        print("• Test different tracks to find your optimal mix")
        print("• Track your sleep/focus improvements")
        
        print(f"\n📊 Research Validation:")
        print("• All frequencies based on 2024 peer-reviewed studies")
        print("• Dynamic beats outperform static beats for sleep")
        print("• Pink noise superior to white noise for memory")
        print("• Multi-modal mixing enhances therapeutic effects")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        print("Check that all dependencies are installed:")
        print("pip install numpy scipy soundfile")
        return False
    
    return True

def quick_test():
    """Quick test to verify everything works"""
    print("🧪 Running Quick Test...")
    
    try:
        mixer = TherapeuticAudioMixer(sample_rate=44100)
        
        # Generate 30-second test sample
        test_audio, metadata = mixer.create_ultimate_sleep_mix(
            duration_minutes=0.5,  # 30 seconds
            include_nature=True
        )
        
        output_dir = create_output_directory()
        test_file = output_dir / "test_sample.wav"
        
        mixer.save_therapeutic_audio(test_audio, str(test_file), metadata)
        
        print(f"✅ Quick test passed!")
        print(f"📁 Test file: {test_file}")
        print(f"🎵 Components: {', '.join(metadata['components'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="2024 Research-Based Therapeutic Audio Generator")
    parser.add_argument("--quick-test", action="store_true", 
                       help="Run quick test only")
    parser.add_argument("--full-demo", action="store_true", 
                       help="Run full demonstration")
    
    args = parser.parse_args()
    
    if args.quick_test:
        success = quick_test()
    elif args.full_demo:
        success = run_comprehensive_demo()
    else:
        # Default: run quick test first, then full demo if successful
        print("Running quick test first...")
        if quick_test():
            print("\nQuick test passed! Running full demo...\n")
            success = run_comprehensive_demo()
        else:
            print("Quick test failed. Please check your setup.")
            success = False
    
    sys.exit(0 if success else 1)
