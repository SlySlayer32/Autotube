# This file locks the Python version for this project
# Any attempt to run with a different Python version will fail

# Required Python version: 3.11.0
# Path: C:\Users\Sly\AppData\Local\Programs\Python\Python311\python.exe

import sys
import os

REQUIRED_PYTHON_VERSION = (3, 11)
REQUIRED_PYTHON_PATH = r"C:\Users\Sly\AppData\Local\Programs\Python\Python311\python.exe"

def check_python_version():
    """Strictly enforce Python 3.11 usage for this project."""
    
    current_version = sys.version_info[:2]
    
    if current_version != REQUIRED_PYTHON_VERSION:
        print(f"❌ PYTHON VERSION ERROR!")
        print(f"   Required: Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}")
        print(f"   Current:  Python {current_version[0]}.{current_version[1]}")
        print(f"   Path:     {sys.executable}")
        print()
        print("🔧 To fix this issue:")
        print(f"   1. Use the correct Python: {REQUIRED_PYTHON_PATH}")
        print("   2. Run setup script: setup_python311.ps1")
        print("   3. Activate virtual environment: .venv\\Scripts\\Activate.ps1")
        print()
        raise RuntimeError(f"This project requires Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} exactly!")
    
    print(f"✅ Python version check passed: {current_version[0]}.{current_version[1]}")
    return True

def check_dependencies():
    """Check if critical dependencies are available."""
    critical_deps = ['tensorflow', 'openl3', 'librosa', 'numpy']
    missing_deps = []
    
    for dep in critical_deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Missing critical dependencies: {', '.join(missing_deps)}")
        print("🔧 Run setup script to install: setup_python311.ps1")
        return False
    
    print("✅ All critical dependencies available")
    return True

if __name__ == "__main__":
    print("🐍 Python Version Control Check")
    print("=" * 40)
    
    try:
        check_python_version()
        check_dependencies()
        print("✅ Environment validation passed!")
    except Exception as e:
        print(f"❌ Environment validation failed: {e}")
        sys.exit(1)
