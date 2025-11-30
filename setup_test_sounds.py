#!/usr/bin/env python3
"""
Download and Organize Test Sounds

This script downloads specific therapeutic sounds for each category 
to create a proper test library for verifying collection functionality.
"""

import sys
import os
import logging
from pathlib import Path
import shutil

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_name.api.freesound_api import FreesoundAPI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_category_test_sounds():
    """Download specific test sounds for each therapeutic category."""
    print("🎵 Downloading Category-Specific Test Sounds")
    print("=" * 60)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    api = FreesoundAPI(api_key)
    
    # Create directories
    test_sounds_dir = Path("test_sounds")
    test_audio_verification_dir = Path("test_audio_verification")
    test_sounds_dir.mkdir(exist_ok=True)
    test_audio_verification_dir.mkdir(exist_ok=True)
    
    # Define specific sounds to look for in each category
    target_sounds = {
        "gentle_rain": {
            "search_terms": [
                '+rain +gentle +roof -storm -thunder',
                '+rain +soft +peaceful -metal -harsh',
                '+"light rain" +ambient -storm'
            ],
            "description": "Gentle, soft rain sounds suitable for sleep",
            "filename_prefix": "gentle_rain"
        },
        "ocean_waves": {
            "search_terms": [
                '+ocean +waves +calm +peaceful -storm -wind',
                '+sea +gentle +beach -surf -rough',
                '+waves +lapping +quiet -crashing'
            ],
            "description": "Calm ocean waves and gentle water sounds",
            "filename_prefix": "ocean_waves"
        },
        "nature_ambience": {
            "search_terms": [
                '+nature +forest +peaceful -birds -animals',
                '+woodland +ambient +calm -wind -rustling',
                '+nature +atmosphere +quiet -loud'
            ],
            "description": "Peaceful nature ambiences without distracting elements",
            "filename_prefix": "nature_ambience"
        },
        "ambient_peaceful": {
            "search_terms": [
                '+ambient +meditation +peaceful -music -electronic',
                '+atmosphere +calm +relaxation -beat -rhythm',
                '+ambient +sleep +gentle -synth -digital'
            ],
            "description": "Ambient atmospheric sounds for meditation and sleep",
            "filename_prefix": "ambient_peaceful"
        },
        "white_noise": {
            "search_terms": [
                '+"white noise" +sleep +gentle -harsh',
                '+"pink noise" +calm +steady -loud',
                '+noise +constant +peaceful -aggressive'
            ],
            "description": "Gentle white/pink noise for sleep and focus",
            "filename_prefix": "white_noise"
        }
    }
    
    downloaded_sounds = {}
    
    for category, config in target_sounds.items():
        print(f"\n🎯 Searching for {category} sounds...")
        print(f"   {config['description']}")
        
        category_sounds = []
        
        for search_term in config['search_terms']:
            try:
                print(f"   🔍 Searching: {search_term}")
                results = api.search(
                    query=search_term,
                    duration_range=(30, 300),  # 30 seconds to 5 minutes
                    rating_min=3.5,
                    downloads_min=10,
                    page_size=5
                )
                
                if results.get('results'):
                    for sound in results['results'][:2]:  # Top 2 from each search
                        sound_info = {
                            'id': sound['id'],
                            'name': sound['name'],
                            'duration': sound.get('duration', 0),
                            'rating': sound.get('avg_rating', 0),
                            'tags': sound.get('tags', []),
                            'category': category
                        }
                        category_sounds.append(sound_info)
                        print(f"      ✓ Found: {sound['name']} ({sound.get('duration', 0):.1f}s, {sound.get('avg_rating', 0):.1f}★)")
                        
                        if len(category_sounds) >= 3:  # Limit per category
                            break
                    
                if len(category_sounds) >= 3:
                    break
                    
            except Exception as e:
                print(f"      ❌ Search failed: {e}")
                continue
        
        downloaded_sounds[category] = category_sounds
        print(f"   📊 Found {len(category_sounds)} {category} sounds")
    
    return downloaded_sounds


def create_test_sound_files(downloaded_sounds):
    """Create organized test sound files in both directories."""
    print(f"\n📁 Organizing Test Sounds")
    print("=" * 60)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    api = FreesoundAPI(api_key)
    
    # Create category subdirectories
    categories = ["gentle_rain", "ocean_waves", "nature_ambience", "ambient_peaceful", "white_noise"]
    
    for base_dir in [Path("test_sounds"), Path("test_audio_verification")]:
        for category in categories:
            (base_dir / category).mkdir(exist_ok=True)
    
    total_downloaded = 0
    
    for category, sounds in downloaded_sounds.items():
        print(f"\n🎵 Processing {category} sounds:")
        
        for i, sound_info in enumerate(sounds, 1):
            try:
                print(f"   📥 Downloading: {sound_info['name']}")
                
                # Download the sound
                downloaded_file = api.download(sound_info['id'])
                
                if downloaded_file and os.path.exists(downloaded_file):
                    # Create descriptive filename
                    safe_name = "".join(c for c in sound_info['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
                    safe_name = safe_name.replace(' ', '_')[:50]  # Limit length
                    
                    new_filename = f"{category}_{i:02d}_{safe_name}.wav"
                    
                    # Copy to both test directories
                    for base_dir in [Path("test_sounds"), Path("test_audio_verification")]:
                        target_dir = base_dir / category
                        target_file = target_dir / new_filename
                        
                        shutil.copy2(downloaded_file, target_file)
                        print(f"      ✓ Saved: {target_file}")
                    
                    # Clean up original download
                    os.remove(downloaded_file)
                    total_downloaded += 1
                    
                    # Create metadata file
                    metadata = {
                        'freesound_id': sound_info['id'],
                        'original_name': sound_info['name'],
                        'duration': sound_info['duration'],
                        'rating': sound_info['rating'],
                        'tags': sound_info['tags'],
                        'category': category,
                        'filename': new_filename
                    }
                    
                    # Save metadata
                    metadata_file = Path("test_sounds") / category / f"{new_filename}.json"
                    import json
                    with open(metadata_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                else:
                    print(f"      ❌ Download failed for {sound_info['name']}")
                    
            except Exception as e:
                print(f"      ❌ Error processing {sound_info['name']}: {e}")
                continue
    
    print(f"\n🎉 Successfully downloaded and organized {total_downloaded} test sounds!")
    return total_downloaded


def create_test_manifest():
    """Create a manifest file describing all test sounds."""
    print(f"\n📋 Creating Test Sound Manifest")
    print("=" * 60)
    
    manifest = {
        "test_sound_categories": {
            "gentle_rain": {
                "description": "Soft, gentle rain sounds without thunder or storms",
                "use_case": "Sleep sounds, Rain & Water collections",
                "expected_tags": ["rain", "gentle", "soft", "peaceful", "ambient"],
                "avoid_tags": ["thunder", "storm", "metal", "harsh"]
            },
            "ocean_waves": {
                "description": "Calm ocean waves and gentle water sounds",
                "use_case": "Sleep sounds, Rain & Water collections",
                "expected_tags": ["ocean", "waves", "calm", "peaceful", "water"],
                "avoid_tags": ["storm", "surf", "rough", "wind"]
            },
            "nature_ambience": {
                "description": "Peaceful nature atmospheres without animal sounds",
                "use_case": "Sleep sounds, Nature Ambience collections",
                "expected_tags": ["nature", "forest", "ambient", "peaceful", "atmosphere"],
                "avoid_tags": ["birds", "animals", "wind", "rustling"]
            },
            "ambient_peaceful": {
                "description": "Atmospheric ambient sounds for meditation",
                "use_case": "Sleep sounds, Nature Ambience collections",
                "expected_tags": ["ambient", "meditation", "peaceful", "atmosphere", "calm"],
                "avoid_tags": ["music", "electronic", "beat", "rhythm"]
            },
            "white_noise": {
                "description": "Gentle white/pink noise for sleep and focus",
                "use_case": "White/Pink Noise collections",
                "expected_tags": ["white-noise", "pink-noise", "sleep", "constant"],
                "avoid_tags": ["harsh", "loud", "sudden", "music"]
            }
        },
        "collection_type_mapping": {
            "Sleep Sounds": ["gentle_rain", "ocean_waves", "nature_ambience", "ambient_peaceful"],
            "Rain & Water": ["gentle_rain", "ocean_waves"],
            "Nature Ambience": ["nature_ambience", "ambient_peaceful"],
            "White/Pink Noise": ["white_noise"],
            "Complete Collection": ["gentle_rain", "ocean_waves", "nature_ambience", "ambient_peaceful", "white_noise"]
        },
        "usage_instructions": {
            "testing_collection_types": "Use these sounds to verify that different collection types download appropriate sounds",
            "audio_verification": "Use these sounds to test the audio verification and preview systems",
            "quality_control": "These sounds represent the quality and type of content users should expect"
        }
    }
    
    # Save manifest
    import json
    with open("test_sounds_manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("✅ Test sound manifest created: test_sounds_manifest.json")
    
    # Create README
    readme_content = """# Test Sounds Directory

This directory contains categorized test sounds for verifying the SonicSleep Pro collection system.

## Directory Structure

```
test_sounds/
├── gentle_rain/          # Soft rain sounds without thunder
├── ocean_waves/          # Calm ocean and water sounds  
├── nature_ambience/      # Peaceful nature atmospheres
├── ambient_peaceful/     # Meditation and ambient sounds
├── white_noise/          # Gentle white/pink noise
└── test_sounds_manifest.json  # Detailed metadata

test_audio_verification/
├── gentle_rain/          # Copy of sounds for verification testing
├── ocean_waves/          
├── nature_ambience/      
├── ambient_peaceful/     
└── white_noise/          
```

## Usage

1. **Collection Type Testing**: Use these sounds to verify that:
   - "Sleep Sounds" downloads from all peaceful categories
   - "Rain & Water" downloads only rain and ocean sounds
   - "Nature Ambience" downloads only nature and ambient sounds
   - "White/Pink Noise" downloads only noise sounds

2. **Audio Verification**: Use the `test_audio_verification/` copies to test:
   - Audio preview functionality
   - Quality verification systems
   - File format compatibility

3. **Quality Control**: These sounds represent the expected quality and style:
   - High ratings (3.5+ stars)
   - Appropriate duration (30-300 seconds)
   - Therapeutic tags and content
   - No harsh or inappropriate elements

## Testing Commands

```bash
# Test collection types
python test_enhanced_integration.py

# Test context-aware search
python test_context_aware_search.py

# Test audio verification
python test_audio_verification_simple.py
```
"""
    
    with open("test_sounds/README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ Test sounds README created: test_sounds/README.md")


def main():
    """Download and organize therapeutic test sounds by category."""
    print("🚀 Test Sound Organizer for SonicSleep Pro")
    print("=" * 80)
    
    try:
        # Step 1: Search and identify appropriate sounds
        downloaded_sounds = download_category_test_sounds()
        
        if not any(downloaded_sounds.values()):
            print("❌ No sounds found. Check API key and network connection.")
            return False
        
        # Step 2: Download and organize the sounds
        total_files = create_test_sound_files(downloaded_sounds)
        
        if total_files == 0:
            print("❌ No files were successfully downloaded.")
            return False
        
        # Step 3: Create documentation
        create_test_manifest()
        
        # Summary
        print("\n" + "=" * 80)
        print("🎉 TEST SOUND SETUP COMPLETE!")
        print(f"✅ Downloaded {total_files} therapeutic test sounds")
        print("✅ Organized into category-specific directories")
        print("✅ Created metadata and documentation")
        print("✅ Ready for collection type testing")
        
        print("\n📁 Directory Structure:")
        for category in ["gentle_rain", "ocean_waves", "nature_ambience", "ambient_peaceful", "white_noise"]:
            test_dir = Path("test_sounds") / category
            if test_dir.exists():
                file_count = len(list(test_dir.glob("*.wav")))
                print(f"   {category}/: {file_count} sound files")
        
        print("\n🧪 Next Steps:")
        print("1. Test collection types in the GUI to verify correct categorization")
        print("2. Use these sounds for audio verification testing")
        print("3. Validate that different collection types download appropriate sounds")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in test sound setup: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
