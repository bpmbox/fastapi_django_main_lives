#!/usr/bin/env python3
"""
軽量版 app.py テスト - Gradio無効
"""

import os
import sys
from pathlib import Path

# プロジェクトルートを設定
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 環境変数の設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

print("🚀 軽量版テスト開始")

try:
    # Django初期化
    import django
    django.setup()
    print("✅ Django初期化完了")
    
    # 基本的なFastAPIアプリ作成
    from fastapi import FastAPI
    from django.core.asgi import get_asgi_application
    
    # Django ASGIアプリケーション
    django_asgi_app = get_asgi_application()
    print("✅ Django ASGI作成完了")
    
    # FastAPIアプリケーション
    app = FastAPI(title="Laravel構造対応アプリ")
    print("✅ FastAPI作成完了")
    
    # 静的ファイル設定
    from fastapi.staticfiles import StaticFiles
    if os.path.exists("public"):
        app.mount("/static", StaticFiles(directory="public"), name="static")
        print("✅ 静的ファイルマウント完了")
    
    # Pollsルーター追加テスト
    try:
        from routes.polls import register_polls_routers
        register_polls_routers(app)
        print("✅ Pollsルーター登録完了")
    except Exception as e:
        print(f"⚠️  Pollsルーター登録失敗: {e}")
    
    # 基本的なヘルスチェックエンドポイント
    @app.get("/health")
    def health_check():
        return {"status": "OK", "structure": "Laravel", "framework": "Django+FastAPI"}
    
    print("✅ 軽量版アプリ準備完了")
    print(f"📋 アプリタイプ: {type(app)}")
    
    # エクスポート
    __all__ = ["app"]
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    print("🔧 軽量版サーバー起動")
    uvicorn.run(app, host="0.0.0.0", port=7860)
