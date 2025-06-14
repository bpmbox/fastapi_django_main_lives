#!/usr/bin/env python3
"""
FastAPI Laravel-style Application
=================================

Laravel風のPythonアプリケーション
Artisanコマンドとともに使用
"""

from bootstrap.bootstrap_app import create_app
from config.app import get_config

# アプリケーションインスタンス作成
app = create_app()

# ルーティング設定
from routes.web import router as web_router
from routes.api import router as api_router

app.include_router(web_router)
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    """
    ホームページ
    """
    return {
        "message": f"Welcome to {get_config('app.name')}!",
        "version": "1.0.0",
        "environment": get_config('app.env')
    }

@app.get("/health")
async def health_check():
    """
    ヘルスチェック
    """
    return {
        "status": "ok",
        "app": get_config('app.name'),
        "environment": get_config('app.env')
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=get_config('app.debug')
    )
