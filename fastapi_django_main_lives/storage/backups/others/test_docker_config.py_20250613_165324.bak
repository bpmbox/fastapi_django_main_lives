#!/usr/bin/env python3
"""
Docker環境設定テストスクリプト
README.md仕様: Gradio 4.29.0, 🦀 emoji, app.py
"""

import os
import json
import sys

def test_environment_variables():
    """環境変数の設定をテスト"""
    print("🦀 Docker環境設定テスト - Gradio FastAPI Django Main")
    print("=" * 60)
    
    # 必須環境変数のチェック
    required_vars = [
        'OPENAI_API_KEY',
        'OPENAI_API_BASE', 
        'MODEL_NAME',
        'GRADIO_SERVER_NAME',
        'GRADIO_SERVER_PORT',
        'GOOGLE_APPLICATION_CREDENTIALS_CONTENT'
    ]
    
    print("📋 必須環境変数チェック:")
    all_set = True
    for var in required_vars:
        value = os.getenv(var, 'NOT_SET')
        if value == 'NOT_SET' or value == 'YOUR_VALUE_HERE':
            print(f"  ❌ {var}: 未設定")
            all_set = False
        else:
            # 機密情報はマスク
            if 'KEY' in var or 'SECRET' in var or 'TOKEN' in var:
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
    
    print("\n📦 オプション環境変数:")
    optional_vars = [
        'APPSHEET_APPID', 'APPSHEET_KEY', 'ChannelAccessToken',
        'github_user', 'github_token', 'hf_token'
    ]
    
    for var in optional_vars:
        value = os.getenv(var, 'NOT_SET')
        if value != 'NOT_SET' and value != 'YOUR_VALUE_HERE':
            print(f"  ✅ {var}: 設定済み")
        else:
            print(f"  ⚠️  {var}: 未設定（オプション）")
    
    return all_set

def test_gradio_version():
    """Gradio バージョンチェック"""
    try:
        import gradio as gr
        print(f"\n🎨 Gradio バージョン: {gr.__version__}")
        
        # README.md仕様との比較
        expected_version = "4.29.0"
        if gr.__version__ == expected_version:
            print(f"  ✅ README.md仕様と一致: {expected_version}")
        else:
            print(f"  ⚠️  README.md仕様 ({expected_version}) と異なります")
        
        return True
    except ImportError as e:
        print(f"  ❌ Gradio インポートエラー: {e}")
        return False

def test_google_cloud_config():
    """Google Cloud認証設定テスト"""
    print("\n☁️  Google Cloud設定:")
    
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    if creds_content:
        try:
            creds_json = json.loads(creds_content)
            project_id = creds_json.get('project_id', 'NOT_FOUND')
            client_email = creds_json.get('client_email', 'NOT_FOUND')
            
            print(f"  ✅ プロジェクトID: {project_id}")
            print(f"  ✅ サービスアカウント: {client_email}")
            return True
        except json.JSONDecodeError:
            print("  ❌ 認証情報のJSON形式が無効です")
            return False
    else:
        print("  ❌ Google Cloud認証情報が設定されていません")
        return False

def main():
    """メインテスト実行"""
    print("🚀 Docker環境設定検証開始\n")
    
    env_ok = test_environment_variables()
    gradio_ok = test_gradio_version()
    gcp_ok = test_google_cloud_config()
    
    print("\n" + "=" * 60)
    print("📊 テスト結果サマリー:")
    print(f"  環境変数: {'✅ OK' if env_ok else '❌ NG'}")
    print(f"  Gradio: {'✅ OK' if gradio_ok else '❌ NG'}")
    print(f"  Google Cloud: {'✅ OK' if gcp_ok else '❌ NG'}")
    
    overall_status = all([env_ok, gradio_ok, gcp_ok])
    if overall_status:
        print("\n🎉 すべてのテストが通過しました！")
        print("✨ README.md仕様に準拠したDocker環境が正常に設定されています")
    else:
        print("\n⚠️  いくつかの設定に問題があります")
        print("💡 上記のエラーを修正してから再度テストしてください")
    
    return 0 if overall_status else 1

if __name__ == "__main__":
    sys.exit(main())
