#!/usr/bin/env python3
"""
Simple test script to verify 2024 research integration works correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all new modules import correctly"""
    print("Testing imports...")
    
    try:
        from project_name.audio_engine.therapeutic_engine_2024 import (
            TherapeuticAudioMixer, 
            DynamicBinauralEngine, 
            SuperiorPinkNoiseEngine
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of the new engines"""
    print("Testing basic functionality...")
    
    try:
        from project_name.audio_engine.therapeutic_engine_2024 import (
            TherapeuticAudioMixer, 
            DynamicBinauralEngine, 
            SuperiorPinkNoiseEngine
        )
        
        # Test DynamicBinauralEngine
        binaural_engine = DynamicBinauralEngine(sample_rate=44100)
        test_beat, test_pattern = binaural_engine.generate_dynamic_beat(
            center_freq=2.0, 
            freq_range=1.0, 
            duration_seconds=5
        )
        print(f"✓ Dynamic binaural engine: Generated {len(test_beat)} samples")
        
        # Test SuperiorPinkNoiseEngine
        pink_engine = SuperiorPinkNoiseEngine(sample_rate=44100)
        test_pink = pink_engine.generate_research_grade_pink_noise(5)
        print(f"✓ Pink noise engine: Generated {len(test_pink)} samples")
        
        # Test TherapeuticAudioMixer
        mixer = TherapeuticAudioMixer(sample_rate=44100)
        test_mix, test_metadata = mixer.create_ultimate_sleep_mix(
            duration_minutes=0.1,  # 6 seconds
            include_nature=True
        )
        print(f"✓ Therapeutic mixer: Generated {len(test_mix)} samples")
        print(f"  Components: {', '.join(test_metadata['components'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        return False

def test_audio_generation():
    """Test actual audio file generation"""
    print("Testing audio file generation...")
    
    try:
        from project_name.audio_engine.therapeutic_engine_2024 import TherapeuticAudioMixer
        
        mixer = TherapeuticAudioMixer(sample_rate=44100)
        
        # Generate very short test audio
        test_audio, metadata = mixer.create_ultimate_sleep_mix(
            duration_minutes=0.05,  # 3 seconds
            include_nature=True
        )
        
        # Try to save it
        output_dir = project_root / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        test_file = output_dir / "test_audio.wav"
        mixer.save_therapeutic_audio(test_audio, str(test_file), metadata)
        
        if test_file.exists():
            file_size = test_file.stat().st_size
            print(f"✓ Audio generation: Created {test_file.name} ({file_size} bytes)")
            
            # Clean up
            test_file.unlink()
            if output_dir.exists() and not any(output_dir.iterdir()):
                output_dir.rmdir()
            
            return True
        else:
            print("✗ Audio file was not created")
            return False
            
    except Exception as e:
        print(f"✗ Audio generation test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Running 2024 Research Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Functionality Tests", test_basic_functionality),
        ("Audio Generation Tests", test_audio_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*50}")
    print("Test Results Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! 2024 research integration is working correctly.")
        print("\nNext steps:")
        print("1. Run: python scripts/generate_research_audio_2024.py --quick-test")
        print("2. Run: python scripts/generate_research_audio_2024.py --full-demo")
        print("3. Test the generated audio files with headphones")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        print("\nCommon issues:")
        print("• Make sure you have installed: pip install numpy scipy soundfile")
        print("• Verify you're running from the project root directory")
        print("• Check that the project structure is correct")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
