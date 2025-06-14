# FastAPI Django アプリケーション VS Code デバッグ環境構築ガイド

## 📋 概要

このドキュメントは、FastAPI Django アプリケーションでのGroq API統合と`chat_with_interpreter`関数のVS Codeデバッグ環境構築手順をまとめたものです。

## 🚀 完了した作業内容

### 1. Groq API統合とエラー修正
- ✅ 環境変数読み込みエラーの修正
- ✅ `chat_with_interpreter`関数でのGroq API設定
- ✅ `load_dotenv()`の適切な配置

### 2. VS Codeデバッグ環境構築
- ✅ デバッグ用launch.json設定
- ✅ debugpyサーバー設定
- ✅ リモートアタッチ機能
- ✅ ブレークポイント設定

### 3. Webベースデバッグ機能
- ✅ ブラウザ経由でのチャット機能テスト
- ✅ ブレークポイントでの実行停止
- ✅ ステップ実行とデバッグ変数確認

## 🔧 セットアップ手順

### 前提条件
- Python 3.12+
- VS Code
- FastAPI Django アプリケーション
- Groq API キー

### 1. 依存関係のインストール

```bash
pip install debugpy
pip install python-dotenv
pip install open-interpreter
pip install groq
```

### 2. 環境変数設定

`.env`ファイルにGroq APIキーとOpenInterpreterパスワードを設定：
```env
GROQ_API_KEY=gsk_your_api_key_here
api_key=gsk_your_api_key_here
OPENINTERPRETER_PASSWORD=your_secure_password_here
```

**セキュリティ注意事項:**
- パスワードは強固なものを設定してください
- `.env`ファイルは`.gitignore`に追加してバージョン管理から除外してください
- 本番環境では環境変数やシークレット管理サービスを使用してください

### 3. VS Code デバッグ設定

`.vscode/launch.json`ファイル：
```json
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "🎯 Remote Attach (現在のプロセス)",
        "type": "debugpy",
        "request": "attach",
        "connect": {
          "host": "localhost",
          "port": 5678
        },
        "justMyCode": false,
        "pathMappings": [
          {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "${workspaceFolder}"
          }
        ]
      },
      {
        "name": "🚀 App.py Debug (メインアプリ)",
        "type": "debugpy",
        "request": "launch",
        "program": "${workspaceFolder}/app.py",
        "args": ["--debug"],
        "console": "integratedTerminal",
        "justMyCode": false,
        "env": {
          "PYTHONPATH": "${workspaceFolder}",
          "DJANGO_SETTINGS_MODULE": "mysite.settings"
        },
        "cwd": "${workspaceFolder}",
        "stopOnEntry": false,
        "subProcess": false,
        "python": "/home/codespace/.python/current/bin/python3"
      }
    ]
}
```

### 4. デバッグサーバー用アプリケーション

`app_debug_server.py`ファイル：
```python
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
```

## 🎯 デバッグ実行手順

### 1. デバッグサーバー起動

```bash
python3 app_debug_server.py
```

出力例：
```
🐛 デバッグサーバーが起動しました (ポート: 5678)
VS Codeで 'Python: Attach to Process' または 'Python: Remote Attach' を実行してください
ホスト: localhost, ポート: 5678
⏸️  デバッガーの接続を待機中... VS Codeでアタッチしてください
```

### 2. ブレークポイント設定

VS Codeで `controllers/gra_02_openInterpreter/OpenInterpreter.py` の **187行目** にブレークポイントを設定：

```python
def chat_with_interpreter(message, history=None,passw=None, temperature=None, max_new_tokens=None):
    import os
    
    # 🎯 ここにブレークポイントを設定してください！ (デバッグ開始点)
    print(f"DEBUG: Received message: '{message}'")
    print(f"DEBUG: Password: '{passw}'")
```

### 3. VS Codeでデバッガーアタッチ

**方法1: デバッグパネル使用**
1. VS Code左側の「実行とデバッグ」アイコン（🐛）をクリック
2. 上部のドロップダウンで **"🎯 Remote Attach (現在のプロセス)"** を選択
3. **緑の再生ボタン** をクリック

**方法2: F5キー使用**
1. **F5** を押す
2. **"🎯 Remote Attach (現在のプロセス)"** を選択

### 4. デバッガー接続確認

デバッガーが正常に接続されると、ターミナルに以下が表示されます：
```
✅ デバッガーが接続されました！
🚀 デバッグモードでアプリケーションを開始しています...
```

### 5. Webブラウザでテスト

1. ブラウザで `http://localhost:7860` にアクセス
2. **OpenInterpreter** タブをクリック
3. **パスワード欄に環境変数で設定したパスワードを入力** (デフォルト: 12345)
4. **メッセージ欄にテスト用メッセージを入力**
5. **送信ボタンをクリック**

### 6. デバッグ実行

ブレークポイントで実行が停止したら：

- **F10**: ステップオーバー（次の行に進む）
- **F11**: ステップイン（関数内部に入る）  
- **F5**: 継続実行
- **左パネル**: 変数の値を確認
- **ウォッチ**: 式の監視

## 🔍 デバッグ対象ファイル

### メインファイル
- `controllers/gra_02_openInterpreter/OpenInterpreter.py`
- `mysite/interpreter/interpreter.py`

### 重要な関数
- `chat_with_interpreter()` - メインのチャット処理関数
- `format_response()` - レスポンス整形関数
- `initialize_db()` - データベース初期化

## 🐛 トラブルシューティング

### よくある問題と解決方法

#### 1. デバッガーが接続できない
```bash
# プロセス確認
ps aux | grep "python.*app_debug_server"

# ポート確認
netstat -tulpn | grep 5678
```

#### 2. Groq APIキーエラー
```bash
# 環境変数確認
echo $GROQ_API_KEY

# .envファイル確認
cat .env | grep GROQ_API_KEY
```

#### 3. モジュール不足エラー
```bash
# 必要なパッケージをインストール
pip install -r requirements.txt
pip install debugpy python-dotenv open-interpreter groq
```

## 📁 ファイル構成

```
/workspaces/fastapi_django_main_live/
├── app_debug_server.py              # デバッグサーバー用アプリ
├── .vscode/
│   └── launch.json                  # VS Codeデバッグ設定
├── controllers/
│   └── gra_02_openInterpreter/
│       └── OpenInterpreter.py       # メインのチャット処理
├── mysite/
│   └── interpreter/
│       └── interpreter.py           # インタープリター設定
└── .env                             # 環境変数（Groq APIキー）
```

## 🎉 成功時の状態

### ターミナル出力例
```
🐛 デバッグサーバーが起動しました (ポート: 5678)
✅ デバッガーが接続されました！
🚀 デバッグモードでアプリケーションを開始しています...
INFO:     Started server process [270257]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

### デバッグ実行時の出力例
```
DEBUG: Received message: 'Hello, test debug'
DEBUG: Password: '12345'
DEBUG: API key found: gsk_JVhaGp...
DEBUG: Interpreter configured successfully
DEBUG: Password check passed
DEBUG: Processing message: 'Hello, test debug'
```

## 📚 参考情報

### 使用技術
- **FastAPI**: Webアプリケーションフレームワーク
- **Django**: バックエンドフレームワーク
- **Gradio**: Web UI インターフェース
- **Groq API**: LLM API サービス
- **Open Interpreter**: コード実行エンジン
- **debugpy**: Python デバッガー
- **VS Code**: 開発環境

### 重要な設定
- **ポート**: 7860 (Webアプリ), 5678 (デバッグサーバー)
- **パスワード**: 環境変数 `OPENINTERPRETER_PASSWORD` で設定 (デフォルト: 12345)
- **API設定**: Groq llama3-8b-8192 モデル

## 🔒 セキュリティ考慮事項

### パスワード管理
- ハードコーディングを避け、環境変数を使用
- 強固なパスワードを設定
- `.env`ファイルをバージョン管理から除外

### 本番環境での推奨事項
- AWS Secrets Manager, Azure Key Vault等のシークレット管理サービス使用
- 最小権限の原則に従ったアクセス制御
- 定期的なパスワードローテーション

## 🔗 関連ドキュメント

- [VS Code Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [debugpy Documentation](https://github.com/microsoft/debugpy)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq API Documentation](https://console.groq.com/docs)

---

**作成日**: 2025年6月10日  
**最終更新**: 2025年6月10日  
**ステータス**: ✅ 動作確認済み

## 📝 更新履歴

| 日付 | 内容 | 担当者 |
|------|------|--------|
| 2025-06-10 | 初版作成 - VS Codeデバッグ環境構築完了 | GitHub Copilot |
| 2025-06-10 | Groq API統合とエラー修正完了 | GitHub Copilot |
| 2025-06-10 | Webベースデバッグ機能動作確認 | GitHub Copilot |
