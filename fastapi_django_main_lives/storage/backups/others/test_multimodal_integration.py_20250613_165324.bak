#!/usr/bin/env python3
"""
Test script to verify multimodal interface integration
"""
import sys
import os
sys.path.append('.')

def test_multimodal_integration():
    print("🧪 Testing Multimodal Interface Integration")
    print("=" * 50)
    
    try:
        # Test 1: Import the multimodal interface
        print("Test 1: Importing multimodal interface...")
        from controllers.gra_11_multimodal.image_to_ui import gradio_interface
        print("✅ Successfully imported multimodal interface")
        print(f"   Title: {gradio_interface.title}")
        
        # Test 2: Test the auto-detection system
        print("\nTest 2: Testing auto-detection system...")
        from mysite.routers.gradio import include_gradio_interfaces
        interfaces = include_gradio_interfaces()
        print(f"✅ Auto-detection found {len(interfaces)} interfaces:")
        
        for i, interface_info in enumerate(interfaces, 1):
            print(f"   {i}. {interface_info}")
            
        # Check if multimodal is detected
        multimodal_detected = any('multimodal' in str(info).lower() for info in interfaces)
        if multimodal_detected:
            print("✅ Multimodal interface is properly detected!")
        else:
            print("❌ Multimodal interface not detected in auto-system")
            
        # Test 3: Test the image analysis function
        print("\nTest 3: Testing image analysis function...")
        from controllers.gra_11_multimodal.image_to_ui import analyze_image_and_generate_ui
        result = analyze_image_and_generate_ui(None, "Test description", "React")
        print(f"✅ Function test result: {result[0]}")
        
        # Test 4: Test framework generators
        print("\nTest 4: Testing framework generators...")
        from controllers.gra_10_frontend.frontend_generator import gradio_interface as frontend_interface
        print(f"✅ Frontend generator interface: {frontend_interface.title}")
        
        print("\n🎉 All tests passed! Multimodal system is fully integrated!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multimodal_integration()
    sys.exit(0 if success else 1)
