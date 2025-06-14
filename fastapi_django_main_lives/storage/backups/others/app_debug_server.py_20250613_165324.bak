#!/usr/bin/env python3
# Debug版のapp.py - VS Codeデバッガー対応

import debugpy
import os
import sys

# デバッグサーバーを開始
debugpy.listen(5678)
print("🐛 デバッグサーバーが起動しました (ポート: 5678)")
print("VS Codeで 'Python: Attach to Process' または 'Python: Remote Attach' を実行してください")
print("ホスト: localhost, ポート: 5678")

# ブレークポイントで待機するかどうか
WAIT_FOR_DEBUGGER = True

if WAIT_FOR_DEBUGGER:
    print("⏸️  デバッガーの接続を待機中... VS Codeでアタッチしてください")
    debugpy.wait_for_client()
    print("✅ デバッガーが接続されました！")

# 元のapp.pyと同じコードを実行
import gradio as gr
import shutil
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

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

GENERATION_TIMEOUT_SEC = 60

from llamafactory.webui.interface import create_ui

if __name__ == "__main__":
    try:
        print("🚀 デバッグモードでアプリケーションを開始しています...")
        
        # デバッグモードで起動
        uvicorn.run(
            "mysite.asgi:app", 
            host="0.0.0.0", 
            port=7860, 
            reload=False,  # デバッグ時はリロード無効
            log_level="debug",
            access_log=True,
            use_colors=True
        )
            
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
