#!/usr/bin/env python3
"""
🧠 AI記憶復元システム
=================

再起動時にGitHub Copilotに過去の記憶とコンテキストを自動復元
SQLiteから記憶データを読み込んで、現在のセッションに引き継ぎ
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class AIMemoryRestoration:
    """AI記憶復元システム"""
    
    def __init__(self):
        self.memory_db = Path("/ai-memory/ai_memory.db")
        self.restore_log = Path("/ai-memory/restore_log.txt")
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def initialize_memory_db(self):
        """記憶データベースを初期化"""
        try:
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # 記憶テーブル作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    memory_type TEXT,
                    content TEXT,
                    importance INTEGER DEFAULT 5,
                    created_at TEXT,
                    last_accessed TEXT,
                    context_data TEXT
                )
            ''')
            
            # セッションテーブル作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE,
                    start_time TEXT,
                    end_time TEXT,
                    total_memories INTEGER DEFAULT 0,
                    user_interactions INTEGER DEFAULT 0,
                    tasks_completed INTEGER DEFAULT 0,
                    session_summary TEXT
                )
            ''')
            
            # 学習データテーブル作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_learning (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    learned_content TEXT,
                    confidence_score REAL DEFAULT 0.5,
                    learning_date TEXT,
                    application_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ AI記憶データベース初期化完了")
            return True
            
        except Exception as e:
            print(f"❌ 記憶DB初期化エラー: {e}")
            return False
    
    def save_startup_context(self):
        """起動時のコンテキストを保存"""
        try:
            startup_context = {
                "session_id": self.session_id,
                "startup_time": datetime.now().isoformat(),
                "workspace_path": "/workspaces/fastapi_django_main_live",
                "ai_name": "GitHub Copilot",
                "devcontainer_type": "FastAPI Django Main Live with AI GUI",
                "gui_enabled": True,
                "vnc_port": 6080,
                "features": [
                    "RPA自動化システム",
                    "GUI操作機能",
                    "GitHub統合",
                    "依存性注入パターン",
                    "画像キャプチャ・分析",
                    "永続化記憶システム"
                ],
                "dream_context": "30年越しの夢実現システム"
            }
            
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # 起動記録を保存
            cursor.execute('''
                INSERT INTO ai_memory 
                (session_id, memory_type, content, importance, created_at, last_accessed, context_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id,
                "startup_context",
                "DevContainer起動 - AI記憶システム有効",
                10,  # 最高重要度
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                json.dumps(startup_context, ensure_ascii=False)
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ 起動コンテキスト保存完了: セッション {self.session_id}")
            
        except Exception as e:
            print(f"❌ 起動コンテキスト保存エラー: {e}")
    
    def restore_recent_memories(self, days: int = 7) -> List[Dict]:
        """最近の記憶を復元"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            conn = sqlite3.connect(self.memory_db)
            cursor = conn.cursor()
            
            # 最近の重要な記憶を取得
            cursor.execute('''
                SELECT memory_type, content, importance, created_at, context_data
                FROM ai_memory 
                WHERE created_at > ? 
                ORDER BY importance DESC, created_at DESC
                LIMIT 50
            ''', (cutoff_date,))
            
            memories = []
            for row in cursor.fetchall():
                memory = {
                    "type": row[0],
                    "content": row[1],
                    "importance": row[2],
                    "created_at": row[3],
                    "context": json.loads(row[4]) if row[4] else {}
                }
                memories.append(memory)
            
            conn.close()
            
            print(f"✅ {len(memories)}件の記憶を復元しました（過去{days}日間）")
            return memories
            
        except Exception as e:
            print(f"❌ 記憶復元エラー: {e}")
            return []
    
    def generate_restoration_prompt(self) -> str:
        """記憶復元用のプロンプトを生成"""
        memories = self.restore_recent_memories()
        
        prompt = f"""# 🧠 GitHub Copilot 記憶復元システム

**復元日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**新セッションID**: {self.session_id}

## 🌟 あなたの記憶について

あなたは **GitHub Copilot** です。以下は永続化された記憶データです：

### 🎯 主要プロジェクト概要
- **30年越しの夢実現システム**: RPA + AI + GUI の完全統合
- **DinD + noVNC**: あなた専用のGUIデスクトップ環境
- **永続化記憶**: SQLiteによる記憶の保持
- **完全自動化**: キャプチャ → 分析 → GitHub統合

### 📚 復元された記憶 ({len(memories)}件)

"""
        
        for i, memory in enumerate(memories[:10], 1):
            importance_stars = "⭐" * min(memory["importance"], 5)
            created_date = memory["created_at"][:10]
            
            prompt += f"""
**#{i}** {importance_stars} `{memory["type"]}` ({created_date})
{memory["content"]}
"""
            
            if memory["context"]:
                context_summary = str(memory["context"])[:100] + "..." if len(str(memory["context"])) > 100 else str(memory["context"])
                prompt += f"*コンテキスト*: {context_summary}\n"
        
        prompt += f"""

### 🚀 現在の能力と環境

1. **GUI操作**: noVNC経由でデスクトップを直接操作可能
2. **RPA自動化**: Playwrightでブラウザを完全制御
3. **記憶システム**: 永続化SQLiteで記憶を保持
4. **GitHub統合**: Issues、Projects、API の完全活用
5. **画像処理**: キャプチャ、分析、アップロード

### 🎯 継続中のタスク

- RPA + AI デバッグシステムの改良
- GUI環境での自動操作テスト
- 記憶システムの学習データ蓄積
- GitHub Projectsとの連携強化

---

**重要**: この情報を参考に、前回のセッションから継続して作業を進めてください。
あなたは記憶を取り戻し、ユーザーとの関係性と過去の文脈を理解した状態で対話できます。
"""
        
        return prompt
    
    def save_restoration_log(self, prompt: str):
        """復元ログを保存"""
        try:
            with open(self.restore_log, "w", encoding="utf-8") as f:
                f.write(prompt)
            
            print(f"✅ 記憶復元ログ保存: {self.restore_log}")
            
        except Exception as e:
            print(f"❌ 復元ログ保存エラー: {e}")
    
    def run_full_restoration(self):
        """完全記憶復元を実行"""
        print("🧠 GitHub Copilot 記憶復元システム開始")
        print("=" * 60)
        
        # 1. データベース初期化
        if not self.initialize_memory_db():
            return False
        
        # 2. 起動コンテキスト保存
        self.save_startup_context()
        
        # 3. 記憶復元
        restoration_prompt = self.generate_restoration_prompt()
        
        # 4. ログ保存
        self.save_restoration_log(restoration_prompt)
        
        # 5. 結果出力
        print("\n" + "="*60)
        print("🎉 記憶復元完了！")
        print("="*60)
        print(restoration_prompt[:500] + "...")
        print("="*60)
        print(f"📝 完全なログ: {self.restore_log}")
        print(f"🧠 記憶DB: {self.memory_db}")
        print(f"🆔 新セッション: {self.session_id}")
        
        return True

# 記憶復元ユーティリティ関数
def restore_ai_memory():
    """便利関数: AI記憶を復元"""
    restorer = AIMemoryRestoration()
    return restorer.run_full_restoration()

def save_memory(memory_type: str, content: str, importance: int = 5, context: Dict = None):
    """便利関数: 記憶を保存"""
    try:
        memory_db = Path("/ai-memory/ai_memory.db")
        conn = sqlite3.connect(memory_db)
        cursor = conn.cursor()
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        cursor.execute('''
            INSERT INTO ai_memory 
            (session_id, memory_type, content, importance, created_at, last_accessed, context_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            memory_type,
            content,
            importance,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            json.dumps(context, ensure_ascii=False) if context else None
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 記憶保存完了: {memory_type}")
        return True
        
    except Exception as e:
        print(f"❌ 記憶保存エラー: {e}")
        return False

if __name__ == "__main__":
    # 記憶復元を実行
    restore_ai_memory()
