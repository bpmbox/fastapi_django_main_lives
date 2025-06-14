"""
🛣️ Laravel風 統合ルーティングシステム
====================================

Django + FastAPI + Gradio を統合したルーティング
Laravel風のルーティング体験を提供
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from django.urls import path, include
from django.http import JsonResponse
import gradio as gr
from typing import Dict, Any, List
import logging

# コントローラーのインポート
from app.Http.Controllers.Api.FastApiController import fastapi_controller
from app.Http.Controllers.Web.WebController import web_controller
from app.Http.Controllers.Gradio.GradioController import gradio_controller

logger = logging.getLogger(__name__)

class LaravelStyleRouter:
    """Laravel風ルーティングシステム"""
    
    def __init__(self):
        self.fastapi_app = FastAPI(
            title="Laravel風 統合API",
            description="Django + FastAPI + Gradio ハイブリッドシステム",
            version="1.0.0"
        )
        self.setup_middleware()
        self.setup_routes()
        
    def setup_middleware(self):
        """ミドルウェア設定"""
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """ルーティング設定"""
        
        # API Routes (FastAPI)
        self.fastapi_app.include_router(
            fastapi_controller.router,
            prefix="/api/v1",
            tags=["FastAPI"]
        )
        
        # Gradio API Routes
        self.fastapi_app.include_router(
            gradio_controller.router,
            prefix="/api/gradio",
            tags=["Gradio"]
        )
        
        # Root endpoints
        @self.fastapi_app.get("/")
        async def root():
            return {
                "message": "🏗️ Laravel風 統合システム",
                "services": {
                    "fastapi": "/api/v1",
                    "gradio_api": "/api/gradio", 
                    "gradio_ui": "/gradio",
                    "django_web": "/web",
                    "docs": "/docs"
                },
                "version": "1.0.0"
            }
        
        @self.fastapi_app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "services": {
                    "fastapi": "running",
                    "gradio": "running",
                    "django": "running"
                }
            }

# Django URLパターン
def django_url_patterns():
    """Django URL パターンを生成"""
    from django.urls import path
    
    return [
        # Web Routes (Django)
        path('web/', web_controller.django_view, name='web_index'),
        path('web/<int:id>/', web_controller.detail_view, name='web_detail'),
        
        # API compatibility routes
        path('api/web/', web_controller.django_view, name='web_api'),
    ]

def setup_gradio_interface():
    """Gradio インターフェースをセットアップ"""
    try:
        # タブ形式の統合インターフェース作成
        interface = gradio_controller.create_tabbed_interface()
        
        # Gradio アプリケーションを /gradio パスでマウント
        gradio_app = interface.queue()
        
        return gradio_app
        
    except Exception as e:
        logger.error(f"Gradio setup error: {e}")
        
        # エラー時は基本インターフェースを作成
        basic_interface = gr.Interface(
            fn=lambda x: f"システムエラー: {e}",
            inputs=gr.Textbox(label="入力"),
            outputs=gr.Textbox(label="出力"),
            title="🚨 システムエラー"
        )
        return basic_interface

# Laravel風ルーター設定
class RouteServiceProvider:
    """Laravel風 ルートサービスプロバイダー"""
    
    @staticmethod
    def register_api_routes(app: FastAPI):
        """API ルートを登録"""
        
        # RESTful API routes
        api_routes = [
            # FastAPI Routes
            {
                "path": "/api/v1/resources",
                "controller": fastapi_controller,
                "methods": ["GET", "POST"]
            },
            {
                "path": "/api/v1/resources/{id}",
                "controller": fastapi_controller,
                "methods": ["GET", "PUT", "DELETE"]
            },
            
            # Gradio API Routes
            {
                "path": "/api/gradio/interfaces",
                "controller": gradio_controller,
                "methods": ["GET", "POST"]
            },
            {
                "path": "/api/gradio/interfaces/{id}",
                "controller": gradio_controller,
                "methods": ["GET", "PUT", "DELETE"]
            }
        ]
        
        logger.info(f"Registered {len(api_routes)} API route groups")
        return api_routes
    
    @staticmethod
    def register_web_routes():
        """Web ルートを登録"""
        
        web_routes = [
            # Laravel風 Web Routes
            ("web.index", "/web/", "WebController@index"),
            ("web.show", "/web/{id}/", "WebController@show"),
            ("web.create", "/web/create/", "WebController@create"),
            ("web.store", "/web/store/", "WebController@store"),
            ("web.edit", "/web/{id}/edit/", "WebController@edit"),
            ("web.update", "/web/{id}/update/", "WebController@update"),
            ("web.destroy", "/web/{id}/destroy/", "WebController@destroy"),
        ]
        
        logger.info(f"Registered {len(web_routes)} web routes")
        return web_routes

# インスタンス作成
laravel_router = LaravelStyleRouter()
app = laravel_router.fastapi_app

# Gradio インターフェース
gradio_app = setup_gradio_interface()

# Django URL patterns
django_urlpatterns = django_url_patterns()

# Export for use in other modules
__all__ = [
    'app',
    'gradio_app', 
    'django_urlpatterns',
    'laravel_router',
    'RouteServiceProvider'
]
