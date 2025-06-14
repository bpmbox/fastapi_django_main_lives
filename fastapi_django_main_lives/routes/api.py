"""
API Routes
==========

RESTful API用のルーティング
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

router = APIRouter()

# サンプルデータ
users_data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]

@router.get("/")
async def api_root() -> Dict[str, Any]:
    """
    API ルート
    """
    return {
        "message": "FastAPI Laravel API",
        "version": "1.0.0",
        "endpoints": [
            "/api/users",
            "/api/users/{id}",
            "/api/health"
        ]
    }

@router.get("/users")
async def get_users() -> List[Dict[str, Any]]:
    """
    ユーザー一覧取得
    """
    return users_data

@router.get("/users/{user_id}")
async def get_user(user_id: int) -> Dict[str, Any]:
    """
    特定ユーザー取得
    """
    user = next((u for u in users_data if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users")
async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ユーザー作成
    """
    new_id = max(u["id"] for u in users_data) + 1 if users_data else 1
    new_user = {
        "id": new_id,
        "name": user_data.get("name", ""),
        "email": user_data.get("email", "")
    }
    users_data.append(new_user)
    return {"message": "User created", "user": new_user}

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    API ヘルスチェック
    """
    return {
        "status": "healthy",
        "service": "FastAPI Laravel API",
        "timestamp": "2025-06-13T16:30:00Z"
    }
