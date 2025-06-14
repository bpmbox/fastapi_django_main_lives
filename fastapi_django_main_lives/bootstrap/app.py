import gradio as gr
import os
import shutil
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# デバッグサーバーの設定
def setup_debug_server():
    """デバッグサーバーをセットアップ"""
    try:
        import debugpy
        if not debugpy.is_client_connected():
            print("🔧 デバッグサーバーを起動中...")
            debugpy.listen(("0.0.0.0", 5678))
            print("✅ デバッグサーバーがポート5678で待機中")
            print("💡 VS Codeで 'Remote Attach' を使用してアタッチできます")
        else:
            print("🔗 デバッグクライアントが既に接続されています")
    except ImportError:
        print("⚠️  debugpy がインストールされていません。通常のデバッグモードで継続します")
    except Exception as e:
        print(f"⚠️  デバッグサーバー起動エラー: {e}")

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
from groq import Groq

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Any, Coroutine, List

from starlette.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from groq import AsyncGroq, AsyncStream, Groq
from groq.lib.chat_completion_chunk import ChatCompletionChunk
from groq.resources import Models
from groq.types import ModelList
from groq.types.chat.completion_create_params import Message

import async_timeout
import asyncio
from interpreter import interpreter
import os

GENERATION_TIMEOUT_SEC = 60

if __name__ == "__main__":
    import sys
    
    # デバッグ: コマンドライン引数と環境変数を確認
    print(f"🔍 sys.argv: {sys.argv}")
    print(f"🔍 SPACE_ID環境変数: {os.getenv('SPACE_ID')}")
    print(f"🔍 '--gradio' in sys.argv: {'--gradio' in sys.argv}")
    
    # デバッグモードかどうかを判定
    is_debug = "--debug" in sys.argv or any("debugpy" in arg for arg in sys.argv)
    
    # デバッグモードの場合、デバッグサーバーをセットアップ
    if is_debug:
        setup_debug_server()
    
    # 実行環境の表示
    if os.getenv("SPACE_ID"):
        print("🤗 Hugging Face Spaces環境で実行中")
    else:
        print("💻 ローカル開発環境で実行中")
    
    try:
        print("🚀 アプリケーションを開始しています...")
        
        # デバッグサーバーのセットアップ
        setup_debug_server()
        
        if is_debug:
            print("🐛 デバッグモード: リロードを無効化してブレークポイントを有効にします")
            # デバッグモード: reloadを無効にしてブレークポイントを使用可能に
            uvicorn.run(
                "app:app",  # ルートレベルのapp.pyを参照
                host="0.0.0.0", 
                port=7860, 
                reload=False,  # デバッグ時はリロード無効
                log_level="debug",
                access_log=True,
                use_colors=True
            )
        else:
            print("📍 開発モード: ホットリロードが有効です")
            # 開発モード: reloadを有効にして高速開発
            uvicorn.run(
                "app:app",  # ルートレベルのapp.pyを参照
                host="0.0.0.0", 
                port=7860, 
                reload=True,  # 開発時はリロード有効
                log_level="debug",
                access_log=True,
                use_colors=True,
                reload_dirs=["/workspaces/fastapi_django_main_live"]
            )
            
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
