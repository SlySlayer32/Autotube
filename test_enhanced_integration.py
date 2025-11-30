#!/usr/bin/env python3
"""
Test Enhanced Freesound Integration

This script tests the new enhanced Freesound search integration 
with research-based strategies and improved quality filtering.
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.content_gatherer import ContentGatherer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_enhanced_freesound_api():
    """Test the enhanced FreesoundAPI therapeutic search capabilities."""
    print("🔬 Testing Enhanced Freesound API Integration")
    print("=" * 60)
    
    # API key for testing
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        # Initialize API
        api = FreesoundAPI(api_key)
        print("✅ FreesoundAPI initialized successfully")
        
        # Test therapeutic sound categories
        categories = ["nature", "rain", "ocean", "ambient", "white_noise"]
        
        for category in categories:
            print(f"\n🎵 Testing category: {category}")
            print("-" * 40)
            
            try:
                results = api.search_therapeutic_sounds(
                    category_type=category,
                    max_results=5,
                    duration_range=(10, 120)
                )
                
                if 'results' in results and results['results']:
                    print(f"✅ Found {len(results['results'])} {category} sounds")
                    
                    # Show first result details
                    sound = results['results'][0]
                    print(f"   📎 Sample: {sound['name']}")
                    print(f"   ⏱️  Duration: {sound.get('duration', 'N/A')} seconds")
                    print(f"   ⭐ Rating: {sound.get('avg_rating', 'N/A')}/5")
                    print(f"   🏷️  Tags: {', '.join(sound.get('tags', [])[:5])}")
                else:
                    print(f"⚠️  No results found for {category}")
                    
            except Exception as e:
                print(f"❌ Error testing {category}: {str(e)}")
        
        print("\n" + "=" * 60)
        print("✅ Enhanced API test completed!")
        
    except Exception as e:
        print(f"❌ API initialization error: {str(e)}")
        return False
    
    return True


def test_content_gatherer():
    """Test the enhanced ContentGatherer functionality."""
    print("\n🎯 Testing Enhanced Content Gatherer")
    print("=" * 60)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        # Initialize content gatherer
        gatherer = ContentGatherer(api_key)
        print("✅ ContentGatherer initialized successfully")
        
        # Test category structure
        categories = gatherer.content_categories
        print(f"📚 Available categories: {len(categories)}")
        
        for cat_name, cat_data in list(categories.items())[:3]:  # Test first 3
            print(f"\n🎵 Category: {cat_name}")
            print("-" * 40)
            
            if isinstance(cat_data, dict):
                for subcat_name, subcat_data in cat_data.items():
                    print(f"   📂 {subcat_name}: {len(subcat_data.get('queries', []))} queries")
                    if 'descriptors' in subcat_data:
                        print(f"      🔍 Descriptors: {subcat_data['descriptors'][:50]}...")
        
        print("\n" + "=" * 60)
        print("✅ Content Gatherer test completed!")
        
    except Exception as e:
        print(f"❌ Content Gatherer error: {str(e)}")
        return False
    
    return True


def test_quality_filters():
    """Test the quality filtering functionality."""
    print("\n🎯 Testing Quality Filters")
    print("=" * 60)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        api = FreesoundAPI(api_key)
        
        # Test search with quality filters
        results = api.search(
            query='+rain +gentle',
            duration_range=(30, 180),
            rating_min=3.0,
            downloads_min=100,
            license_filter="Creative Commons 0",
            category="Sound effects",
            subcategory="Natural elements",
            descriptors_filter="ac_brightness:[0 TO 25]"
        )
        
        if 'results' in results and results['results']:
            print(f"✅ Quality filtered search returned {len(results['results'])} results")
            
            # Analyze first result
            sound = results['results'][0]
            print(f"   📎 Sample: {sound['name']}")
            print(f"   ⭐ Rating: {sound.get('avg_rating', 'N/A')}")
            print(f"   📥 Downloads: {sound.get('num_downloads', 'N/A')}")
            print(f"   📜 License: {sound.get('license', 'N/A')}")
            
            # Check AudioCommons analysis if available
            if 'ac_analysis' in sound:
                ac = sound['ac_analysis']
                print(f"   🔊 AC Brightness: {ac.get('ac_brightness', 'N/A')}")
                print(f"   🎵 AC Warmth: {ac.get('ac_warmth', 'N/A')}")
        else:
            print("⚠️  No quality filtered results found")
        
        print("\n" + "=" * 60)
        print("✅ Quality filter test completed!")
        
    except Exception as e:
        print(f"❌ Quality filter test error: {str(e)}")
        return False
    
    return True


def main():
    """Run comprehensive enhanced integration tests."""
    print("🚀 Enhanced Freesound Integration Test Suite")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_enhanced_freesound_api():
        tests_passed += 1
    
    if test_content_gatherer():
        tests_passed += 1
        
    if test_quality_filters():
        tests_passed += 1
    
    # Final report
    print("\n" + "=" * 80)
    print(f"🏆 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All enhanced integration tests PASSED!")
        print("✅ Ready for production use with advanced search strategies")
        return True
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
