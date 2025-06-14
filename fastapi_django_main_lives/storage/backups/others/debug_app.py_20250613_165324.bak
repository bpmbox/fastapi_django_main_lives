#!/usr/bin/env python3
"""
デバッグ専用アプリケーション起動スクリプト
ブレークポイントが確実に動作するように設定されています
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 環境変数を設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# dotenvから環境変数を読み込み
from dotenv import load_dotenv
load_dotenv()

print("🐛 デバッグモードで起動中...")
print("📍 ブレークポイントを設定してF5でデバッグを開始してください")

# Djangoを初期化
django.setup()

# FastAPIアプリを直接インポート
try:
    from mysite.asgi import app
    print("✅ FastAPIアプリケーションをインポートしました")
except ImportError as e:
    print(f"❌ アプリケーションのインポートに失敗: {e}")
    sys.exit(1)

# デバッグ用のテスト関数
def debug_test():
    """
    この関数にブレークポイントを設定してテストしてください
    """
    print("🔍 デバッグテスト関数が呼び出されました")
    
    # 環境変数の確認
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key exists: {bool(api_key)}")
    
    # ここにブレークポイントを設定
    test_data = {
        "message": "Hello Debug",
        "api_key_present": bool(api_key),
        "django_ready": True
    }
    
    # この行にもブレークポイントを設定して変数を確認
    for key, value in test_data.items():
        print(f"{key}: {value}")
    
    return test_data

if __name__ == "__main__":
    # テスト関数を実行（ここにブレークポイントを設定）
    result = debug_test()
    
    print("🚀 デバッグモードでサーバーを起動します...")
    print("⚠️  reload=False でブレークポイントが有効です")
    
    # uvicornを直接使用（リロードなし）
    import uvicorn
    
    # ここにブレークポイントを設定してuvicorn.runの動作を確認
    uvicorn.run(
        app,  # アプリケーションオブジェクトを直接渡す
        host="0.0.0.0",
        port=7860,
        reload=False,  # 重要: リロードを無効化
        log_level="debug",
        access_log=True,
        use_colors=True
    )
