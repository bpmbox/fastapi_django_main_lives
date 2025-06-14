#!/usr/bin/env python3
"""
データベース依存性注入パターン for RPA + AI Debug System
================================================================

DIパターンでデータベース処理を抽象化し、テスタビリティと拡張性を向上
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import asyncio
from dataclasses import dataclass

# ============================================================================
# データモデル定義
# ============================================================================

@dataclass
class DebugRecord:
    """デバッグ記録のデータクラス"""
    id: Optional[int] = None
    timestamp: str = ""
    url: str = ""
    description: str = ""
    selector: Optional[str] = None
    capture_path: str = ""
    analysis_prompt: str = ""
    analysis_result: Optional[str] = None
    status: str = "captured"  # captured, analyzed, resolved
    created_at: str = ""
    updated_at: str = ""

# ============================================================================
# データベース抽象化層
# ============================================================================

class IDebugRepository(ABC):
    """デバッグ記録リポジトリのインターフェース"""
    
    @abstractmethod
    async def save_debug_record(self, record: DebugRecord) -> int:
        """デバッグ記録を保存"""
        pass
    
    @abstractmethod
    async def get_debug_record(self, record_id: int) -> Optional[DebugRecord]:
        """IDでデバッグ記録を取得"""
        pass
    
    @abstractmethod
    async def get_recent_records(self, limit: int = 10) -> List[DebugRecord]:
        """最新のデバッグ記録を取得"""
        pass
    
    @abstractmethod
    async def update_analysis_result(self, record_id: int, analysis_result: str) -> bool:
        """解析結果を更新"""
        pass
    
    @abstractmethod
    async def search_records(self, query: str) -> List[DebugRecord]:
        """デバッグ記録を検索"""
        pass
    
    @abstractmethod
    async def get_records_by_url(self, url: str) -> List[DebugRecord]:
        """URL別のデバッグ記録を取得"""
        pass
    
    @abstractmethod
    async def delete_record(self, record_id: int) -> bool:
        """デバッグ記録を削除"""
        pass

# ============================================================================
# SQLite実装
# ============================================================================

class SQLiteDebugRepository(IDebugRepository):
    """SQLiteベースのデバッグ記録リポジトリ"""
    
    def __init__(self, db_path: str = "/workspaces/fastapi_django_main_live/rpa_debug.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """データベース初期化"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS debug_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT,
                    selector TEXT,
                    capture_path TEXT NOT NULL,
                    analysis_prompt TEXT,
                    analysis_result TEXT,
                    status TEXT DEFAULT 'captured',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # インデックス作成
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON debug_records(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON debug_records(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON debug_records(status)")
            conn.commit()
    
    async def save_debug_record(self, record: DebugRecord) -> int:
        """デバッグ記録を保存"""
        now = datetime.now().isoformat()
        record.created_at = now
        record.updated_at = now
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO debug_records 
                (timestamp, url, description, selector, capture_path, 
                 analysis_prompt, analysis_result, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.timestamp, record.url, record.description, record.selector,
                record.capture_path, record.analysis_prompt, record.analysis_result,
                record.status, record.created_at, record.updated_at
            ))
            conn.commit()
            return cursor.lastrowid
    
    async def get_debug_record(self, record_id: int) -> Optional[DebugRecord]:
        """IDでデバッグ記録を取得"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM debug_records WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            
            if row:
                return DebugRecord(**dict(row))
            return None
    
    async def get_recent_records(self, limit: int = 10) -> List[DebugRecord]:
        """最新のデバッグ記録を取得"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM debug_records 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            return [DebugRecord(**dict(row)) for row in cursor.fetchall()]
    
    async def update_analysis_result(self, record_id: int, analysis_result: str) -> bool:
        """解析結果を更新"""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE debug_records 
                SET analysis_result = ?, status = 'analyzed', updated_at = ?
                WHERE id = ?
            """, (analysis_result, now, record_id))
            conn.commit()
            return cursor.rowcount > 0
    
    async def search_records(self, query: str) -> List[DebugRecord]:
        """デバッグ記録を検索"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM debug_records 
                WHERE description LIKE ? OR url LIKE ? OR analysis_result LIKE ?
                ORDER BY created_at DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            
            return [DebugRecord(**dict(row)) for row in cursor.fetchall()]
    
    async def get_records_by_url(self, url: str) -> List[DebugRecord]:
        """URL別のデバッグ記録を取得"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM debug_records 
                WHERE url = ?
                ORDER BY created_at DESC
            """, (url,))
            
            return [DebugRecord(**dict(row)) for row in cursor.fetchall()]
    
    async def delete_record(self, record_id: int) -> bool:
        """デバッグ記録を削除"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM debug_records WHERE id = ?", (record_id,))
            conn.commit()
            return cursor.rowcount > 0

# ============================================================================
# JSON実装（テスト・開発用）
# ============================================================================

class JSONDebugRepository(IDebugRepository):
    """JSONファイルベースのデバッグ記録リポジトリ（テスト用）"""
    
    def __init__(self, json_path: str = "/workspaces/fastapi_django_main_live/docs/debug_history.json"):
        self.json_path = Path(json_path)
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self._records: List[Dict] = self._load_records()
        self._next_id = max([r.get('id', 0) for r in self._records], default=0) + 1
    
    def _load_records(self) -> List[Dict]:
        """JSONファイルから記録を読み込み"""
        if self.json_path.exists():
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_records(self):
        """JSONファイルに記録を保存"""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self._records, f, indent=2, ensure_ascii=False)
    
    async def save_debug_record(self, record: DebugRecord) -> int:
        """デバッグ記録を保存"""
        now = datetime.now().isoformat()
        record.id = self._next_id
        record.created_at = now
        record.updated_at = now
        
        record_dict = {
            'id': record.id,
            'timestamp': record.timestamp,
            'url': record.url,
            'description': record.description,
            'selector': record.selector,
            'capture_path': record.capture_path,
            'analysis_prompt': record.analysis_prompt,
            'analysis_result': record.analysis_result,
            'status': record.status,
            'created_at': record.created_at,
            'updated_at': record.updated_at
        }
        
        self._records.append(record_dict)
        self._next_id += 1
        self._save_records()
        return record.id
    
    async def get_debug_record(self, record_id: int) -> Optional[DebugRecord]:
        """IDでデバッグ記録を取得"""
        for record_dict in self._records:
            if record_dict.get('id') == record_id:
                return DebugRecord(**record_dict)
        return None
    
    async def get_recent_records(self, limit: int = 10) -> List[DebugRecord]:
        """最新のデバッグ記録を取得"""
        sorted_records = sorted(self._records, key=lambda x: x.get('created_at', ''), reverse=True)
        return [DebugRecord(**record_dict) for record_dict in sorted_records[:limit]]
    
    async def update_analysis_result(self, record_id: int, analysis_result: str) -> bool:
        """解析結果を更新"""
        now = datetime.now().isoformat()
        
        for record_dict in self._records:
            if record_dict.get('id') == record_id:
                record_dict['analysis_result'] = analysis_result
                record_dict['status'] = 'analyzed'
                record_dict['updated_at'] = now
                self._save_records()
                return True
        return False
    
    async def search_records(self, query: str) -> List[DebugRecord]:
        """デバッグ記録を検索"""
        query_lower = query.lower()
        matching_records = []
        
        for record_dict in self._records:
            if (query_lower in record_dict.get('description', '').lower() or
                query_lower in record_dict.get('url', '').lower() or
                query_lower in record_dict.get('analysis_result', '').lower()):
                matching_records.append(DebugRecord(**record_dict))
        
        return sorted(matching_records, key=lambda x: x.created_at, reverse=True)
    
    async def get_records_by_url(self, url: str) -> List[DebugRecord]:
        """URL別のデバッグ記録を取得"""
        matching_records = [
            DebugRecord(**record_dict) 
            for record_dict in self._records
            if record_dict.get('url') == url
        ]
        return sorted(matching_records, key=lambda x: x.created_at, reverse=True)
    
    async def delete_record(self, record_id: int) -> bool:
        """デバッグ記録を削除"""
        for i, record_dict in enumerate(self._records):
            if record_dict.get('id') == record_id:
                del self._records[i]
                self._save_records()
                return True
        return False

# ============================================================================
# サービス層（DIパターン）
# ============================================================================

class DebugHistoryService:
    """デバッグ履歴管理サービス（依存性注入パターン）"""
    
    def __init__(self, repository: IDebugRepository):
        self._repository = repository
    
    async def save_debug_session(self, url: str, description: str, selector: Optional[str], 
                               capture_path: str, analysis_prompt: str) -> int:
        """デバッグセッションを保存"""
        record = DebugRecord(
            timestamp=datetime.now().isoformat(),
            url=url,
            description=description,
            selector=selector,
            capture_path=capture_path,
            analysis_prompt=analysis_prompt,
            status="captured"
        )
        
        return await self._repository.save_debug_record(record)
    
    async def complete_analysis(self, record_id: int, analysis_result: str) -> bool:
        """解析完了を記録"""
        return await self._repository.update_analysis_result(record_id, analysis_result)
    
    async def get_debug_history_formatted(self, limit: int = 10) -> str:
        """フォーマットされたデバッグ履歴を取得"""
        records = await self._repository.get_recent_records(limit)
        
        if not records:
            return "📭 デバッグ履歴はありません"
        
        formatted = "📋 **デバッグ履歴**\n\n"
        
        for i, record in enumerate(records, 1):
            timestamp = record.timestamp[:16].replace("T", " ")
            url_short = record.url[:50] + "..." if len(record.url) > 50 else record.url
            status_emoji = "✅" if record.status == "analyzed" else "📸"
            
            formatted += f"**#{i}** {status_emoji} - {timestamp}\n"
            formatted += f"🌐 URL: {url_short}\n"
            formatted += f"📝 説明: {record.description[:100]}...\n"
            formatted += f"📸 キャプチャ: {Path(record.capture_path).name}\n"
            if record.analysis_result:
                formatted += f"🔍 解析: 完了\n"
            formatted += "\n"
        
        return formatted
    
    async def search_debug_history(self, query: str) -> List[DebugRecord]:
        """デバッグ履歴検索"""
        return await self._repository.search_records(query)
    
    async def get_url_statistics(self, url: str) -> Dict[str, Any]:
        """URL別の統計情報を取得"""
        records = await self._repository.get_records_by_url(url)
        
        total_count = len(records)
        analyzed_count = len([r for r in records if r.status == "analyzed"])
        recent_record = records[0] if records else None
        
        return {
            "url": url,
            "total_captures": total_count,
            "analyzed_captures": analyzed_count,
            "analysis_rate": analyzed_count / total_count if total_count > 0 else 0,
            "last_capture": recent_record.timestamp if recent_record else None
        }

# ============================================================================
# ファクトリーパターン
# ============================================================================

class RepositoryFactory:
    """リポジトリファクトリー"""
    
    @staticmethod
    def create_repository(repo_type: str = "sqlite") -> IDebugRepository:
        """リポジトリを作成"""
        if repo_type == "sqlite":
            return SQLiteDebugRepository()
        elif repo_type == "json":
            return JSONDebugRepository()
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")
    
    @staticmethod
    def create_service(repo_type: str = "sqlite") -> DebugHistoryService:
        """サービスを作成（DI済み）"""
        repository = RepositoryFactory.create_repository(repo_type)
        return DebugHistoryService(repository)

# ============================================================================
# テスト用ユーティリティ
# ============================================================================

async def test_di_pattern():
    """DIパターンのテスト"""
    print("🧪 依存性注入パターンのテスト開始")
    
    # SQLite版でテスト
    sqlite_service = RepositoryFactory.create_service("sqlite")
    
    # デバッグ記録を保存
    record_id = await sqlite_service.save_debug_session(
        url="https://example.com",
        description="テスト用のデバッグセッション",
        selector=".test-element",
        capture_path="/tmp/test_capture.png",
        analysis_prompt="テスト用プロンプト"
    )
    
    print(f"✅ SQLite保存成功: Record ID {record_id}")
    
    # 履歴取得
    history = await sqlite_service.get_debug_history_formatted(5)
    print(f"✅ 履歴取得成功:\n{history}")
    
    # JSON版でテスト
    json_service = RepositoryFactory.create_service("json")
    
    record_id_json = await json_service.save_debug_session(
        url="https://json-test.com",
        description="JSON版テスト",
        selector=None,
        capture_path="/tmp/json_test.png",
        analysis_prompt="JSON用プロンプト"
    )
    
    print(f"✅ JSON保存成功: Record ID {record_id_json}")
    
    # 統計情報テスト
    stats = await sqlite_service.get_url_statistics("https://example.com")
    print(f"✅ 統計情報: {stats}")
    
    print("🎉 DIパターンテスト完了!")

if __name__ == "__main__":
    asyncio.run(test_di_pattern())
