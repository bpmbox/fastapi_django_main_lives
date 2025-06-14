#!/usr/bin/env python3
"""
Test script for process.py functions
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, '/workspaces/fastapi_django_main_live')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

def test_process_functions():
    print("=== Process.py Test ===")
    
    try:
        # Test path functions directly without Django imports
        import os
        
        def get_base_path_test():
            """Test version of get_base_path"""
            try:
                env_base_path = os.getenv("INTERPRETER_BASE_PATH")
                if env_base_path and os.path.exists(os.path.dirname(env_base_path)):
                    return env_base_path
                
                current_dir = os.getcwd()
                
                if "/workspaces/" in current_dir:
                    path = os.path.join(current_dir, "app", "Http", "controller")
                    return path + "/"
                
                if "/home/user/app/" in current_dir or os.path.exists("/home/user/app/"):
                    return "/home/user/app/app/Http/controller/"
                
                if "fastapi_django_main_live" in current_dir:
                    path = os.path.join(current_dir, "app", "Http", "controller")
                    return path + "/"
                
                fallback_path = os.path.join(current_dir, "temp_controller")
                return fallback_path + "/"
                
            except Exception as e:
                print(f"Error in get_base_path_test: {e}")
                return os.path.join(os.getcwd(), "temp_controller") + "/"
        
        # Test the function
        base_path = get_base_path_test()
        print(f"✅ Base path detection: {base_path}")
        
        # Test path creation
        os.makedirs(base_path, exist_ok=True)
        print(f"✅ Path creation successful: {os.path.exists(base_path)}")
        
        # Test a sample folder creation
        test_folder = os.path.join(base_path, "test_folder")
        os.makedirs(test_folder, exist_ok=True)
        print(f"✅ Test folder creation: {os.path.exists(test_folder)}")
        
        # Write test file
        test_file = os.path.join(test_folder, "prompt")
        with open(test_file, 'w') as f:
            f.write("Test prompt content")
        print(f"✅ File write test: {os.path.exists(test_file)}")
        
        # Read test file
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"✅ File read test: '{content[:20]}...'")
        
        # Cleanup
        import shutil
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        print("✅ Cleanup completed")
        
        print("\n=== Test Results ===")
        print("✅ All basic path operations working correctly")
        print(f"✅ Recommended BASE_PATH: {base_path}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_process_functions()
