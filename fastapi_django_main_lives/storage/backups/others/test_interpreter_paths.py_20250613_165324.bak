#!/usr/bin/env python3
"""
Interpreter Process Path Configuration Test
"""

import os
import sys

# Add the project root to Python path
sys.path.append('/workspaces/fastapi_django_main_live')

from mysite.interpreter.process import get_base_path, ensure_base_path_exists, BASE_PATH

def test_path_configuration():
    print("=== Interpreter Process Path Configuration Test ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Environment INTERPRETER_BASE_PATH: {os.getenv('INTERPRETER_BASE_PATH', 'Not set')}")
    
    # Test base path detection
    detected_path = get_base_path()
    print(f"Detected base path: {detected_path}")
    print(f"Global BASE_PATH: {BASE_PATH}")
    
    # Test path creation
    print("\nTesting path creation...")
    success = ensure_base_path_exists()
    print(f"Path creation successful: {success}")
    
    # Check if path exists and is writable
    if os.path.exists(BASE_PATH):
        print(f"✅ Path exists: {BASE_PATH}")
        test_file = os.path.join(BASE_PATH, "test_write.txt")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Path is writable")
        except Exception as e:
            print(f"❌ Path is not writable: {e}")
    else:
        print(f"❌ Path does not exist: {BASE_PATH}")
    
    # Test with different environment variable
    print("\n=== Testing with custom environment variable ===")
    custom_path = "/tmp/test_interpreter_path/"
    os.environ["INTERPRETER_BASE_PATH"] = custom_path
    
    # Reload the module to test new environment
    import importlib
    import mysite.interpreter.process
    importlib.reload(mysite.interpreter.process)
    
    print(f"Custom path set: {custom_path}")
    print(f"New BASE_PATH: {mysite.interpreter.process.BASE_PATH}")
    
    # Clean up
    if os.path.exists(custom_path):
        import shutil
        shutil.rmtree(custom_path)
    
    # Reset environment
    del os.environ["INTERPRETER_BASE_PATH"]

if __name__ == "__main__":
    test_path_configuration()
