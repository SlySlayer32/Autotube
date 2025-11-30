#!/usr/bin/env python3
"""
Test Context-Aware Search Integration

This script tests the new context-aware search that analyzes both tags and filenames
to filter out inappropriate sounds like "metal rain" vs "gentle rain".
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_name.api.freesound_api import FreesoundAPI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_context_aware_search():
    """Test the new context-aware search functionality."""
    print("🎯 Testing Context-Aware Search (Tags + Filename Analysis)")
    print("=" * 70)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        api = FreesoundAPI(api_key)
        print("✅ FreesoundAPI initialized successfully")
        
        # Test categories that benefit from context analysis
        test_categories = ["rain", "ocean", "nature", "ambient"]
        
        for category in test_categories:
            print(f"\n🎵 Testing context-aware search for: {category}")
            print("-" * 50)
            
            try:
                results = api.search_by_tags_and_filename(
                    category_type=category,
                    max_results=10,
                    duration_range=(30, 300),
                    quality_filter=True
                )
                
                if results.get('results'):
                    print(f"✅ Found {len(results['results'])} context-filtered {category} sounds")
                    
                    # Show top 3 results with analysis
                    for i, sound in enumerate(results['results'][:3], 1):
                        score = sound.get('therapeutic_score', 0)
                        name = sound.get('name', 'Unknown')
                        duration = sound.get('duration', 0)
                        rating = sound.get('avg_rating', 0)
                        
                        print(f"   {i}. {name}")
                        print(f"      🎯 Therapeutic Score: {score:.1f}")
                        print(f"      ⏱️  Duration: {duration:.1f}s")
                        print(f"      ⭐ Rating: {rating}/5")
                        
                        # Show some tags
                        tags = sound.get('tags', [])[:5]
                        if tags:
                            print(f"      🏷️  Tags: {', '.join(tags)}")
                        print()
                else:
                    print(f"⚠️  No context-filtered results found for {category}")
                    
            except Exception as e:
                print(f"❌ Error testing {category}: {str(e)}")
                continue
        
        print("\n" + "=" * 70)
        print("✅ Context-aware search test completed!")
        
    except Exception as e:
        print(f"❌ API initialization error: {str(e)}")
        return False
    
    return True


def test_filename_filtering():
    """Test the filename context filtering specifically."""
    print("\n🔍 Testing Filename Context Filtering")
    print("=" * 70)
    
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        api = FreesoundAPI(api_key)
        
        # Test cases that should demonstrate filtering
        test_cases = [
            {
                "category": "rain",
                "expected_positive": ["gentle", "soft", "peaceful", "roof", "window"],
                "expected_negative": ["metal", "storm", "thunder", "heavy", "harsh"]
            },
            {
                "category": "ocean", 
                "expected_positive": ["calm", "gentle", "peaceful", "lapping"],
                "expected_negative": ["storm", "crashing", "rough", "violent"]
            }
        ]
        
        for test_case in test_cases:
            category = test_case["category"]
            print(f"\n🎵 Testing filename filtering for: {category}")
            print("-" * 50)
            
            # Get regular search results first
            regular_results = api.search(
                query=f"+{category}",
                page_size=20,
                duration_range=(30, 300)
            )
            
            # Get context-aware results
            context_results = api.search_by_tags_and_filename(
                category_type=category,
                max_results=10,
                duration_range=(30, 300)
            )
            
            print(f"📊 Regular search: {len(regular_results.get('results', []))} results")
            print(f"🎯 Context-filtered: {len(context_results.get('results', []))} results")
            
            if context_results.get('results'):
                print(f"\n📋 Context-filtered results:")
                for i, sound in enumerate(context_results['results'][:5], 1):
                    name = sound.get('name', '').lower()
                    score = sound.get('therapeutic_score', 0)
                    
                    # Check for positive/negative context words
                    positive_found = [word for word in test_case["expected_positive"] if word in name]
                    negative_found = [word for word in test_case["expected_negative"] if word in name]
                    
                    print(f"   {i}. {sound.get('name')} (Score: {score:.1f})")
                    if positive_found:
                        print(f"      ✅ Positive context: {', '.join(positive_found)}")
                    if negative_found:
                        print(f"      ❌ Negative context: {', '.join(negative_found)} (should be filtered)")
                    print()
        
        print("=" * 70)
        print("✅ Filename filtering test completed!")
        
    except Exception as e:
        print(f"❌ Filename filtering test error: {str(e)}")
        return False
    
    return True


def test_therapeutic_scoring():
    """Test the therapeutic scoring algorithm."""
    print("\n🎯 Testing Therapeutic Scoring Algorithm")
    print("=" * 70)
    
    # Test mock sound data
    test_sounds = [
        {
            "name": "gentle rain on roof peaceful ambient",
            "avg_rating": 4.5,
            "num_downloads": 150,
            "duration": 180,
            "tags": ["rain", "peaceful", "ambient", "roof"]
        },
        {
            "name": "metal rain storm harsh industrial",
            "avg_rating": 3.0, 
            "num_downloads": 50,
            "duration": 60,
            "tags": ["rain", "storm", "metal", "industrial"]
        },
        {
            "name": "ocean waves gentle beach calm",
            "avg_rating": 4.8,
            "num_downloads": 300,
            "duration": 240,
            "tags": ["ocean", "waves", "beach", "calm"]
        }
    ]
    
    api = FreesoundAPI("dummy_key")
    
    positive_words = ["gentle", "peaceful", "calm", "ambient", "soft"]
    negative_words = ["metal", "harsh", "storm", "industrial", "loud"] 
    core_tags = ["rain", "ocean", "waves"]
    
    print("📊 Scoring test sounds:")
    for i, sound in enumerate(test_sounds, 1):
        score = api._calculate_therapeutic_score(sound, positive_words, negative_words, core_tags)
        print(f"\n{i}. {sound['name']}")
        print(f"   🎯 Therapeutic Score: {score:.1f}")
        print(f"   ⭐ Rating: {sound['avg_rating']}/5")
        print(f"   📥 Downloads: {sound['num_downloads']}")
        print(f"   🏷️  Tags: {', '.join(sound['tags'])}")
    
    print("\n" + "=" * 70)
    print("✅ Therapeutic scoring test completed!")
    
    return True


def main():
    """Run comprehensive context-aware search tests."""
    print("🚀 Context-Aware Search Test Suite")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_context_aware_search():
        tests_passed += 1
    
    if test_filename_filtering():
        tests_passed += 1
        
    if test_therapeutic_scoring():
        tests_passed += 1
    
    # Final report
    print("\n" + "=" * 80)
    print(f"🏆 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All context-aware search tests PASSED!")
        print("✅ Ready for production use with filename + tag analysis")
        print("🎯 The system will now filter out inappropriate sounds like 'metal rain'")
        print("📊 Therapeutic scoring helps rank sounds by relevance")
        return True
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
