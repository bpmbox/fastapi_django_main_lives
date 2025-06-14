#!/usr/bin/env python3
"""
Simple test for process.py path configuration
"""

import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.append('/workspaces/fastapi_django_main_live')

# Initialize Django
django.setup()

from mysite.interpreter.process import get_base_path, ensure_base_path_exists, get_base_path_safe

def test_path_functions():
    print("=== Process.py Path Test ===")
    
    # Test current directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Test environment variable
    env_path = os.getenv('INTERPRETER_BASE_PATH', 'Not set')
    print(f"INTERPRETER_BASE_PATH: {env_path}")
    
    # Test get_base_path function
    try:
        base_path = get_base_path()
        print(f"✅ get_base_path() succeeded: {base_path}")
    except Exception as e:
        print(f"❌ get_base_path() failed: {e}")
    
    # Test get_base_path_safe function
    try:
        safe_path = get_base_path_safe()
        print(f"✅ get_base_path_safe() succeeded: {safe_path}")
    except Exception as e:
        print(f"❌ get_base_path_safe() failed: {e}")
    
    # Test ensure_base_path_exists function
    try:
        result = ensure_base_path_exists()
        print(f"✅ ensure_base_path_exists() succeeded: {result}")
    except Exception as e:
        print(f"❌ ensure_base_path_exists() failed: {e}")
    
    # Test import
    try:
        from mysite.interpreter.process import BASE_PATH
        print(f"✅ BASE_PATH import succeeded: {BASE_PATH}")
        
        # Check if path exists
        if BASE_PATH and os.path.exists(BASE_PATH):
            print(f"✅ Path exists: {BASE_PATH}")
        else:
            print(f"❌ Path does not exist: {BASE_PATH}")
            
    except Exception as e:
        print(f"❌ BASE_PATH import failed: {e}")

if __name__ == "__main__":
    test_path_functions()
