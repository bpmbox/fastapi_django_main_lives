"""
🌐 Django Web 専用コントローラー
===============================

Laravel風のDjango Webコントローラー
従来のWebビューとAPIレスポンスの両方に対応
"""

from app.Http.Controllers.HybridController import HybridController
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from typing import Dict, Any, Union
import json
import logging

logger = logging.getLogger(__name__)

class WebController(HybridController):
    """
    Django Web専用のLaravel風コントローラー
    HTMLビューとJSONレスポンスの両方に対応
    """
    
    # クラスメソッドレベルでCSRF免除を適用
    def dispatch(self, request, *args, **kwargs):
        # CSRF免除が必要な場合、個別のメソッドで処理
        return super().dispatch(request, *args, **kwargs)
    
    def __init__(self):
        super().__init__()
        self.template_prefix = "web/"
        
    def django_view(self, request) -> Union[JsonResponse, HttpResponse]:
        """
        Django View - Laravel風のメソッドルーティング
        """
        try:
            if request.method == "GET":
                # GETリクエストの処理
                if request.GET.get('format') == 'json':
                    # JSON レスポンス要求
                    import asyncio
                    data = asyncio.run(self.index())
                    return JsonResponse(data)
                else:
                    # HTML ビュー表示
                    return self.index_view(request)
                    
            elif request.method == "POST":
                # POSTリクエストの処理
                import asyncio
                data = asyncio.run(self.store(request))
                return JsonResponse(data)
                
            elif request.method == "PUT":
                # PUTリクエストの処理（RESTful）
                import asyncio
                resource_id = request.GET.get('id')
                if resource_id:
                    data = asyncio.run(self.update(int(resource_id), request))
                    return JsonResponse(data)
                else:
                    return JsonResponse({"error": "ID required for PUT request"}, status=400)
                    
            elif request.method == "DELETE":
                # DELETEリクエストの処理（RESTful）
                import asyncio
                resource_id = request.GET.get('id')
                if resource_id:
                    data = asyncio.run(self.destroy(int(resource_id)))
                    return JsonResponse(data)
                else:
                    return JsonResponse({"error": "ID required for DELETE request"}, status=400)
            
            return JsonResponse({"error": "Method not allowed"}, status=405)
            
        except Exception as e:
            logger.error(f"Django view error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    
    def index_view(self, request) -> HttpResponse:
        """
        インデックスビュー（HTML）
        Laravel の index ビューに相当
        """
        try:
            import asyncio
            data = asyncio.run(self.index())
            
            context = {
                'title': 'Laravel風 Web インターフェース',
                'data': data,
                'controller_name': self.__class__.__name__
            }
            
            return render(request, f'{self.template_prefix}index.html', context)
            
        except Exception as e:
            logger.error(f"Index view error: {e}")
            return HttpResponse(f"エラーが発生しました: {e}", status=500)
    
    def detail_view(self, request, id: int) -> HttpResponse:
        """
        詳細ビュー（HTML）
        Laravel の show ビューに相当
        """
        try:
            import asyncio
            data = asyncio.run(self.show(id))
            
            context = {
                'title': f'詳細 - ID: {id}',
                'data': data,
                'controller_name': self.__class__.__name__,
                'resource_id': id
            }
            
            return render(request, f'{self.template_prefix}detail.html', context)
            
        except Exception as e:
            logger.error(f"Detail view error: {e}")
            return HttpResponse(f"エラーが発生しました: {e}", status=500)
    
    async def index(self) -> Dict[str, Any]:
        """
        リソース一覧取得
        """
        # デフォルト実装 - 継承先で実装
        return {
            "status": "success",
            "data": [
                {"id": 1, "name": "サンプルリソース1", "type": "web"},
                {"id": 2, "name": "サンプルリソース2", "type": "web"},
            ],
            "message": "Web resources retrieved successfully",
            "controller": self.__class__.__name__
        }
    
    async def store(self, request) -> Dict[str, Any]:
        """
        新規リソース作成
        """
        try:
            # Django request からデータを取得
            if hasattr(request, 'body'):
                body = json.loads(request.body.decode('utf-8'))
            else:
                body = dict(request.POST)
            
            return {
                "status": "success",
                "data": {
                    "id": 999,  # 仮のID
                    "created_data": body,
                    "created_at": "2025-06-13T16:52:00Z"
                },
                "message": "Web resource created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Creation failed: {e}"
            }
    
    async def show(self, id: int) -> Dict[str, Any]:
        """
        特定リソース取得
        """
        return {
            "status": "success",
            "data": {
                "id": id,
                "name": f"Webリソース {id}",
                "type": "web_resource",
                "details": "詳細情報がここに表示されます"
            },
            "message": f"Web resource {id} retrieved successfully"
        }
    
    async def update(self, id: int, request) -> Dict[str, Any]:
        """
        リソース更新
        """
        try:
            if hasattr(request, 'body'):
                body = json.loads(request.body.decode('utf-8'))
            else:
                body = dict(request.POST)
            
            return {
                "status": "success",
                "data": {
                    "id": id,
                    "updated_data": body,
                    "updated_at": "2025-06-13T16:52:00Z"
                },
                "message": f"Web resource {id} updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Update failed: {e}"
            }
    
    async def destroy(self, id: int) -> Dict[str, Any]:
        """
        リソース削除
        """
        return {
            "status": "success",
            "data": {
                "id": id,
                "deleted_at": "2025-06-13T16:52:00Z"
            },
            "message": f"Web resource {id} deleted successfully"
        }

# インスタンス作成
web_controller = WebController()
