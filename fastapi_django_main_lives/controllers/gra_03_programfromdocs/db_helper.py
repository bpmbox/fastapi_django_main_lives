#!/usr/bin/env python3
"""
統合データベースヘルパー関数
全てのGradioコントローラー用の統一データベースアクセス
"""

import sqlite3
import os
import sys

# パスを追加してconfig/database.pyにアクセス
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.append(project_root)

def get_unified_db_connection(db_name='approval_system'):
    """統一されたデータベース接続を取得"""
    try:
        from config.database import get_db_connection
        return get_db_connection(db_name)
    except ImportError:
        # フォールバック: 直接データベースパスを指定
        db_path = f"/workspaces/fastapi_django_main_lives/database/{db_name}.db"
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return sqlite3.connect(db_path)

def ensure_unified_tables():
    """統一されたテーブル初期化"""
    try:
        from config.database import ensure_tables_exist
        ensure_tables_exist()
    except ImportError:
        # フォールバック処理
        pass
