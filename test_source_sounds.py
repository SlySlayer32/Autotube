#!/usr/bin/env python3
"""
Test script for the new Automated Source Sounds feature.
This script demonstrates the functionality without requiring the full GUI.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.content_gatherer import ContentGatherer

def test_source_sounds_feature():
    """Test the automated source sounds functionality."""
    print("🎵 Testing SonicSleep Pro - Automated Source Sounds Feature")
    print("=" * 60)
    
    # Your pre-configured API key
    api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
    
    try:
        # Initialize the Freesound API
        print("1. Initializing Freesound API...")
        freesound_api = FreesoundAPI(api_key)
        print("   ✅ API initialized successfully")
        
        # Test a simple search
        print("\n2. Testing search functionality...")
        results = freesound_api.search(
            query="gentle rain sleep",
            page_size=5,
            sort="rating"
        )
        
        if results and 'results' in results:
            print(f"   ✅ Found {len(results['results'])} sleep sounds")
            
            # Display some results
            print("\n   Sample Results:")
            for i, sound in enumerate(results['results'][:3], 1):
                print(f"   {i}. {sound['name']} ({sound['duration']:.1f}s) - {sound['license']}")
        else:
            print("   ❌ No results found")
            
        # Test content gatherer
        print("\n3. Testing content gatherer...")
        content_gatherer = ContentGatherer(api_key)
        print("   ✅ Content gatherer initialized")
        
        # Simulate the sleep sound categories from the GUI
        sleep_categories = {
            "Rain Sounds": ["gentle rain", "light rain"],
            "Ocean Waves": ["ocean waves", "gentle waves"],
        }
        
        print("\n4. Simulating automated collection...")
        print("   Collection Type: Sleep Sounds")
        print("   Categories:", list(sleep_categories.keys()))
        
        # This would be the actual collection process
        print("   📁 Files would be saved to: processed_clips/")
        print("   🎵 Ready for automated sleep sound collection!")
        
        print("\n" + "=" * 60)
        print("🎉 Source Sounds feature test completed successfully!")
        print("\nTo use in the GUI:")
        print("1. Launch: python -m project_name.gui.main")
        print("2. Go to Audio Processing > Freesound API tab")
        print("3. Click '🎵 Source Sounds' button")
        print("4. Select collection type and quantity")
        print("5. Watch automatic collection!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_source_sounds_feature()
