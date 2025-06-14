#!/usr/bin/env python3
"""
ContBK統合システム - 動作確認スクリプト
===================================

このスクリプトは、ContBK統合システムが正しく動作しているかを確認します。
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """必要なモジュールのインポートテスト"""
    print("📦 インポートテスト...")
    try:
        from mysite.routers.gradio import include_gradio_interfaces, setup_gradio_interfaces
        print("   ✅ メイン統合モジュール")
        
        from controllers.contbk_example import gradio_interface as contbk_example
        print("   ✅ ContBKダッシュボード")
        
        from controllers.contbk_dashboard import gradio_interface as contbk_dashboard
        print("   ✅ ContBK統合")
        
        return True
    except ImportError as e:
        print(f"   ❌ インポートエラー: {e}")
        return False

def test_interface_detection():
    """インターフェース検出テスト"""
    print("\n🔍 インターフェース検出テスト...")
    try:
        from mysite.routers.gradio import include_gradio_interfaces
        interfaces, names = include_gradio_interfaces()
        
        print(f"   ✅ 検出されたインターフェース数: {len(interfaces)}")
        
        expected_keywords = ['ContBK', 'ダッシュボード', 'AI', 'チャット']
        found_keywords = [kw for kw in expected_keywords if any(kw in name for name in names)]
        
        print(f"   ✅ 期待されるキーワード: {len(found_keywords)}/{len(expected_keywords)}")
        
        if len(interfaces) >= 10 and len(found_keywords) >= 3:
            print("   🎉 インターフェース検出: 成功")
            return True
        else:
            print("   ⚠️ インターフェース検出: 部分的成功")
            return False
            
    except Exception as e:
        print(f"   ❌ 検出エラー: {e}")
        return False

def test_beautiful_titles():
    """美しいタイトルテスト"""
    print("\n🎨 美しいタイトルテスト...")
    try:
        from mysite.routers.gradio import include_gradio_interfaces
        interfaces, names = include_gradio_interfaces()
        
        emoji_count = sum(1 for name in names if any(ord(char) > 127 for char in name))
        
        print(f"   ✅ 絵文字付きタイトル: {emoji_count}/{len(names)}")
        
        if emoji_count >= len(names) * 0.8:  # 80%以上が絵文字付き
            print("   🎉 美しいタイトル: 成功")
            return True
        else:
            print("   ⚠️ 美しいタイトル: 改善の余地あり")
            return False
            
    except Exception as e:
        print(f"   ❌ タイトルテストエラー: {e}")
        return False

def test_contbk_integration():
    """ContBK統合テスト"""
    print("\n📂 ContBK統合テスト...")
    try:
        # ContBKフォルダーの存在確認
        if not os.path.exists('contbk'):
            print("   ⚠️ contbkフォルダーが見つかりません")
            return False
            
        # ContBKインターフェースのロード確認
        contbk_dirs = [d for d in os.listdir('contbk') if d.startswith('gra_') and os.path.isdir(f'contbk/{d}')]
        
        print(f"   ✅ ContBKディレクトリ数: {len(contbk_dirs)}")
        
        if len(contbk_dirs) >= 3:
            print("   🎉 ContBK統合: 成功")
            return True
        else:
            print("   ⚠️ ContBK統合: 部分的成功")
            return False
            
    except Exception as e:
        print(f"   ❌ ContBK統合エラー: {e}")
        return False

def main():
    """メイン検証関数"""
    print("🎯 ContBK統合システム - 動作確認")
    print("=" * 40)
    
    tests = [
        ("インポート", test_imports),
        ("インターフェース検出", test_interface_detection),
        ("美しいタイトル", test_beautiful_titles),
        ("ContBK統合", test_contbk_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n📊 結果サマリー")
    print("-" * 20)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n🎯 総合結果: {success_count}/{len(tests)} テスト成功")
    
    if success_count == len(tests):
        print("🎉 ContBK統合システムは完全に動作しています！")
    elif success_count >= len(tests) * 0.75:
        print("✅ ContBK統合システムは正常に動作しています")
    else:
        print("⚠️ 一部の機能に問題があります。ドキュメントを確認してください")
    
    print("\n📚 詳細情報:")
    print("   - 使用方法: controllers/USAGE_GUIDE.md")
    print("   - 統合ガイド: controllers/README_contbk_integration.md")
    print("   - システム状況: controllers/SYSTEM_STATUS_REPORT.md")

if __name__ == "__main__":
    main()
