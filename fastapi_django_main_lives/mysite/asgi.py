import os
import sys
from django.core.asgi import get_asgi_application
from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.cors import CORSMiddleware

# Jinjaテンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")

# Codespacesでのポート問題を回避するための環境変数設定
os.environ['GRADIO_SERVER_NAME'] = '0.0.0.0'
if 'CODESPACE_NAME' in os.environ:
    # GitHub Codespacesの場合
    os.environ['GRADIO_SERVER_PORT'] = '443'
    os.environ['GRADIO_ROOT_PATH'] = '/gradio'
else:
    os.environ['GRADIO_SERVER_PORT'] = '7860'

import gradio as gr
from mysite.routers.gradio import setup_gradio_interfaces
from mysite.routers.fastapi import setup_webhook_routes,include_routers
from mysite.routers.database import setup_database_routes
from mysite.config.asgi_config import init_django_app
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
# ロガーの設定
from mysite.logger import logger
import threading
import aiofiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_asgi_application()

app = FastAPI()

# Djangoアプリケーションの初期化
init_django_app(app, application)

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gradioインターフェースの設定
gradio_interfaces = setup_gradio_interfaces()

# Laravel風ルーティング統合 - 一時的に無効化 (syntax error in web.py)
# from routes.laravel_routes import register_laravel_routes
# register_laravel_routes(app)

# シンプルなテストルート - 一時的に無効化 (syntax error in web_simple)
# from routes.web_simple import router as simple_router
# app.include_router(simple_router)

# 基本的なルーティングテスト
from fastapi.responses import HTMLResponse

@app.get("/")
async def dashboard(request: Request):
    """
    メインダッシュボード - サイドバー付きでGradioツールを表示
    """
    # Gradioインターフェースの情報を取得
    try:
        from app.Http.Controllers.GradioController import GradioController
        controller = GradioController()
        interface_info = controller.get_interface_list()
        tools = interface_info.get("interface_names", [])
    except Exception as e:
        print(f"⚠️ Interface info error: {e}")
        tools = [
            "📄 ドキュメント生成", "🌐 HTML表示", "🤖 GitHub ISSUE自動生成システム",
            "🚀 GitHub ISSUE自動化", "🎯 統合承認システム", "🚀 統合管理ダッシュボード",
            "💾 プロンプト管理システム", "🔧 UI検証・システム診断", "📁 ファイル管理",
            "💬 AIチャット", "🚗 データベース管理", "✨ Memory Restore",
            "✨ Memory Restore New", "🤖 Open Interpreter"
        ]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tools": tools,
        "title": "🚀 AI Tools Dashboard"
    })

@app.get("/health")
async def health():
    return {"status": "healthy", "gradio_mounted": True}

## Webhookルートの設定
include_routers(app)
setup_webhook_routes(app)

# データベースルートの設定
setup_database_routes(app)

# テンプレートディレクトリの確認
templates_dir = "templates"
if not os.path.exists(templates_dir):
    print(f"⚠️  警告: {templates_dir} ディレクトリが存在しません")
else:
    print(f"✅ テンプレートディレクトリ {templates_dir} を使用しています")


# Gradioインターフェースを Laravel風Controller経由でマウント
try:
    import sys
    import os
    # Laravel風構造のパスを追加
    project_root = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(project_root)
    
    from app.Http.Controllers.GradioController import mount_gradio_to_fastapi
    
    # Laravel風Controller経由でマウント（改良版）
    if gradio_interfaces:
        # シンプルなマウント: 1つのパス、適切なMIME設定
        try:
            # Gradioアプリケーションを作成してマウント
            gradio_app = gr.routes.App.create_app(
                gradio_interfaces,
                app_kwargs={
                    "docs_url": None,
                    "redoc_url": None,
                }
            )
            app.mount("/gradio", gradio_app)
            print("✅ Gradio mounted at /gradio with proper static file handling")
        except Exception as e:
            print(f"⚠️ Primary mount failed: {e}")
            # フォールバック: gr.mount_gradio_app
            try:
                app = gr.mount_gradio_app(app, gradio_interfaces, path="/gradio")
                print("✅ Gradio mounted via gr.mount_gradio_app fallback")
            except Exception as e2:
                print(f"❌ Fallback mount also failed: {e2}")
    else:
        print("❌ No Gradio interfaces found to mount")
        
except Exception as mount_error:
    print(f"❌ Laravel風マウント処理でエラー: {mount_error}")
    # 最終フォールバック: 簡単なインターフェース
    try:
        simple_interface = gr.Interface(
            fn=lambda x: f"🤖 System available, interfaces loading...\nInput: {x}",
            inputs="text",
            outputs="text",
            title="� FastAPI + Gradio Integration",
            description="Laravel風アーキテクチャでGradioを統合"
        )
        app = gr.mount_gradio_app(app, simple_interface, path="/gradio")
        print("✅ Emergency fallback: Simple interface mounted")
    except Exception as emergency_error:
        print(f"❌ Emergency fallback failed: {emergency_error}")



# Gradio静的ファイル用のMIME設定
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi import Request
import mimetypes

# MIMEタイプの設定を強化
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('image/svg+xml', '.svg')

# Gradio静的ファイルのカスタムハンドラー
@app.middleware("http")
async def fix_gradio_static_files(request: Request, call_next):
    response = await call_next(request)
    
    # Gradio関連のファイルのMIMEタイプを修正
    if request.url.path.startswith("/gradio/"):
        if request.url.path.endswith(".css"):
            response.headers["content-type"] = "text/css"
        elif request.url.path.endswith(".js"):
            response.headers["content-type"] = "application/javascript"
        elif request.url.path.endswith(".json"):
            response.headers["content-type"] = "application/json"
        elif request.url.path.endswith(".svg"):
            response.headers["content-type"] = "image/svg+xml"
    
    return response

# Gradio専用の静的ファイルルート
@app.get("/gradio/theme.css")
async def gradio_theme_css():
    """Gradio theme.css を適切なMIMEタイプで提供"""
    from fastapi.responses import Response
    # Gradioのデフォルトテーマを返す
    css_content = """
    :root {
        --color-accent: #3b82f6;
        --color-accent-soft: #dbeafe;
        --color-background-primary: #ffffff;
        --color-background-secondary: #f9fafb;
        --color-border-accent: #3b82f6;
        --color-border-primary: #e5e7eb;
        --color-text-primary: #111827;
        --color-text-secondary: #6b7280;
    }
    
    .gradio-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .tab-nav {
        border-bottom: 1px solid var(--color-border-primary);
        margin-bottom: 20px;
    }
    
    .tab-nav button {
        padding: 10px 20px;
        border: none;
        background: none;
        color: var(--color-text-secondary);
        cursor: pointer;
        font-weight: 500;
    }
    
    .tab-nav button.selected {
        color: var(--color-accent);
        border-bottom: 2px solid var(--color-accent);
    }
    """
    return Response(content=css_content, media_type="text/css")

@app.get("/gradio/config")
async def gradio_config():
    """Gradio設定情報を提供"""
    return {
        "version": "4.29.0",
        "api_docs": False,
        "title": "Gradio Interface Collection",
        "description": "Laravel風アーキテクチャ統合"
    }

# FastAPIにGradioをマウントするため、別途launchは不要
# def run_gradio():
#     gradio_interfaces.launch(server_name="0.0.0.0", server_port=7861, share=True)

# FastAPIで統合するため、threadingでの起動は使用しない

# Gradio静的ファイルパス修正ミドルウェア
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
import re

class GradioStaticFileMiddleware(BaseHTTPMiddleware):
    """Gradioの静的ファイルリクエストを正しいパスにリダイレクト"""
    
    async def dispatch(self, request: Request, call_next):
        # Gradioの静的ファイルパターンをチェック
        path = request.url.path
        
        # Gradioの静的ファイルパターン
        gradio_static_patterns = [
            r'^/theme\.css$',
            r'^/custom\.css$', 
            r'^/component-.*\.js$',
            r'^/theme-.*\.css$',
            r'^/assets/.*\.(css|js|svg|png|jpg|ico)$',
            r'^/file=.*$',
            r'^/info$',
            r'^/heartbeat/.*$',
            r'^/upload.*$',
            r'^/api/.*$'
        ]
        
        # パターンにマッチする場合、/gradioプレフィックスを追加
        for pattern in gradio_static_patterns:
            if re.match(pattern, path):
                new_path = f"/gradio{path}"
                print(f"🔀 Redirecting Gradio static: {path} -> {new_path}")
                return RedirectResponse(url=new_path, status_code=302)
        
        # 通常のリクエスト処理
        response = await call_next(request)
        return response

# ミドルウェアを追加
app.add_middleware(GradioStaticFileMiddleware)
print("✅ Gradio static file middleware added")

# Gradio静的ファイル用の直接ルーティング
@app.get("/theme.css")
async def gradio_theme_css():
    """Gradioのtheme.cssを直接提供"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/gradio/theme.css", status_code=302)

@app.get("/info")
async def gradio_info():
    """Gradioのinfo APIを直接提供"""
    from fastapi.responses import RedirectResponse  
    return RedirectResponse(url="/gradio/info", status_code=302)

@app.get("/heartbeat/{path:path}")
async def gradio_heartbeat(path: str):
    """Gradioのheartbeat APIを直接提供"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/gradio/heartbeat/{path}", status_code=302)

print("✅ Gradio static file routes added")

# 個別ツールアクセス用のルーティング
@app.get("/tools/{tool_name}")
async def tool_redirect(request: Request, tool_name: str):
    """
    個別ツールへの直接アクセス（Gradioにリダイレクト）
    """
    tool_mapping = {
        "chat": "💬 AIチャット",
        "database": "🚗 データベース管理", 
        "files": "📁 ファイル管理",
        "github": "🤖 GitHub ISSUE自動生成システム",
        "memory": "✨ Memory Restore",
        "interpreter": "🤖 Open Interpreter",
        "document": "📄 ドキュメント生成",
        "html": "🌐 HTML表示"
    }
    
    if tool_name in tool_mapping:
        return templates.TemplateResponse("tool_redirect.html", {
            "request": request,
            "tool_name": tool_name,
            "tool_display_name": tool_mapping[tool_name]
        })
    else:
        return templates.TemplateResponse("tool_not_found.html", {
            "request": request,
            "tool_name": tool_name,
            "available_tools": list(tool_mapping.keys())
        })

@app.get("/api")
async def api_docs_redirect(request: Request):
    """
    API文書へのリダイレクト
    """
    return templates.TemplateResponse("api_docs.html", {
        "request": request
    })

# Gradio URL修正ミドルウェア（Codespacesでのポート問題対応）
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class GradioURLFixMiddleware(BaseHTTPMiddleware):
    """GradioのHTMLレスポンス内のポート番号を修正するミドルウェア"""
    
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Gradioのページの場合のみ処理
        if (request.url.path.startswith('/gradio') and 
            response.headers.get('content-type', '').startswith('text/html')):
            
            try:
                # レスポンスボディを取得
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                # HTMLの修正（:7860を削除）
                html_content = body.decode('utf-8')
                
                # Codespacesの場合、:7860を削除
                if 'CODESPACE_NAME' in os.environ:
                    codespace_url = f"https://{os.environ['CODESPACE_NAME']}-7860.app.github.dev"
                    fixed_url = f"https://{os.environ['CODESPACE_NAME']}-7860.app.github.dev"
                    html_content = html_content.replace(f"{fixed_url}:7860", fixed_url)
                    html_content = html_content.replace(":7860/gradio", "/gradio")
                    html_content = html_content.replace(":7860/", "/")
                
                # 新しいレスポンスを作成
                return Response(
                    content=html_content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.headers.get('content-type')
                )
            except Exception as e:
                print(f"⚠️ URL fix middleware error: {e}")
                return response
        
        return response

# Gradio URL修正ミドルウェアを追加
app.add_middleware(GradioURLFixMiddleware)

# Route API の追加
from routers.route_api import router as route_api_router
app.include_router(route_api_router, prefix="/api/v1", tags=["routes"])



