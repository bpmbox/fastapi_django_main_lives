"""
🚀 FastAPI 専用コントローラー
===========================

Laravel風のFastAPI RESTful APIコントローラー
"""

from app.Http.Controllers.HybridController import HybridController
from fastapi import Request, HTTPException
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

class FastApiController(HybridController):
    """
    FastAPI専用のLaravel風コントローラー
    RESTful API エンドポイントを提供
    """
    
    def __init__(self):
        super().__init__()
        self.data_store = []  # サンプルデータストア
        
    async def index(self) -> Dict[str, Any]:
        """
        API リソース一覧
        GET /api/resources
        """
        return {
            "status": "success",
            "data": self.data_store,
            "total": len(self.data_store),
            "message": "Resources retrieved successfully"
        }
    
    async def store(self, request: Request) -> Dict[str, Any]:
        """
        新規リソース作成
        POST /api/resources
        """
        try:
            body = await request.json()
            new_id = len(self.data_store) + 1
            new_resource = {
                "id": new_id,
                **body,
                "created_at": "2025-06-13T16:52:00Z"
            }
            self.data_store.append(new_resource)
            
            return {
                "status": "success",
                "data": new_resource,
                "message": "Resource created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating resource: {e}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def show(self, id: int) -> Dict[str, Any]:
        """
        特定リソース取得
        GET /api/resources/{id}
        """
        resource = next((item for item in self.data_store if item["id"] == id), None)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        return {
            "status": "success",
            "data": resource,
            "message": "Resource retrieved successfully"
        }
    
    async def update(self, id: int, request: Request) -> Dict[str, Any]:
        """
        リソース更新
        PUT /api/resources/{id}
        """
        try:
            body = await request.json()
            resource_index = next((i for i, item in enumerate(self.data_store) if item["id"] == id), None)
            
            if resource_index is None:
                raise HTTPException(status_code=404, detail="Resource not found")
            
            # リソース更新
            self.data_store[resource_index].update(body)
            self.data_store[resource_index]["updated_at"] = "2025-06-13T16:52:00Z"
            
            return {
                "status": "success",
                "data": self.data_store[resource_index],
                "message": "Resource updated successfully"
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating resource: {e}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def destroy(self, id: int) -> Dict[str, Any]:
        """
        リソース削除
        DELETE /api/resources/{id}
        """
        resource_index = next((i for i, item in enumerate(self.data_store) if item["id"] == id), None)
        
        if resource_index is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        deleted_resource = self.data_store.pop(resource_index)
        
        return {
            "status": "success",
            "data": deleted_resource,
            "message": "Resource deleted successfully"
        }

# ルーター用のインスタンス作成
fastapi_controller = FastApiController()
router = fastapi_controller.router
