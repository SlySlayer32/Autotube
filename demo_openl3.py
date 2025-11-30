#!/usr/bin/env python3
"""
Demo script for OpenL3 Audio Similarity Matching

This script demonstrates the audio similarity matching capabilities
using OpenL3 embeddings integrated into the project.
"""

import sys
import os
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import with version control
from python_version_control import check_python_version
check_python_version()

from project_name.core.processor import SoundProcessor
from project_name.core.audio_similarity import create_similarity_matcher


def demo_similarity_matching():
    """Demonstrate audio similarity matching functionality."""
    print("🎵 OpenL3 Audio Similarity Matching Demo")
    print("=" * 50)
    
    # Test OpenL3 availability
    try:
        import openl3
        import soundfile as sf
        print(f"✅ OpenL3 version: {openl3.__version__}")
        print(f"✅ SoundFile available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("🔧 Run: pip install openl3 soundfile")
        return False
    
    # Test similarity matcher creation
    try:
        print("\n📦 Creating similarity matcher...")
        matcher = create_similarity_matcher(content_type="env")
        print("✅ Similarity matcher created successfully")
        
        # Get cache stats
        stats = matcher.get_cache_stats()
        print(f"   - Embedding size: {stats['embedding_size']}")
        print(f"   - Memory usage: {stats['memory_usage_mb']:.2f} MB")
        
    except Exception as e:
        print(f"❌ Failed to create similarity matcher: {e}")
        return False
    
    # Test SoundProcessor integration
    try:
        print("\n🔧 Testing SoundProcessor integration...")
        processor = SoundProcessor()
        
        if processor.similarity_matcher:
            print("✅ SoundProcessor has similarity matching enabled")
        else:
            print("❌ SoundProcessor similarity matching not available")
            return False
            
    except Exception as e:
        print(f"❌ SoundProcessor integration failed: {e}")
        return False
    
    # Check for audio files to test with
    print("\n🎧 Checking for audio files...")
    input_folder = Path("input_clips")
    
    if input_folder.exists():
        audio_files = list(input_folder.glob("*.wav")) + list(input_folder.glob("*.mp3"))
        print(f"   Found {len(audio_files)} audio files in {input_folder}")
        
        if len(audio_files) >= 2:
            print("\n🔍 Testing similarity matching with real files...")
            try:
                # Test with first two files
                query_file = str(audio_files[0])
                candidate_files = [str(f) for f in audio_files[1:6]]  # Up to 5 candidates
                
                print(f"   Query file: {Path(query_file).name}")
                print(f"   Candidates: {[Path(f).name for f in candidate_files]}")
                
                # Find similar clips
                similar_clips = matcher.find_similar_clips(query_file, candidate_files, top_k=3)
                
                print(f"\n   📊 Most similar clips:")
                for i, (file_path, similarity) in enumerate(similar_clips, 1):
                    print(f"   {i}. {Path(file_path).name} (similarity: {similarity:.3f})")
                
                print("✅ Similarity matching test successful!")
                
            except Exception as e:
                print(f"❌ Similarity matching test failed: {e}")
                return False
        else:
            print("   ℹ️  Need at least 2 audio files for similarity testing")
    else:
        print(f"   ℹ️  No {input_folder} directory found")
    
    print("\n🎉 OpenL3 integration demo completed successfully!")
    return True


def demo_batch_processing():
    """Demonstrate batch embedding extraction."""
    print("\n🚀 Batch Processing Demo")
    print("-" * 30)
    
    try:
        processor = SoundProcessor()
        
        if not processor.similarity_matcher:
            print("❌ Similarity matching not available")
            return False
        
        # Load existing cache if available
        cache_loaded = processor.load_embeddings_cache()
        if cache_loaded:
            print("✅ Loaded existing embeddings cache")
        else:
            print("ℹ️  No existing embeddings cache found")
        
        # Check if we have categorized files
        total_files = sum(len(files) for files in processor.categories.values())
        print(f"📂 Total categorized files: {total_files}")
        
        if total_files > 0:
            print("🔄 Precomputing embeddings for all files...")
            processor.precompute_embeddings(save_cache=True)
            
            # Show updated stats
            stats = processor.similarity_matcher.get_cache_stats()
            print(f"   ✅ Cached embeddings: {stats['cached_files']}")
            print(f"   💾 Memory usage: {stats['memory_usage_mb']:.2f} MB")
        else:
            print("ℹ️  No categorized files found. Run audio processing first.")
        
        return True
        
    except Exception as e:
        print(f"❌ Batch processing demo failed: {e}")
        return False


def main():
    """Run the OpenL3 integration demo."""
    print("🔍 OpenL3 Audio Similarity Integration Demo")
    print("🎯 This demo tests the OpenL3 integration in your audio processing project")
    print()
    
    # Run basic demo
    success = demo_similarity_matching()
    
    if success:
        # Run batch processing demo
        demo_batch_processing()
        
        print("\n" + "=" * 60)
        print("🎊 Demo completed successfully!")
        print()
        print("🚀 Next steps:")
        print("   1. Add more audio files to input_clips/")
        print("   2. Run audio categorization: python cli.py")
        print("   3. Use similarity matching in your mixes")
        print("   4. Implement recommendation features")
        print()
        print("📖 Documentation:")
        print("   - Audio similarity: project_name/core/audio_similarity.py")
        print("   - Integration tests: tests/test_audio_similarity.py")
        
    else:
        print("\n❌ Demo failed. Check the error messages above.")
        print("🔧 Try running the setup script: setup_python311.ps1")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
