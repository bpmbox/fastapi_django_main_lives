#!/usr/bin/env python3
"""
フロントエンドジェネレーター修正確認テスト
"""
import sys
import os
sys.path.append('.')

def test_frontend_generator():
    print("🔧 フロントエンドジェネレーター修正テスト")
    print("=" * 50)
    
    try:
        print("1. フロントエンドジェネレーターインポートテスト...")
        from controllers.gra_10_frontend.frontend_generator import gradio_interface as frontend_interface
        print("   ✅ インポート成功")
        print(f"   📄 タイトル: {frontend_interface.title}")
        
        print("\n2. 基本機能テスト...")
        from controllers.gra_10_frontend.frontend_generator import generate_react_component
        result = generate_react_component("TestComponent", "テスト用コンポーネント", "Modern")
        print(f"   ✅ React生成テスト: {result[0]}")
        
        from controllers.gra_10_frontend.frontend_generator import generate_vue_component
        result = generate_vue_component("TestVueComponent", "テスト用Vueコンポーネント", "Modern")
        print(f"   ✅ Vue生成テスト: {result[0]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auto_detection():
    print("\n🔍 自動検出システムテスト")
    print("=" * 50)
    
    try:
        from mysite.routers.gradio import include_gradio_interfaces
        interfaces = include_gradio_interfaces()
        
        print(f"検出されたインターフェース数: {len(interfaces)}")
        
        frontend_found = False
        multimodal_found = False
        
        print("\n📋 検出されたインターフェース一覧:")
        for i, interface_info in enumerate(interfaces, 1):
            print(f"{i:2d}. {interface_info}")
            
            info_str = str(interface_info).lower()
            if 'frontend' in info_str:
                frontend_found = True
            elif 'multimodal' in info_str or 'image_to_ui' in info_str:
                multimodal_found = True
        
        print(f"\n🎯 マルチモーダル統合確認:")
        print(f"   フロントエンドジェネレーター: {'✅ 検出済み' if frontend_found else '❌ 未検出'}")
        print(f"   画像→UI生成: {'✅ 検出済み' if multimodal_found else '❌ 未検出'}")
        
        return frontend_found and multimodal_found
        
    except Exception as e:
        print(f"❌ 自動検出エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 フロントエンドジェネレーター修正確認")
    print(f"実行日時: {os.popen('date').read().strip()}")
    print()
    
    generator_test = test_frontend_generator()
    detection_test = test_auto_detection()
    
    print("\n" + "=" * 50)
    print("📊 最終結果:")
    print(f"   ジェネレーターテスト: {'✅ 成功' if generator_test else '❌ 失敗'}")
    print(f"   自動検出テスト: {'✅ 成功' if detection_test else '❌ 失敗'}")
    
    if generator_test and detection_test:
        print("\n🎉 フロントエンドジェネレーター修正完了！")
        print("🌟 マルチモーダルシステム完全稼働中")
    else:
        print("\n⚠️  追加の修正が必要です")
    
    # WebUIアクセス情報
    print(f"\n🌐 WebUIアクセス: http://localhost:7860")
    print("   新しいタブが追加されているかご確認ください")
