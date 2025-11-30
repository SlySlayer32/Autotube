"""
Demo: Content Gathering and Intelligent Clipping System

This script demonstrates how to:
1. Generate synthetic binaural beats library
2. Gather content from Freesound (if API key available)
3. Analyze and clip audio files intelligently
4. Build a comprehensive audio library for seamless mixing
"""

import logging
import json
from pathlib import Path

from project_name.core.content_gatherer import ContentGatherer
from project_name.core.intelligent_clipper import IntelligentAudioClipper

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demo_content_gathering():
    """Demonstrate content gathering capabilities."""
    logger.info("🎵 Starting Content Gathering Demo")
    
    # Initialize gatherer
    gatherer = ContentGatherer()
    
    # 1. Generate synthetic binaural beats library
    logger.info("📡 Generating synthetic binaural beats library...")
    gatherer.generate_synthetic_binaural_library()
    
    # 2. If you have a Freesound API key, uncomment this:
    # logger.info("🌐 Gathering content from Freesound...")
    # gatherer.gather_all_content(max_per_category=5)  # Small demo
    
    # 3. Analyze library content
    logger.info("🔍 Analyzing library content...")
    gatherer.analyze_library_content()
    
    logger.info("✅ Content gathering demo complete!")
    
    # Show what we have
    library_path = Path("audio_library")
    if library_path.exists():
        print(f"\n📁 Audio Library Structure:")
        for item in library_path.rglob("*"):
            if item.is_file() and item.suffix == '.wav':
                print(f"  🎵 {item.relative_to(library_path)}")


def demo_intelligent_clipping():
    """Demonstrate intelligent audio clipping."""
    logger.info("✂️ Starting Intelligent Clipping Demo")
    
    # Initialize clipper
    clipper = IntelligentAudioClipper()
    
    # Look for audio files to analyze
    audio_files = []
    
    # Check for existing audio files
    for ext in ['*.wav', '*.mp3', '*.flac']:
        audio_files.extend(Path("input_clips").glob(ext))
        audio_files.extend(Path("audio_library").rglob(ext))
    
    if not audio_files:
        logger.info("⚠️ No audio files found for clipping demo")
        logger.info("💡 Add some audio files to 'input_clips/' folder to test intelligent clipping")
        return
    
    # Analyze first few files
    for i, audio_file in enumerate(audio_files[:3]):  # Analyze first 3 files
        logger.info(f"🔍 Analyzing: {audio_file.name}")
        
        try:
            # Analyze the audio file
            results = clipper.analyze_and_extract_segments(
                str(audio_file),
                output_dir=f"extracted_segments/{audio_file.stem}"
            )
            
            # Display results
            print(f"\n📊 Analysis Results for {audio_file.name}:")
            print(f"  Duration: {results['file_info']['duration']:.1f} seconds")
            print(f"  Content Type: {results['audio_characteristics'].get('content_type', 'unknown')}")
            print(f"  Loops Found: {len(results.get('loop_analysis', []))}")
            print(f"  Segments: {len(results.get('segment_analysis', []))}")
            print(f"  Quality Score: {results['quality_metrics'].get('overall_quality', 0):.2f}")
            
            # Show best loops
            loops = results.get('loop_analysis', [])
            if loops:
                print(f"  🔄 Best Loop: {loops[0]['duration']}s (quality: {loops[0]['quality_metrics']['seamless_score']:.2f})")
            
        except Exception as e:
            logger.error(f"Error analyzing {audio_file}: {e}")
    
    logger.info("✅ Intelligent clipping demo complete!")


def demo_library_organization():
    """Show how the organized library looks."""
    logger.info("📚 Library Organization Demo")
    
    library_path = Path("audio_library")
    
    if not library_path.exists():
        logger.info("⚠️ No library found - run content gathering first")
        return
    
    # Count files by category
    categories = {}
    total_duration = 0
    
    for audio_file in library_path.rglob("*.wav"):
        # Get category from path
        category = str(audio_file.relative_to(library_path).parent)
        if category not in categories:
            categories[category] = {'count': 0, 'duration': 0}
        
        categories[category]['count'] += 1
        
        # Try to get duration from metadata
        metadata_file = audio_file.with_suffix('.json')
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    duration = metadata.get('duration', 0)
                    categories[category]['duration'] += duration
                    total_duration += duration
            except:
                pass
    
    print(f"\n📊 Library Statistics:")
    print(f"  Total Duration: {total_duration/3600:.1f} hours")
    print(f"  Categories:")
    
    for category, stats in categories.items():
        print(f"    🎵 {category}: {stats['count']} files ({stats['duration']/60:.1f} minutes)")


def main():
    """Run all demos."""
    print("🚀 Audio Content System Demo")
    print("=" * 50)
    
    try:
        # Demo 1: Content Gathering
        demo_content_gathering()
        print("\n" + "=" * 50)
        
        # Demo 2: Intelligent Clipping
        demo_intelligent_clipping()
        print("\n" + "=" * 50)
        
        # Demo 3: Library Organization
        demo_library_organization()
        print("\n" + "=" * 50)
        
        print("🎉 All demos completed successfully!")
        
        print("\n💡 Next Steps:")
        print("1. Add a Freesound API key to gather real content")
        print("2. Drop audio files in 'input_clips/' to test clipping")
        print("3. Use the intelligent clipper to build your perfect library")
        print("4. Create seamless, long-duration mixes with the processed content")
        
    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
