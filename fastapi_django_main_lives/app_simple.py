#!/usr/bin/env python3
"""
簡易版テスト用 app.py
"""

import os
import sys
from pathlib import Path

# プロジェクトルートを設定
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 環境変数の設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

print("🚀 Laravel構造対応 Django+FastAPI+Gradio アプリケーション")
print("🔄 初期化中...")

try:
    # ASGIアプリケーションをインポート
    from mysite.asgi import app
    print("✅ ASGIアプリのインポート成功")
    print(f"📋 アプリタイプ: {type(app)}")
    
    # Hugging Face Spaces互換性のため、appをエクスポート
    __all__ = ["app"]
    
    print("✅ app.py セットアップ完了")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    print("🔧 直接実行モード")
    print("ℹ️  本番環境では uvicorn app:app を使用してください")
