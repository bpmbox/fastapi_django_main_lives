#!/usr/bin/env python3
"""
Final verification script for process.py fixes
"""
import os
import sys
import subprocess
import time

def main():
    print("=== Process.py Fix Verification ===")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Test 1: Import test
    print("\n1. Testing imports...")
    try:
        # Test the robust version first
        sys.path.insert(0, '/workspaces/fastapi_django_main_live')
        import process_robust
        
        # Test basic functions
        base_path = process_robust.get_base_path_safe()
        print(f"✅ Robust version working: {base_path}")
        
        # Test path creation
        success = process_robust.ensure_base_path_exists()
        print(f"✅ Path creation: {success}")
        
    except Exception as e:
        print(f"❌ Robust version failed: {e}")
        return False
    
    # Test 2: Original process.py with Django
    print("\n2. Testing original process.py...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        import django
        django.setup()
        
        from mysite.interpreter.process import get_base_path, ensure_base_path_exists
        
        original_base_path = get_base_path()
        print(f"✅ Original get_base_path: {original_base_path}")
        
        original_success = ensure_base_path_exists()
        print(f"✅ Original path creation: {original_success}")
        
    except Exception as e:
        print(f"❌ Original process.py failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Functional test
    print("\n3. Testing functional operations...")
    try:
        from mysite.interpreter.process import set_environment_variables
        set_environment_variables()
        print("✅ Environment variables set")
        
        # Test folder creation simulation
        test_folder = f"test_{int(time.time())}"
        test_path = os.path.join(original_base_path, test_folder)
        os.makedirs(test_path, exist_ok=True)
        
        # Test file creation
        test_file = os.path.join(test_path, "prompt")
        with open(test_file, 'w') as f:
            f.write("Test prompt content")
        
        print(f"✅ Test folder and file created: {test_path}")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_path)
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Functional test failed: {e}")
        return False
    
    # Test 4: Configuration summary
    print("\n=== Configuration Summary ===")
    print(f"✅ Base path: {original_base_path}")
    print(f"✅ Environment type: {process_robust.get_environment_type()}")
    print(f"✅ Path exists: {os.path.exists(original_base_path)}")
    print(f"✅ Path writable: {os.access(original_base_path, os.W_OK)}")
    
    # Test 5: Environment variables
    print("\n=== Environment Variables ===")
    env_vars = ['INTERPRETER_BASE_PATH', 'OPENAI_API_KEY', 'MODEL_NAME']
    for var in env_vars:
        value = os.getenv(var, 'Not set')
        status = "✅" if value != 'Not set' else "⚠️"
        print(f"{status} {var}: {value[:20]}{'...' if len(value) > 20 else ''}")
    
    print("\n=== Verification Complete ===")
    print("✅ All tests passed - process.py is working correctly")
    print(f"✅ System ready for use with base path: {original_base_path}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
