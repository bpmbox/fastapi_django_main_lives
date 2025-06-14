"""
Application Bootstrap
====================

Laravel風のアプリケーション初期化
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 環境変数読み込み
load_dotenv()

def create_app():
    """
    アプリケーションインスタンスを作成
    """
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title=os.getenv("APP_NAME", "FastAPI Laravel"),
        description="Laravel風FastAPIアプリケーション",
        version="1.0.0"
    )
    
    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 静的ファイル設定
    try:
        app.mount("/static", StaticFiles(directory="public"), name="static")
    except RuntimeError:
        # publicディレクトリが存在しない場合はスキップ
        pass
    
    return app
