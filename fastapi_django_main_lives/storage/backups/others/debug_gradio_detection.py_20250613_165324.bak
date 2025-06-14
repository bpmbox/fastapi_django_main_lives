#!/usr/bin/env python3
import os
import sys
import traceback

# パスを追加
sys.path.insert(0, '/workspaces/fastapi_django_main_live')

print("=== Gradio Interface Detection Debug ===")

try:
    # 1. 基本的な import テスト
    print("1. Testing basic imports...")
    import gradio as gr
    print("✓ gradio imported successfully")
    
    # 2. 特定のモジュールテスト
    print("\n2. Testing specific module imports...")
    from controllers.gra_07_html.gradio import gradio_interface
    print(f"✓ gradio_interface imported: {type(gradio_interface)}")
    
    # 3. 自動検出システムテスト
    print("\n3. Testing auto-detection system...")
    from mysite.routers.gradio import include_gradio_interfaces
    
    print("Calling include_gradio_interfaces()...")
    interfaces, names = include_gradio_interfaces()
    
    print(f"\n=== Results ===")
    print(f"Total interfaces found: {len(interfaces)}")
    print(f"Interface names: {names}")
    
    for i, name in enumerate(names):
        try:
            print(f"  {i+1}. {name}: {type(interfaces[i])}")
        except Exception as e:
            print(f"  {i+1}. {name}: ERROR - {e}")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()

print("\n=== Debug Complete ===")
