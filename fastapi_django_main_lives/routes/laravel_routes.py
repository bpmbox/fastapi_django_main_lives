"""
Laravel風ルーティング統合
========================

すべてのLaravel構造のルートを統合
"""

from fastapi import FastAPI
import gradio as gr

def register_laravel_routes(app: FastAPI):
    """
    Laravel風のルートファイルをすべて登録
    """
    
    # Web Routes
    try:
        from routes.web_simple import router as web_simple_router
        app.include_router(web_simple_router, tags=["web"])
        print("✅ Web Routes (Simple) registered")
    except ImportError as e:
        print(f"⚠️  Web Routes import error: {e}")
        
    # Original Web Routes (fallback)
    try:
        from routes.web import router as web_router
        app.include_router(web_router, tags=["web-original"])
        print("✅ Web Routes (Original) registered")
    except Exception as e:
        print(f"⚠️  Original Web Routes import error: {e}")
    
    # API Routes  
    try:
        from routes.api import router as api_router
        app.include_router(api_router, prefix="/api/v1", tags=["api"])
        print("✅ API Routes registered")
    except ImportError as e:
        print(f"⚠️  API Routes import error: {e}")
    
    # Polls Routes (Laravel構造)
    try:
        from routes.polls import register_polls_routers
        register_polls_routers(app)
        print("✅ Polls Routes (Laravel structure) registered")
    except ImportError as e:
        print(f"⚠️  Polls Routes import error: {e}")
    
    # Hybrid Routes (一時的に無効化)
    try:
        # from routes.hybrid import router as hybrid_router
        # app.include_router(hybrid_router, prefix="/hybrid", tags=["hybrid"])
        print("⚠️ Hybrid Routes は一時的に無効化されています")
    except ImportError as e:
        print(f"⚠️  Hybrid Routes import error: {e}")
    except Exception as e:
        print(f"⚠️  Hybrid Routes general error: {e}")
    
    # Gradio Interface Mount
    try:
        # Gradioインターフェースを作成・マウント
        gradio_interfaces = create_gradio_interfaces()
        app = gr.mount_gradio_app(app, gradio_interfaces, "/gradio")
        print("✅ Gradio app mounted at /gradio")
    except Exception as e:
        print(f"⚠️  Gradio mounting error: {e}")
    
    print("🚀 Laravel風ルーティング統合完了")


def create_gradio_interfaces():
    """
    Gradioインターフェースを作成
    """
    # 基本的なGradioインターフェース例
    def hello_world(name):
        return f"Hello {name}!"
    
    interface = gr.Interface(
        fn=hello_world,
        inputs=gr.Textbox(placeholder="Your name"),
        outputs="text",
        title="FastAPI + Laravel + Gradio Integration",
        description="Laravel風ルーティングシステムでのGradio統合例"
    )
    
    return interface
