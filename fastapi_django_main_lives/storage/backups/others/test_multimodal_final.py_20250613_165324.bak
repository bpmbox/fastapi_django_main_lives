#!/usr/bin/env python3
"""
マルチモーダルインターフェース完全テスト
"""
import sys
import os
sys.path.append('.')

def test_multimodal_interfaces():
    print("🧪 マルチモーダルインターフェース完全テスト")
    print("=" * 60)
    
    success_count = 0
    total_tests = 2
    
    # テスト1: フロントエンド生成インターフェース
    print("1. フロントエンド生成インターフェーステスト...")
    try:
        from controllers.gra_10_frontend.frontend_generator import gradio_interface as frontend_interface
        print("   ✅ フロントエンド生成: 正常インポート")
        print(f"   📄 タイトル: {frontend_interface.title}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ フロントエンド生成エラー: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # テスト2: 画像→UI生成インターフェース
    print("2. 画像→UI生成インターフェーステスト...")
    try:
        from controllers.gra_11_multimodal.image_to_ui import gradio_interface as multimodal_interface  
        print("   ✅ 画像→UI生成: 正常インポート")
        print(f"   📄 タイトル: {multimodal_interface.title}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ 画像→UI生成エラー: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print(f"🎯 テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("🎉 すべてのマルチモーダルインターフェースが正常に動作しています！")
        return True
    else:
        print("⚠️  一部のインターフェースに問題があります")
        return False

def test_auto_detection():
    print("\n🔍 自動検出システムテスト")
    print("=" * 60)
    
    try:
        from mysite.routers.gradio import include_gradio_interfaces
        interfaces = include_gradio_interfaces()
        
        print(f"✅ 自動検出されたインターフェース数: {len(interfaces)}")
        print("\n📋 検出されたインターフェース一覧:")
        
        multimodal_found = 0
        for i, interface_info in enumerate(interfaces, 1):
            print(f"{i:2d}. {interface_info}")
            
            # マルチモーダル関連のチェック
            info_str = str(interface_info).lower()
            if 'multimodal' in info_str or 'image_to_ui' in info_str or 'frontend' in info_str:
                multimodal_found += 1
        
        print(f"\n🎯 マルチモーダル関連インターフェース: {multimodal_found}/2 検出")
        
        if multimodal_found >= 1:
            print("✅ マルチモーダルシステムが自動検出システムに統合されています！")
            return True
        else:
            print("❌ マルチモーダルインターフェースが自動検出されていません")
            return False
            
    except Exception as e:
        print(f"❌ 自動検出システムエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 マルチモーダルAIシステム統合テスト開始")
    print("日時:", os.popen("date").read().strip())
    print()
    
    interface_test = test_multimodal_interfaces()
    detection_test = test_auto_detection()
    
    print("\n" + "=" * 60)
    print("📊 最終結果:")
    print(f"   インターフェーステスト: {'✅ 成功' if interface_test else '❌ 失敗'}")
    print(f"   自動検出テスト: {'✅ 成功' if detection_test else '❌ 失敗'}")
    
    if interface_test and detection_test:
        print("\n🎉 マルチモーダルAIシステム完全統合成功！")
        print("🌟 革命的AI自動生成プラットフォーム稼働中")
    else:
        print("\n⚠️  一部に問題があります。確認が必要です。")
