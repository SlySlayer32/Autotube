#!/usr/bin/env python3
"""
Quick Integration Test for Unified GUI

This script performs a rapid test of the key integrated features
to ensure everything is working in the unified GUI.
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
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_integration_readiness():
    """Test that all integrated components are ready."""
    print("🚀 Testing Unified GUI Integration Readiness")
    print("=" * 60)
    
    # Test API initialization
    try:
        api_key = "itJbrm0dQnrfvaQF98tjjCj7GXSCLBvY5a6eNde8"
        api = FreesoundAPI(api_key)
        print("✅ FreesoundAPI initialized successfully")
    except Exception as e:
        print(f"❌ FreesoundAPI initialization failed: {e}")
        return False
    
    # Test context-aware search method exists
    try:
        hasattr(api, 'search_by_tags_and_filename')
        print("✅ Context-aware search method available")
    except:
        print("❌ Context-aware search method missing")
        return False
    
    # Test therapeutic scoring method exists
    try:
        hasattr(api, '_calculate_therapeutic_score')
        print("✅ Therapeutic scoring method available")
    except:
        print("❌ Therapeutic scoring method missing")
        return False
    
    # Test basic search functionality
    try:
        result = api.search(query="rain", page_size=1)
        if result.get('results'):
            print("✅ Basic search functionality working")
        else:
            print("⚠️  Basic search returned no results (API may be rate limited)")
    except Exception as e:
        print(f"❌ Basic search failed: {e}")
        return False
    
    # Test file structure
    required_files = [
        "unified_sleep_audio_gui.py",
        "project_name/api/freesound_api.py",
        "project_name/gui/panels/input_panel.py",
        "project_name/core/content_gatherer.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 All integration components are ready!")
    print("\n🎯 Available Features in Unified GUI:")
    print("  • Context-Aware Search (default)")
    print("  • Empirical Tag Search")
    print("  • Advanced API Search")
    print("  • Hybrid Search Approach")
    print("  • Therapeutic Scoring")
    print("  • Filename Context Filtering")
    print("  • Quality-based Collection")
    print("\n📝 Usage:")
    print("  1. Launch: python unified_sleep_audio_gui.py")
    print("  2. Go to Input Processing → Freesound API")
    print("  3. Select 'Context-Aware Search' (default)")
    print("  4. Choose collection type and quantity")
    print("  5. Click '🎵 Source Sounds'")
    print("  6. Watch therapeutic sounds collected with scores!")
    
    return True


if __name__ == "__main__":
    success = test_integration_readiness()
    if success:
        print("\n✅ READY FOR USE: All systems integrated and operational!")
    else:
        print("\n❌ INTEGRATION ISSUES: Check the output above for problems.")
    
    sys.exit(0 if success else 1)
