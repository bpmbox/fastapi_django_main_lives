"""
Application Configuration
========================

Laravel風の設定管理
"""

import os
from typing import Dict, Any

# アプリケーション設定
APP_CONFIG = {
    "name": os.getenv("APP_NAME", "FastAPI Laravel"),
    "env": os.getenv("APP_ENV", "development"),
    "debug": os.getenv("APP_DEBUG", "true").lower() == "true",
    "url": os.getenv("APP_URL", "http://localhost:8000"),
    "timezone": "UTC",
}

# データベース設定
DATABASE_CONFIG = {
    "default": "sqlite",
    "connections": {
        "sqlite": {
            "driver": "sqlite",
            "database": os.getenv("DB_DATABASE", "database.sqlite"),
        },
        "mysql": {
            "driver": "mysql",
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "database": os.getenv("DB_DATABASE", "fastapi_laravel"),
            "username": os.getenv("DB_USERNAME", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
        },
        "postgresql": {
            "driver": "postgresql",
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DB_DATABASE", "fastapi_laravel"),
            "username": os.getenv("DB_USERNAME", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
        }
    }
}

# Redis設定
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "127.0.0.1"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "password": os.getenv("REDIS_PASSWORD", None),
    "database": int(os.getenv("REDIS_DB", "0")),
}

# ログ設定
LOGGING_CONFIG = {
    "default": "stack",
    "channels": {
        "stack": {
            "driver": "stack",
            "channels": ["single"],
        },
        "single": {
            "driver": "single",
            "path": "storage/logs/laravel.log",
            "level": "debug",
        },
    }
}

def get_config(key: str, default: Any = None) -> Any:
    """
    設定値を取得
    
    Args:
        key: 設定キー (例: "app.name", "database.default")
        default: デフォルト値
    
    Returns:
        設定値
    """
    keys = key.split(".")
    
    if keys[0] == "app":
        config = APP_CONFIG
    elif keys[0] == "database":
        config = DATABASE_CONFIG
    elif keys[0] == "redis":
        config = REDIS_CONFIG
    elif keys[0] == "logging":
        config = LOGGING_CONFIG
    else:
        return default
    
    try:
        for k in keys[1:]:
            config = config[k]
        return config
    except (KeyError, TypeError):
        return default
