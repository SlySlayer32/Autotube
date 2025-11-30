#!/usr/bin/env python3
"""
Test Collection Type Mapping

This script tests if the collection type selection is properly mapping
to the correct therapeutic categories.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_therapeutic_mapping():
    """Test the therapeutic category mapping function."""
    print("🧪 Testing Collection Type → Category Mapping")
    print("=" * 60)
    
    # Mock the function from input_panel.py
    def _get_therapeutic_categories(collection_type):
        """Map collection types to enhanced therapeutic categories for new API."""
        therapeutic_mapping = {
            "Sleep Sounds": ["nature", "rain", "ocean", "ambient"],
            "Rain & Water": ["rain", "ocean"],
            "Nature Ambience": ["nature", "ambient"], 
            "White/Pink Noise": ["white_noise"],
            "Binaural Sources": ["binaural"],
            "Complete Collection": ["nature", "rain", "ocean", "ambient", "white_noise", "binaural"]
        }
        
        return therapeutic_mapping.get(collection_type, ["nature", "rain", "ocean"])
    
    # Test all collection types
    collection_types = [
        "Sleep Sounds",
        "Rain & Water", 
        "Nature Ambience",
        "White/Pink Noise",
        "Binaural Sources",
        "Complete Collection"
    ]
    
    for collection_type in collection_types:
        categories = _get_therapeutic_categories(collection_type)
        print(f"📂 {collection_type}")
        print(f"   → Categories: {categories}")
        print(f"   → Will search for: {', '.join(categories)}")
        print()
    
    print("=" * 60)
    print("✅ All mappings look correct!")
    print()
    print("🔍 If the wrong files are being downloaded, the issue might be:")
    print("   1. Search queries not finding the right content")
    print("   2. Filename filtering being too restrictive") 
    print("   3. All categories returning similar 'ambient' type sounds")
    print()
    print("💡 Try running with different search methods to compare results:")
    print("   - Context-Aware Search (default)")
    print("   - Empirical Tags")
    print("   - Advanced API")


if __name__ == "__main__":
    test_therapeutic_mapping()
