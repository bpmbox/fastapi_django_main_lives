#!/usr/bin/env python3
"""
最小限のデバッグテストファイル
確実にブレークポイントが動作します
"""

import os
import sys

# 環境変数を直接読み込み
from dotenv import load_dotenv
load_dotenv()

def simple_test():
    """
    シンプルなテスト関数
    ここにブレークポイントを設定してください
    """
    print("🐛 デバッグテストを開始します")
    
    # ここにブレークポイントを設定 (行 18)
    message = "Hello, Debug World!"
    number = 42
    
    # ここにもブレークポイントを設定 (行 22)
    data = {
        "test": True,
        "message": message,
        "number": number
    }
    
    # ここにもブレークポイントを設定 (行 29)
    for key, value in data.items():
        print(f"{key}: {value}")
    
    print("✅ デバッグテスト完了")
    return data

def test_environment():
    """
    環境変数テスト
    """
    print("🔧 環境変数テストを開始")
    
    # ここにブレークポイントを設定 (行 40)
    api_key = os.getenv("GROQ_API_KEY")
    django_settings = os.getenv("DJANGO_SETTINGS_MODULE")
    
    # ここにブレークポイントを設定 (行 44)
    env_data = {
        "api_key_exists": bool(api_key),
        "django_settings": django_settings,
        "python_path": sys.executable
    }
    
    # ここにブレークポイントを設定 (行 51)
    print(f"API Key exists: {env_data['api_key_exists']}")
    print(f"Django settings: {env_data['django_settings']}")
    print(f"Python path: {env_data['python_path']}")
    
    return env_data

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 最小限デバッグテスト開始")
    print("=" * 50)
    
    # ここにブレークポイントを設定してF10でステップ実行 (行 62)
    result1 = simple_test()
    
    print("\n" + "-" * 30)
    
    # ここにブレークポイントを設定 (行 67)
    result2 = test_environment()
    
    print("\n" + "=" * 50)
    print("🎉 デバッグテスト完了")
    print("=" * 50)
    print(f"Result 1: {result1}")
    print(f"Result 2: {result2}")
