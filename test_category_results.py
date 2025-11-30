#!/usr/bin/env python3
"""
Test Category-Specific Search Results

This script tests what actual sounds each category finds to debug
why different collection types aren't showing different results.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_name.api.freesound_api import FreesoundAPI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_category_differences():
    """Test what each category actually finds to see if they're different."""
    print("🎯 Testing Category-Specific Search Results")
    print("=" * 70)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        api = FreesoundAPI(api_key)
        print("✅ FreesoundAPI initialized successfully")
        
        # Test the therapeutic categories used in collection mapping
        categories_to_test = ["rain", "ocean", "nature", "ambient", "white_noise", "binaural"]
        
        for category in categories_to_test:
            print(f"\n🎵 Testing category: {category}")
            print("-" * 50)
            
            try:
                # Use context-aware search (the default method)
                results = api.search_by_tags_and_filename(
                    category_type=category,
                    max_results=5,  # Just get a few to compare
                    duration_range=(30, 300),
                    quality_filter=True
                )
                
                if results.get('results'):
                    print(f"✅ Found {len(results['results'])} {category} sounds:")
                    
                    for i, sound in enumerate(results['results'], 1):
                        name = sound.get('name', 'Unknown')
                        score = sound.get('therapeutic_score', 0)
                        tags = sound.get('tags', [])[:3]  # First 3 tags
                        duration = sound.get('duration', 0)
                        
                        print(f"   {i}. {name}")
                        print(f"      🎯 Score: {score:.1f} | ⏱️ {duration:.1f}s | 🏷️ {', '.join(tags)}")
                else:
                    print(f"❌ No results found for {category}")
                    
                    # Try a simpler search if context-aware fails
                    simple_results = api.search(
                        query=f"+{category}",
                        duration_range=(30, 300),
                        rating_min=3.0,
                        page_size=3
                    )
                    
                    if simple_results.get('results'):
                        print(f"   📋 Simple search found {len(simple_results['results'])} results:")
                        for sound in simple_results['results']:
                            print(f"      - {sound.get('name', 'Unknown')}")
                    else:
                        print(f"   📋 Even simple search found nothing for {category}")
                    
            except Exception as e:
                print(f"❌ Error testing {category}: {str(e)}")
                continue
        
        print("\n" + "=" * 70)
        print("🔍 Analysis:")
        print("   • If categories show similar results → Search queries overlap")
        print("   • If categories show no results → Filters too restrictive")
        print("   • If rain/ocean return 'ambient' sounds → Need more specific queries")
        
    except Exception as e:
        print(f"❌ API initialization error: {str(e)}")
        return False
    
    return True


def test_collection_type_simulation():
    """Simulate what happens when you select different collection types."""
    print("\n🎪 Simulating Collection Type Selection")
    print("=" * 70)
    
    # Map collection types like the GUI does
    therapeutic_mapping = {
        "Sleep Sounds": ["nature", "rain", "ocean", "ambient"],
        "Rain & Water": ["rain", "ocean"],
        "Nature Ambience": ["nature", "ambient"], 
        "White/Pink Noise": ["white_noise"],
        "Binaural Sources": ["binaural"],
    }
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    api = FreesoundAPI(api_key)
    
    for collection_type, categories in therapeutic_mapping.items():
        print(f"\n📂 Collection Type: {collection_type}")
        print(f"   Categories to search: {categories}")
        print("   Results preview:")
        
        found_any = False
        for category in categories:
            try:
                results = api.search_by_tags_and_filename(
                    category_type=category,
                    max_results=2,  # Just 2 per category
                    duration_range=(30, 300),
                    quality_filter=True
                )
                
                if results.get('results'):
                    found_any = True
                    for sound in results['results']:
                        name = sound.get('name', 'Unknown')[:40]  # Truncate long names
                        score = sound.get('therapeutic_score', 0)
                        print(f"      • [{category}] {name}... (Score: {score:.1f})")
                        
            except Exception as e:
                print(f"      ❌ [{category}] Error: {str(e)}")
                
        if not found_any:
            print("      ⚠️  No results found for any category!")
    
    print("\n" + "=" * 70)
    print("💡 If all collection types show similar results:")
    print("   1. Try 'Empirical Tags' search method instead")
    print("   2. Lower quality filters (rating_min, downloads_min)")
    print("   3. Expand duration range")
    print("   4. Use different search queries")


def main():
    """Run comprehensive category testing."""
    print("🚀 Collection Type & Category Testing Suite")
    print("=" * 80)
    
    test_category_differences()
    test_collection_type_simulation()
    
    print("\n" + "=" * 80)
    print("✅ Testing complete!")
    print("🎯 Check the results above to see if categories are returning different sounds")


if __name__ == "__main__":
    main()
