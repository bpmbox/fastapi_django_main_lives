#!/usr/bin/env python3
"""
シンプルなWEBデバッグサーバー
確実にブレークポイントが動作するように最小限の設定
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

app = FastAPI(title="WEBデバッグサーバー", description="ブレークポイントテスト用")

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    ホームページ - ここにブレークポイントを設定してください
    """
    # ここにブレークポイントを設定 ⚡
    debug_message = "🐛 デバッグモードでアクセスされました"
    print(debug_message)
    
    # 環境変数をチェック
    api_key = os.getenv("GROQ_API_KEY")
    api_key_status = "✅ 設定済み" if api_key else "❌ 未設定"
    
    # ここにもブレークポイントを設定可能 ⚡
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐛 WEBデバッグサーバー</title>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
            .button {{ display: inline-block; padding: 12px 24px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; cursor: pointer; border: none; font-size: 16px; }}
            .button:hover {{ background: #0056b3; }}
            .status {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
            .success {{ background: #d4edda; color: #155724; }}
            .error {{ background: #f8d7da; color: #721c24; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐛 WEBデバッグサーバー</h1>
            <p>このページでWEB画面操作によるデバッグを試すことができます。</p>
            
            <div class="status {('success' if api_key else 'error')}">
                <strong>GROQ API Key:</strong> {api_key_status}
            </div>
            
            <h2>🎯 デバッグテスト</h2>
            <p>各ボタンをクリックして、VS Codeでブレークポイントの動作を確認してください。</p>
            
            <button class="button" onclick="location.href='/test-simple'">🔥 シンプルテスト</button>
            <button class="button" onclick="location.href='/test-api'">🔑 API キーテスト</button>
            <button class="button" onclick="location.href='/test-chat'">💬 チャットテスト</button>
            <button class="button" onclick="location.href='/test-error'">❌ エラーテスト</button>
            
            <h2>📝 ブレークポイント設定方法</h2>
            <ol>
                <li>VS Codeで <code>simple_debug.py</code> を開く</li>
                <li>行番号の左側をクリックして赤い点を設定</li>
                <li>上のボタンをクリックしてテスト</li>
                <li>VS Codeでステップ実行 (F10, F11, F5)</li>
            </ol>
        </div>
    </body>
    </html>
    """
    
    return html_content

@app.get("/test-simple")
async def test_simple():
    """
    シンプルなテスト - ブレークポイント設定に最適
    """
    # ここにブレークポイントを設定 ⚡
    test_data = {
        "message": "シンプルテストが実行されました",
        "timestamp": "2025-06-10",
        "status": "success"
    }
    
    # 変数を確認できるブレークポイント ⚡
    for key, value in test_data.items():
        print(f"{key}: {value}")
    
    # 結果を返す前のブレークポイント ⚡
    return {"result": "✅ シンプルテスト成功", "data": test_data}

@app.get("/test-api")
async def test_api():
    """
    API設定テスト
    """
    # ここにブレークポイントを設定 ⚡
    api_key = os.getenv("GROQ_API_KEY")
    api_key_exists = bool(api_key)
    
    if api_key_exists:
        # 成功パスのブレークポイント ⚡
        result = {
            "status": "success",
            "message": "✅ GROQ API Key が設定されています",
            "key_length": len(api_key) if api_key else 0
        }
    else:
        # エラーパスのブレークポイント ⚡
        result = {
            "status": "error",
            "message": "❌ GROQ API Key が設定されていません"
        }
    
    return result

@app.get("/test-chat")
async def test_chat():
    """
    チャット機能テスト
    """
    try:
        # ここにブレークポイントを設定 ⚡
        print("🔍 チャット機能のテストを開始")
        
        # chat_with_interpreter のインポートテスト
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        
        # テストメッセージ ⚡
        test_message = "Hello, this is a debug test"
        test_password = "12345"
        
        # ここでchat_with_interpreter関数を呼び出し ⚡
        # (実際の実行は時間がかかるのでスキップ)
        
        result = {
            "status": "success", 
            "message": "✅ chat_with_interpreter 関数が正常にインポートされました",
            "test_message": test_message
        }
        
    except Exception as e:
        # エラー処理のブレークポイント ⚡
        result = {
            "status": "error",
            "message": f"❌ エラー: {str(e)}"
        }
    
    return result

@app.get("/test-error")
async def test_error():
    """
    エラーハンドリングテスト
    """
    # 意図的なエラーのブレークポイント ⚡
    error_message = "これは意図的なテストエラーです"
    
    # ここにブレークポイントを設定してエラーハンドリングを確認 ⚡
    raise HTTPException(status_code=400, detail=error_message)

if __name__ == "__main__":
    print("🚀 シンプルWEBデバッグサーバーを起動中...")
    print("📍 VS Codeでブレークポイントを設定してからアクセスしてください")
    print("🌐 URL: http://localhost:7860")
    
    # デバッグ用設定でuvicornを起動
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        reload=False,  # 重要: デバッグ時はリロード無効
        log_level="debug",
        access_log=True
    )
