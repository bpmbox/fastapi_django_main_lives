"""
WEB画面操作デバッグ用のスクリプト
HTTPリクエストでブレークポイントをトリガーします
"""

import os
import sys
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import traceback

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 環境変数を読み込み
load_dotenv()

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = FastAPI(title="WEB Debug App")

@app.get("/", response_class=HTMLResponse)
async def debug_home():
    """
    デバッグ用ホームページ
    ここにブレークポイントを設定してWEBアクセス時のデバッグができます
    """
    # ここにブレークポイントを設定してください！
    debug_info = {
        "message": "デバッグ用ページ",
        "api_key_exists": bool(os.getenv("GROQ_API_KEY")),
        "python_path": sys.path[:3]
    }
    
    # この行にもブレークポイントを設定して変数を確認
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐛 WEB Debug Interface</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .debug-box {{ background: #e8f4f8; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #007cba; }}
            button {{ padding: 15px 25px; margin: 10px; font-size: 16px; cursor: pointer; border: none; border-radius: 5px; }}
            .test-button {{ background: #4CAF50; color: white; }}
            .debug-button {{ background: #2196F3; color: white; }}
            .warning-button {{ background: #ff9800; color: white; }}
            .test-button:hover {{ background: #45a049; }}
            .debug-button:hover {{ background: #0b7dda; }}
            .warning-button:hover {{ background: #e68900; }}
            .form-group {{ margin: 20px 0; }}
            input, textarea {{ padding: 10px; width: 300px; border: 1px solid #ddd; border-radius: 4px; }}
            textarea {{ width: 500px; height: 80px; }}
            .status {{ display: inline-block; padding: 5px 10px; border-radius: 20px; font-size: 12px; }}
            .status.ok {{ background: #d4edda; color: #155724; }}
            .status.error {{ background: #f8d7da; color: #721c24; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐛 WEB Debug Interface for Chat Interpreter</h1>
            
            <div class="debug-box">
                <h3>🎯 デバッグ状況</h3>
                <p><strong>API Key:</strong> <span class="status {'ok' if debug_info['api_key_exists'] else 'error'}">
                    {'✅ 設定済み' if debug_info['api_key_exists'] else '❌ 未設定'}</span></p>
                <p><strong>Python Path:</strong> {debug_info['python_path'][0]}</p>
                <p><strong>ブレークポイント:</strong> VS Codeで設定してからボタンをクリックしてください</p>
            </div>

            <div class="debug-box">
                <h3>🚀 Chat Interpreter テスト</h3>
                <p>実際のchat_with_interpreter関数を呼び出してデバッグできます</p>
                <form action="/chat_debug" method="post">
                    <div class="form-group">
                        <label>メッセージ:</label><br>
                        <textarea name="message" placeholder="例: Hello, what is 2+2?">Hello, what is 2+2?</textarea>
                    </div>
                    <div class="form-group">
                        <label>パスワード:</label><br>
                        <input type="password" name="password" value="12345" placeholder="12345">
                    </div>
                    <button type="submit" class="test-button">🚀 Chat Interpreter テスト</button>
                </form>
            </div>

            <div class="debug-box">
                <h3>🔧 その他のテスト</h3>
                <form action="/api_test" method="post" style="display: inline;">
                    <button type="submit" class="debug-button">🔑 API Key テスト</button>
                </form>
                <form action="/env_test" method="post" style="display: inline;">
                    <button type="submit" class="debug-button">🌍 環境変数テスト</button>
                </form>
                <form action="/interpreter_test" method="post" style="display: inline;">
                    <button type="submit" class="warning-button">🤖 Interpreter設定テスト</button>
                </form>
            </div>

            <div class="debug-box">
                <h3>📝 ブレークポイント設定箇所</h3>
                <ul>
                    <li><code>web_debug.py</code> 34行目 - ホームページアクセス時</li>
                    <li><code>controllers/gra_02_openInterpreter/OpenInterpreter.py</code> 184行目</li>
                    <li><code>mysite/interpreter/interpreter.py</code> chat_with_interpreter関数内</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content
        </style>
    </head>
    <body>
        <h1>🐛 WEB Debug Interface</h1>
        <div class="debug-box">
            <h2>デバッグ情報</h2>
            <p><strong>API Key:</strong> {debug_info['api_key_exists']}</p>
            <p><strong>Python Path:</strong> {debug_info['python_path']}</p>
        </div>
        
        <div class="debug-box">
            <h2>デバッグテスト</h2>
            <button class="test-button" onclick="testChatInterpreter()">Chat Interpreter テスト</button>
            <button class="debug-button" onclick="testApiKey()">API Key テスト</button>
            <button class="debug-button" onclick="testEnvironment()">環境変数テスト</button>
        </div>
        
        <div class="debug-box">
            <h2>結果表示</h2>
            <div id="result" style="background: white; padding: 15px; border: 1px solid #ddd; min-height: 100px;">
                ここに結果が表示されます
            </div>
        </div>
        
        <script>
            async function testChatInterpreter() {{
                const result = document.getElementById('result');
                result.innerHTML = '🔄 Chat Interpreter をテスト中...';
                
                try {{
                    const response = await fetch('/test/chat-interpreter', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            message: 'Hello, this is a debug test!',
                            password: '12345'
                        }})
                    }});
                    
                    const data = await response.json();
                    result.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    result.innerHTML = '❌ エラー: ' + error.message;
                }}
            }}
            
            async function testApiKey() {{
                const result = document.getElementById('result');
                result.innerHTML = '🔄 API Key をテスト中...';
                
                try {{
                    const response = await fetch('/test/api-key');
                    const data = await response.json();
                    result.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    result.innerHTML = '❌ エラー: ' + error.message;
                }}
            }}
            
            async function testEnvironment() {{
                const result = document.getElementById('result');
                result.innerHTML = '🔄 環境変数をテスト中...';
                
                try {{
                    const response = await fetch('/test/environment');
                    const data = await response.json();
                    result.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    result.innerHTML = '❌ エラー: ' + error.message;
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content

@app.get("/test/api-key")
async def test_api_key():
    """
    API Key テスト用エンドポイント
    ここにブレークポイントを設定してAPI Key の状態をデバッグできます
    """
    # ここにブレークポイントを設定！
    api_key = os.getenv("GROQ_API_KEY")
    alt_api_key = os.getenv("api_key")
    
    # この行にもブレークポイントを設定して変数を確認
    result = {
        "groq_api_key_exists": bool(api_key),
        "api_key_exists": bool(alt_api_key),
        "groq_api_key_length": len(api_key) if api_key else 0,
        "api_key_length": len(alt_api_key) if alt_api_key else 0,
        "environment_loaded": True
    }
    
    return result

@app.get("/test/environment")
async def test_environment():
    """
    環境変数テスト用エンドポイント
    """
    # ここにブレークポイントを設定！
    env_vars = {
        "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY")),
        "api_key": bool(os.getenv("api_key")),
        "DJANGO_SETTINGS_MODULE": os.getenv("DJANGO_SETTINGS_MODULE"),
        "PYTHONPATH": project_root in sys.path
    }
    
    return env_vars

@app.post("/test/chat-interpreter")
async def test_chat_interpreter(request: Request):
    """
    Chat Interpreter テスト用エンドポイント
    ここでchat_with_interpreter関数をデバッグできます
    """
    try:
        # リクエストデータを取得
        data = await request.json()
        message = data.get("message", "Hello")
        password = data.get("password", "12345")
        
        # ここにブレークポイントを設定！
        print(f"🐛 DEBUG: Received message: {message}")
        print(f"🐛 DEBUG: Password: {password}")
        
        # chat_with_interpreter関数をインポート
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        
        # ここにブレークポイントを設定してchat_with_interpreter関数の呼び出しを確認
        responses = []
        response_generator = chat_with_interpreter(
            message=message,
            history=None,
            passw=password,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # レスポンスを収集（ここにもブレークポイント設定可能）
        for response in response_generator:
            responses.append(response)
            print(f"🐛 DEBUG: Response chunk: {response}")
        
        return {
            "success": True,
            "message": message,
            "password_valid": password == "12345",
            "response_count": len(responses),
            "final_response": responses[-1] if responses else "No response"
        }
        
    except Exception as e:
        # エラーハンドリング（ここにもブレークポイント設定可能）
        error_details = {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"🐛 DEBUG: Error occurred: {error_details}")
        return JSONResponse(status_code=500, content=error_details)

if __name__ == "__main__":
    print("🐛 WEB Debug Server を起動中...")
    print("📍 http://localhost:7860 にアクセスしてデバッグを開始してください")
    print("🔧 VS Code でブレークポイントを設定してからボタンをクリックしてください")
    
    # ここにブレークポイントを設定して起動プロセスをデバッグ
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        reload=False,  # デバッグのためリロードを無効化
        log_level="debug"
    )
