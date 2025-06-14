#!/usr/bin/env python3
"""
WEB画面からchat_with_interpreterをデバッグするためのシンプルなアプリ
"""

import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 環境変数を読み込み
from dotenv import load_dotenv
load_dotenv()

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Chat Interpreter Debug App")

@app.get("/", response_class=HTMLResponse)
async def debug_home():
    """
    デバッグ用ホームページ
    ここにブレークポイントを設定してWEBアクセス時のデバッグができます
    """
    # ここにブレークポイントを設定してください！ (行 35)
    debug_info = {
        "api_key_exists": bool(os.getenv("GROQ_API_KEY")),
        "python_executable": sys.executable
    }
    
    # この行にもブレークポイントを設定 (行 41)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐛 Chat Interpreter Debug</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .form-group { margin: 20px 0; }
            input, textarea, button { padding: 10px; margin: 5px; }
            textarea { width: 100%; height: 80px; }
            button { background: #007cba; color: white; border: none; cursor: pointer; border-radius: 5px; }
            button:hover { background: #005a8b; }
            .status { padding: 5px 10px; border-radius: 20px; font-size: 12px; }
            .ok { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐛 Chat Interpreter Debug Interface</h1>
            
            <div style="background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>🎯 デバッグ状況</h3>
                <p><strong>API Key:</strong> 
                   <span class="status {status_class}">
                       {status_text}
                   </span>
                </p>
                <p><strong>ブレークポイント設定箇所:</strong></p>
                <ul>
                    <li><code>web_debug_simple.py</code> 35行目・41行目</li>
                    <li><code>controllers/gra_02_openInterpreter/OpenInterpreter.py</code> 184行目</li>
                </ul>
            </div>

            <form action="/chat_debug" method="post">
                <div class="form-group">
                    <label><strong>メッセージ:</strong></label><br>
                    <textarea name="message" placeholder="例: Hello, what is 2+2?">Hello, what is 2+2?</textarea>
                </div>
                <div class="form-group">
                    <label><strong>パスワード:</strong></label><br>
                    <input type="password" name="password" value="12345" placeholder="12345">
                </div>
                <div class="form-group">
                    <button type="submit">🚀 Chat Interpreter テスト</button>
                </div>
            </form>

            <form action="/api_test" method="post" style="display: inline;">
                <button type="submit" style="background: #4CAF50;">🔑 API Key テスト</button>
            </form>
        </div>
    </body>
    </html>
    """.format(
        status_class="ok" if debug_info["api_key_exists"] else "error",
        status_text="✅ 設定済み" if debug_info["api_key_exists"] else "❌ 未設定"
    )
    
    return html

@app.post("/chat_debug")
async def chat_debug_endpoint(message: str = Form(...), password: str = Form(...)):
    """
    chat_with_interpreter関数をテストするエンドポイント
    """
    # ここにブレークポイントを設定！ (行 96)
    print(f"🐛 DEBUG: Chat request - Message: '{message}', Password: '{password}'")
    
    try:
        # ここにブレークポイントを設定 (行 100)
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        
        print("🔧 DEBUG: About to call chat_with_interpreter")
        
        # ここにブレークポイントを設定してchat_with_interpreter関数をデバッグ (行 105)
        response_generator = chat_with_interpreter(
            message=message,
            history=None,
            passw=password,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # レスポンス収集
        responses = []
        # ここにブレークポイントを設定 (行 115)
        for response in response_generator:
            responses.append(response)
            print(f"🔄 DEBUG: Response: {response}")
        
        final_response = responses[-1] if responses else "No response"
        
        # 結果HTML
        result_html = f"""
        <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>✅ Chat Debug Result</h1>
            <p><strong>Message:</strong> {message}</p>
            <p><strong>Total Responses:</strong> {len(responses)}</p>
            <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3>Final Response:</h3>
                <pre>{final_response}</pre>
            </div>
            <a href="/" style="color: #007cba;">← Back</a>
        </body>
        </html>
        """
        return HTMLResponse(result_html)
        
    except Exception as e:
        # ここにブレークポイントを設定してエラーを確認 (行 139)
        print(f"❌ DEBUG: Error: {e}")
        import traceback
        traceback.print_exc()
        
        error_html = f"""
        <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>❌ Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <pre>{traceback.format_exc()}</pre>
            <a href="/" style="color: #007cba;">← Back</a>
        </body>
        </html>
        """
        return HTMLResponse(error_html)

@app.post("/api_test")
async def api_test_endpoint():
    """
    API Key テスト
    """
    # ここにブレークポイントを設定 (行 158)
    api_key = os.getenv("GROQ_API_KEY")
    
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        status = "✅ Success"
    except Exception as e:
        status = f"❌ Error: {e}"
    
    result_html = f"""
    <html>
    <body style="font-family: Arial; margin: 40px;">
        <h1>🔑 API Key Test</h1>
        <p><strong>API Key Exists:</strong> {bool(api_key)}</p>
        <p><strong>Groq Client Status:</strong> {status}</p>
        <a href="/" style="color: #007cba;">← Back</a>
    </body>
    </html>
    """
    return HTMLResponse(result_html)

if __name__ == "__main__":
    print("🌐 WEB Debug Server starting...")
    print("📍 Access: http://localhost:7861")
    print("🐛 Set breakpoints and use the web form to debug!")
    
    # ここにブレークポイントを設定 (行 184)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7861,
        reload=False,  # デバッグ時はリロード無効
        log_level="debug"
    )
