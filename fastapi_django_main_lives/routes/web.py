"""
Web Routes
==========

ウェブアプリケーション用のルーティング
個別GradioマウントとReact連携対応
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
import gradio as gr
import sys
import os

# Laravel風Controller のパスを追加
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

router = APIRouter()
templates = Jinja2Templates(directory="resources/views")

# Gradioインターフェースのキャッシュ
gradio_cache = {}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    ホームページ
    """
    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "title": "Welcome to FastAPI Laravel"
    })

# テスト用のシンプルなログイン画面
@router.get("/login", response_class=HTMLResponse)
async def simple_login(request: Request):
    """
    シンプルなログイン画面（テスト用）
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Tools Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-card {
                background: white;
                border-radius: 15px;
                padding: 40px;
                max-width: 400px;
                width: 100%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .title {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-weight: bold;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                box-sizing: border-box;
            }
            input:focus {
                border-color: #667eea;
                outline: none;
            }
            .btn {
                width: 100%;
                background: #667eea;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #5a67d8;
            }
            .tools-list {
                margin-top: 30px;
                text-align: center;
            }
            .tool-link {
                display: inline-block;
                margin: 5px;
                padding: 10px 15px;
                background: #f0f0f0;
                color: #333;
                text-decoration: none;
                border-radius: 5px;
                font-size: 14px;
            }
            .tool-link:hover {
                background: #667eea;
                color: white;
            }
            .current-url {
                background: #e2e8f0;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 14px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
            }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h1 class="title">🚀 AI Tools Login</h1>
            
            <div class="current-url">
                📍 現在のURL: <strong>""" + str(request.url) + """</strong>
            </div>
            
            <form action="/dashboard" method="get">
                <div class="form-group">
                    <label for="username">👤 ユーザー名</label>
                    <input type="text" id="username" name="username" placeholder="ユーザー名を入力" required>
                </div>
                
                <div class="form-group">
                    <label for="password">🔒 パスワード</label>
                    <input type="password" id="password" name="password" placeholder="パスワードを入力" required>
                </div>
                
                <button type="submit" class="btn">
                    🔓 ログイン
                </button>
            </form>
            
            <div class="tools-list">
                <h3>🛠️ 利用可能ツール</h3>
                <a href="/tools/chat" class="tool-link">💬 Chat</a>
                <a href="/tools/code-generator" class="tool-link">🤖 Code Gen</a>
                <a href="/tools/screenshot" class="tool-link">📸 Screenshot</a>
                <a href="/tools/admin" class="tool-link">⚙️ Admin</a>
                <a href="/dashboard" class="tool-link">📊 Dashboard</a>
                <a href="/gradio" class="tool-link">🌐 Gradio</a>
            </div>
        </div>
    </body>
    </html>
    """)

# テスト用のシンプルなダッシュボード  
@router.get("/dashboard", response_class=HTMLResponse)
async def simple_dashboard(request: Request):
    """
    シンプルなダッシュボード（テスト用）
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Tools Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                background: rgba(255,255,255,0.1);
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                text-align: center;
            }
            .tools-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .tool-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .tool-card:hover {
                transform: translateY(-5px);
            }
            .tool-icon {
                font-size: 3em;
                margin-bottom: 15px;
            }
            .tool-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333;
            }
            .tool-description {
                color: #666;
                margin-bottom: 20px;
            }
            .tool-url {
                background: #f0f0f0;
                padding: 8px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
                margin-bottom: 15px;
                border-left: 3px solid #667eea;
            }
            .tool-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }
            .tool-btn:hover {
                background: #5a67d8;
            }
            .current-url {
                background: rgba(255,255,255,0.2);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 AI Tools Dashboard</h1>
                <div class="current-url">
                    📍 現在のURL: <strong>""" + str(request.url) + """</strong>
                </div>
                <p>AIツールへの個別アクセス - PWA & キャプチャ対応</p>
            </div>
            
            <div class="tools-grid">
                <div class="tool-card">
                    <div class="tool-icon">💬</div>
                    <div class="tool-title">AI Chat</div>
                    <div class="tool-description">AIとの対話インターフェース</div>
                    <div class="tool-url">/tools/chat</div>
                    <a href="/tools/chat" class="tool-btn" target="_blank">開く</a>
                </div>
                
                <div class="tool-card">
                    <div class="tool-icon">🤖</div>
                    <div class="tool-title">Code Generator</div>
                    <div class="tool-description">AIによるコード生成</div>
                    <div class="tool-url">/tools/code-generator</div>
                    <a href="/tools/code-generator" class="tool-btn" target="_blank">開く</a>
                </div>
                
                <div class="tool-card">
                    <div class="tool-icon">📸</div>
                    <div class="tool-title">Screenshot Tool</div>
                    <div class="tool-description">画面キャプチャ・スクリーンショット</div>
                    <div class="tool-url">/tools/screenshot</div>
                    <a href="/tools/screenshot" class="tool-btn" target="_blank">開く</a>
                </div>
                
                <div class="tool-card">
                    <div class="tool-icon">⚙️</div>
                    <div class="tool-title">Admin Panel</div>
                    <div class="tool-description">システム管理・設定</div>
                    <div class="tool-url">/tools/admin</div>
                    <a href="/tools/admin" class="tool-btn" target="_blank">開く</a>
                </div>
                
                <div class="tool-card">
                    <div class="tool-icon">🌐</div>
                    <div class="tool-title">Gradio Direct</div>
                    <div class="tool-description">統合Gradioインターフェース</div>
                    <div class="tool-url">/gradio</div>
                    <a href="/gradio" class="tool-btn" target="_blank">開く</a>
                </div>
            </div>
        </div>
        
        <script>
            console.log('Dashboard loaded');
            console.log('Current URL:', window.location.href);
        </script>
    </body>
    </html>
    """)

# 個別Gradioマウント機能
def mount_gradio_interface(app: FastAPI, interface_name: str, mount_path: str):
    """
    特定のGradioインターフェースを指定されたパスにマウント
    
    Args:
        app: FastAPIアプリケーション
        interface_name: Gradioインターフェース名
        mount_path: マウントパス（例："/tools/chat"）
    """
    try:
        # Laravel風Controller経由でインターフェース取得
        try:
            from app.Http.Controllers.GradioController import GradioController
            controller = GradioController()
            interfaces, names = controller.gradio_service.collect_gradio_interfaces()
            
            # 指定されたインターフェースを検索
            target_interface = None
            for interface, name in zip(interfaces, names):
                if interface_name.lower() in name.lower():
                    target_interface = interface
                    break
            
            if target_interface:
                # Gradioをマウント
                gradio_asgi = gr.routes.App.create_app(target_interface)
                app.mount(mount_path, gradio_asgi)
                gradio_cache[mount_path] = {
                    "interface": target_interface,
                    "name": interface_name,
                    "mounted": True
                }
                return True, f"✅ {interface_name} mounted at {mount_path}"
            else:
                return False, f"❌ Interface '{interface_name}' not found"
                
        except ImportError:
            # フォールバック: 直接インターフェース作成
            fallback_interface = gr.Interface(
                fn=lambda x: f"Hello from {interface_name}!",
                inputs="text",
                outputs="text",
                title=f"{interface_name} Interface"
            )
            gradio_asgi = gr.routes.App.create_app(fallback_interface)
            app.mount(mount_path, gradio_asgi)
            gradio_cache[mount_path] = {
                "interface": fallback_interface,
                "name": interface_name,
                "mounted": True,
                "fallback": True
            }
            return True, f"✅ Fallback {interface_name} mounted at {mount_path}"
            
    except Exception as e:
        return False, f"❌ Error mounting {interface_name}: {str(e)}"

# React連携用のAPI - 認証付き
@router.get("/api/auth/user")
async def get_current_user():
    """
    現在のユーザー情報を取得（React側で使用）
    """
    # 実際の認証ロジックをここに実装
    return {
        "user_id": "demo_user",
        "username": "Demo User",
        "role": "admin",
        "authenticated": True,
        "permissions": ["chat", "code_gen", "admin", "screenshot"]
    }

@router.post("/api/auth/login")
async def login(request: Request):
    """
    ログイン処理（React側から呼び出し）
    """
    # 実際のログイン処理をここに実装
    return {
        "success": True,
        "token": "demo_token_123",
        "user": {
            "username": "Demo User",
            "role": "admin"
        },
        "redirect_url": "/dashboard"
    }

# React用のダッシュボードルート
@router.get("/dashboard", response_class=HTMLResponse)
async def react_dashboard(request: Request):
    """
    React製のダッシュボード
    """
    return templates.TemplateResponse("react-dashboard.html", {
        "request": request,
        "title": "AI Tools Dashboard",
        "api_base": str(request.base_url),
        "gradio_endpoints": {
            "chat": "/tools/chat",
            "code_gen": "/tools/code-generator", 
            "admin": "/tools/admin",
            "screenshot": "/tools/screenshot"
        }
    })

# 個別Gradioツールのマウント用ルート
@router.get("/tools/mount/{interface_name}")
async def mount_gradio_tool(interface_name: str, request: Request):
    """
    指定されたGradioインターフェースを動的にマウント
    
    Usage: GET /tools/mount/chat → /tools/chat にマウント
    """
    mount_path = f"/tools/{interface_name}"
    
    # 既にマウント済みかチェック
    if mount_path in gradio_cache:
        return {
            "success": True,
            "message": f"Already mounted at {mount_path}",
            "url": mount_path,
            "cached": True
        }
    
    # FastAPIアプリケーションインスタンスを取得
    app = request.app
    
    success, message = mount_gradio_interface(app, interface_name, mount_path)
    
    return {
        "success": success,
        "message": message,
        "url": mount_path if success else None,
        "interface_name": interface_name
    }

# 事前定義された個別ツールルート
@router.get("/tools/chat")
async def ensure_chat_mounted(request: Request):
    """
    チャットインターフェース（事前マウント確認）
    """
    mount_path = "/tools/chat"
    if mount_path not in gradio_cache:
        # シンプルなGradioインターフェースを作成
        import gradio as gr
        simple_chat = gr.Interface(
            fn=lambda x: f"🤖 AI応答: {x}\n\n現在のURL: {request.url}\nタイムスタンプ: 2025-06-13",
            inputs=gr.Textbox(placeholder="メッセージを入力してください..."),
            outputs="text",
            title="💬 AI Chat Interface",
            description="このURLでキャプチャテストが可能です"
        )
        app = request.app
        try:
            gradio_asgi = gr.routes.App.create_app(simple_chat)
            app.mount(mount_path, gradio_asgi)
            gradio_cache[mount_path] = {"interface": simple_chat, "mounted": True}
            print(f"✅ Gradioインターフェースが {mount_path} にマウントされました")
        except Exception as e:
            print(f"❌ マウントエラー: {e}")
            # フォールバック：HTMLページを返す
            return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html><head><title>Chat Tool</title></head>
            <body>
                <h1>💬 AI Chat Tool</h1>
                <p>Gradioインターフェースのマウントに失敗しました。</p>
                <p>エラー: {e}</p>
                <p><a href="/dashboard">ダッシュボードに戻る</a></p>
            </body></html>
            """)
    
    # マウント済みなら、フォワードではなくHTMLページを表示
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html><head><title>Chat Tool</title></head>
    <body>
        <h1>💬 AI Chat Tool</h1>
        <p>Gradioインターフェースは /tools/chat にマウントされています。</p>
        <iframe src="/tools/chat" width="100%" height="600px" frameborder="0"></iframe>
        <p><a href="/dashboard">ダッシュボードに戻る</a></p>
    </body></html>
    """)

# 直接Gradio実行ルート（マウント問題回避用）
@router.get("/tools/chat/direct")
async def chat_direct(request: Request):
    """
    チャット機能の直接実行（Gradioマウント問題回避）
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💬 AI Chat Tool</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }
            .chat-box { background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; min-height: 200px; }
            .input-group { display: flex; gap: 10px; margin-top: 20px; }
            .input-group input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
            .input-group button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; }
            .input-group button:hover { background: #0056b3; }
            .response { background: white; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 4px; }
            .url-info { background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💬 AI Chat Interface</h1>
                <div class="url-info">📍 現在のURL: """ + str(request.url) + """</div>
                <p>PWA & キャプチャテスト対応のチャットツール</p>
            </div>
            
            <div class="chat-box" id="chatBox">
                <div class="response">
                    <strong>🤖 AI:</strong> こんにちは！何かお手伝いできることはありますか？
                </div>
            </div>
            
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="メッセージを入力してください..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">送信</button>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
        
        <script>
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const chatBox = document.getElementById('chatBox');
                const message = input.value.trim();
                
                if (message) {
                    // ユーザーメッセージを表示
                    const userDiv = document.createElement('div');
                    userDiv.className = 'response';
                    userDiv.style.borderLeftColor = '#28a745';
                    userDiv.innerHTML = '<strong>👤 あなた:</strong> ' + message;
                    chatBox.appendChild(userDiv);
                    
                    // AI応答を表示
                    setTimeout(() => {
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'response';
                        aiDiv.innerHTML = '<strong>🤖 AI:</strong> ' + message + ' について理解しました。現在のURL: ' + window.location.href + '<br>タイムスタンプ: ' + new Date().toLocaleString();
                        chatBox.appendChild(aiDiv);
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }, 500);
                    
                    input.value = '';
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            }
        </script>
    </body>
    </html>
    """)

async def ensure_code_gen_mounted(request: Request):
    """
    コード生成インターフェース（事前マウント確認）
    """
    mount_path = "/tools/code-generator"
    if mount_path not in gradio_cache:
        import gradio as gr
        simple_code = gr.Interface(
            fn=lambda prompt: f"""# 生成されたコード
def generated_function():
    '''
    プロンプト: {prompt}
    URL: {request.url}
    '''
    print("Hello from AI Code Generator!")
    return "{prompt}"

# このコードはAIによって生成されました
generated_function()""",
            inputs=gr.Textbox(placeholder="コード生成のプロンプトを入力..."),
            outputs="text",
            title="🤖 AI Code Generator",
            description="コード生成用のキャプチャテストURL"
        )
        app = request.app
        try:
            gradio_asgi = gr.routes.App.create_app(simple_code)
            app.mount(mount_path, gradio_asgi)
            gradio_cache[mount_path] = {"interface": simple_code, "mounted": True}
        except Exception as e:
            print(f"マウントエラー: {e}")
    
    return RedirectResponse(url=mount_path)

# コード生成ツールの直接実行
@router.get("/tools/code-generator/direct")
async def code_generator_direct(request: Request):
    """
    コード生成機能の直接実行
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 Code Generator</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }
            .input-section { margin-bottom: 30px; }
            .input-section label { display: block; margin-bottom: 8px; font-weight: bold; }
            .input-section textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
            .output-section { background: #f8f9fa; border-radius: 8px; padding: 20px; min-height: 300px; }
            .btn { padding: 12px 24px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
            .btn:hover { background: #218838; }
            .url-info { background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }
            pre { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Code Generator</h1>
                <div class="url-info">📍 現在のURL: """ + str(request.url) + """</div>
                <p>AIによるコード生成ツール - PWA対応</p>
            </div>
            
            <div class="input-section">
                <label for="codeRequest">コードリクエスト:</label>
                <textarea id="codeRequest" rows="4" placeholder="作成したいコードの説明を入力してください..."></textarea>
                <button class="btn" onclick="generateCode()" style="margin-top: 10px;">コード生成</button>
            </div>
            
            <div class="output-section">
                <h3>生成されたコード:</h3>
                <div id="codeOutput">
                    <pre><code># ここに生成されたコードが表示されます
def hello_world():
    return "Hello, World from AI Code Generator!"

# 現在のURL: """ + str(request.url) + """
# タイムスタンプ: 2025-06-13</code></pre>
                </div>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
        
        <script>
            function generateCode() {
                const request = document.getElementById('codeRequest').value.trim();
                const output = document.getElementById('codeOutput');
                
                if (request) {
                    const codeTemplate = '# AI生成コード - リクエスト: ' + request + '\\n\\n' +
                        'def generated_function():\\n' +
                        '    """\\n' +
                        '    ' + request + 'のために生成された関数\\n' +
                        '    """\\n' +
                        '    print("🤖 AI Generated Code")\\n' +
                        '    print("リクエスト: ' + request + '")\\n' +
                        '    print("URL: " + window.location.href)\\n' +
                        '    print("生成時刻: " + new Date().toLocaleString())\\n' +
                        '    return "生成完了"\\n\\n' +
                        '# 使用例\\n' +
                        'if __name__ == "__main__":\\n' +
                        '    result = generated_function()\\n' +
                        '    print(result)';
                    
                    output.innerHTML = '<pre><code>' + codeTemplate + '</code></pre>';
                }
            }
        </script>
    </body>
    </html>
    """)

# スクリーンショットツールの直接実行
@router.get("/tools/screenshot/direct")
async def screenshot_direct(request: Request):
    """
    スクリーンショット機能の直接実行
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📸 Screenshot Tool</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }
            .capture-area { background: #f8f9fa; border-radius: 8px; padding: 30px; text-align: center; margin: 20px 0; }
            .btn { padding: 12px 24px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px; }
            .btn:hover { background: #c82333; }
            .btn.success { background: #28a745; }
            .btn.success:hover { background: #218838; }
            .url-info { background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }
            .status { padding: 15px; border-radius: 6px; margin: 15px 0; }
            .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📸 Screenshot & Capture Tool</h1>
                <div class="url-info">📍 現在のURL: """ + str(request.url) + """</div>
                <p>PWA対応のスクリーンキャプチャツール</p>
            </div>
            
            <div class="capture-area">
                <h3>📱 PWAキャプチャテスト</h3>
                <p>このページはPWA/URL-basedスクリーンキャプチャのテスト用です</p>
                
                <button class="btn" onclick="simulateCapture()">📸 スクリーンショット実行</button>
                <button class="btn success" onclick="testPWA()">📱 PWA機能テスト</button>
            </div>
            
            <div id="status"></div>
            
            <div class="status info">
                <strong>📝 キャプチャ情報:</strong><br>
                ・URL: """ + str(request.url) + """<br>
                ・タイムスタンプ: <span id="timestamp"></span><br>
                ・ユーザーエージェント: <span id="userAgent"></span>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
        
        <script>
            document.getElementById('timestamp').textContent = new Date().toLocaleString();
            document.getElementById('userAgent').textContent = navigator.userAgent;
            
            function simulateCapture() {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '<div class="status success">📸 スクリーンショットキャプチャ完了！<br>URL: ' + window.location.href + '<br>時刻: ' + new Date().toLocaleString() + '</div>';
            }
            
            function testPWA() {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '<div class="status success">📱 PWA機能テスト実行中...<br>Service Worker: ' + ('serviceWorker' in navigator ? '対応' : '非対応') + '<br>オフライン対応: 準備完了</div>';
            }
        </script>
    </body>
    </html>
    """)