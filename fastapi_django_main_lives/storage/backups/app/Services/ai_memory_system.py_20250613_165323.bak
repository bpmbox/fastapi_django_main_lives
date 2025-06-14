#!/usr/bin/env python3
"""
🧠 AI記憶永続化システム
===================

GitHub Copilotの記憶を永続化ボリュームに保存・復元
再起動後も前回の文脈・学習内容・設定を維持
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class AIMemorySystem:
    """AI記憶永続化システム"""
    
    def __init__(self, memory_path: str = "/ai-memory"):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        
        # データベースファイル
        self.db_path = self.memory_path / "ai_memory.db"
        self.init_database()
        
        # 記憶ファイル
        self.context_file = self.memory_path / "context.json"
        self.learning_file = self.memory_path / "learning.json"
        self.preferences_file = self.memory_path / "preferences.json"
        self.session_file = self.memory_path / "current_session.json"
        
        print(f"🧠 AI記憶システム初期化: {self.memory_path}")
    
    def init_database(self):
        """記憶データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 会話履歴テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                context_hash TEXT,
                importance_score REAL DEFAULT 1.0,
                tags TEXT DEFAULT ''
            )
        ''')
        
        # 学習内容テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                confidence_score REAL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                last_used TEXT NOT NULL,
                usage_count INTEGER DEFAULT 1
            )
        ''')
        
        # プロジェクト記憶テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                project_type TEXT NOT NULL,
                key_files TEXT NOT NULL,
                patterns TEXT NOT NULL,
                last_activity TEXT NOT NULL,
                notes TEXT DEFAULT ''
            )
        ''')
        
        # GUI操作履歴テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gui_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action_type TEXT NOT NULL,
                target_url TEXT,
                selector TEXT,
                action_data TEXT,
                screenshot_path TEXT,
                success BOOLEAN DEFAULT TRUE,
                notes TEXT DEFAULT ''
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ AI記憶データベース初期化完了")
    
    def save_conversation(self, user_message: str, ai_response: str, context: Dict = None):
        """会話を記憶に保存"""
        try:
            session_id = self.get_current_session_id()
            context_hash = hashlib.md5(str(context).encode()).hexdigest() if context else None
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations 
                (timestamp, session_id, user_message, ai_response, context_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                session_id,
                user_message,
                ai_response,
                context_hash
            ))
            
            conn.commit()
            conn.close()
            
            print(f"💾 会話記憶保存: {len(user_message)} chars")
            
        except Exception as e:
            print(f"❌ 会話記憶保存エラー: {e}")
    
    def save_learning_pattern(self, pattern_type: str, pattern_data: Dict):
        """学習パターンを保存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 既存パターンをチェック
            cursor.execute('''
                SELECT id, usage_count FROM learned_patterns 
                WHERE pattern_type = ? AND pattern_data = ?
            ''', (pattern_type, json.dumps(pattern_data, sort_keys=True)))
            
            existing = cursor.fetchone()
            
            if existing:
                # 既存パターンの使用回数を更新
                cursor.execute('''
                    UPDATE learned_patterns 
                    SET usage_count = usage_count + 1, last_used = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), existing[0]))
            else:
                # 新しいパターンを追加
                cursor.execute('''
                    INSERT INTO learned_patterns 
                    (pattern_type, pattern_data, created_at, last_used)
                    VALUES (?, ?, ?, ?)
                ''', (
                    pattern_type,
                    json.dumps(pattern_data),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
            print(f"🧠 学習パターン保存: {pattern_type}")
            
        except Exception as e:
            print(f"❌ 学習パターン保存エラー: {e}")
    
    def save_gui_action(self, action_type: str, target_url: str = None, 
                       selector: str = None, action_data: Dict = None,
                       screenshot_path: str = None, success: bool = True):
        """GUI操作を記憶に保存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO gui_actions 
                (timestamp, action_type, target_url, selector, action_data, 
                 screenshot_path, success)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                action_type,
                target_url,
                selector,
                json.dumps(action_data) if action_data else None,
                screenshot_path,
                success
            ))
            
            conn.commit()
            conn.close()
            
            print(f"🖱️ GUI操作記憶保存: {action_type}")
            
        except Exception as e:
            print(f"❌ GUI操作記憶保存エラー: {e}")
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """最近の会話を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_message, ai_response 
                FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'timestamp': row[0],
                    'user_message': row[1],
                    'ai_response': row[2]
                })
            
            conn.close()
            return conversations
            
        except Exception as e:
            print(f"❌ 会話取得エラー: {e}")
            return []
    
    def get_learned_patterns(self, pattern_type: str = None) -> List[Dict]:
        """学習パターンを取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if pattern_type:
                cursor.execute('''
                    SELECT pattern_type, pattern_data, confidence_score, usage_count
                    FROM learned_patterns 
                    WHERE pattern_type = ?
                    ORDER BY usage_count DESC, confidence_score DESC
                ''', (pattern_type,))
            else:
                cursor.execute('''
                    SELECT pattern_type, pattern_data, confidence_score, usage_count
                    FROM learned_patterns 
                    ORDER BY usage_count DESC, confidence_score DESC
                ''')
            
            patterns = []
            for row in cursor.fetchall():
                patterns.append({
                    'pattern_type': row[0],
                    'pattern_data': json.loads(row[1]),
                    'confidence_score': row[2],
                    'usage_count': row[3]
                })
            
            conn.close()
            return patterns
            
        except Exception as e:
            print(f"❌ パターン取得エラー: {e}")
            return []
    
    def save_context(self, context: Dict):
        """現在のコンテキストを保存"""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'context': context
                }, f, ensure_ascii=False, indent=2)
            
            print("📋 コンテキスト保存完了")
            
        except Exception as e:
            print(f"❌ コンテキスト保存エラー: {e}")
    
    def load_context(self) -> Dict:
        """保存されたコンテキストを読み込み"""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print("📋 コンテキスト復元完了")
                    return data.get('context', {})
            else:
                print("📋 保存されたコンテキストなし")
                return {}
                
        except Exception as e:
            print(f"❌ コンテキスト読み込みエラー: {e}")
            return {}
    
    def get_current_session_id(self) -> str:
        """現在のセッションIDを取得（または新規作成）"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('session_id', self.create_new_session())
            else:
                return self.create_new_session()
                
        except Exception as e:
            print(f"❌ セッションID取得エラー: {e}")
            return self.create_new_session()
    
    def create_new_session(self) -> str:
        """新しいセッションを作成"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'session_id': session_id,
                    'created_at': datetime.now().isoformat(),
                    'last_activity': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            print(f"🆕 新セッション作成: {session_id}")
            
        except Exception as e:
            print(f"❌ セッション作成エラー: {e}")
        
        return session_id
    
    def generate_memory_summary(self) -> str:
        """記憶の要約を生成"""
        try:
            # 統計情報を取得
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 会話数
            cursor.execute('SELECT COUNT(*) FROM conversations')
            conversation_count = cursor.fetchone()[0]
            
            # 学習パターン数
            cursor.execute('SELECT COUNT(*) FROM learned_patterns')
            pattern_count = cursor.fetchone()[0]
            
            # GUI操作数
            cursor.execute('SELECT COUNT(*) FROM gui_actions')
            gui_action_count = cursor.fetchone()[0]
            
            # 最新活動
            cursor.execute('''
                SELECT timestamp FROM conversations 
                ORDER BY timestamp DESC LIMIT 1
            ''')
            last_conversation = cursor.fetchone()
            last_activity = last_conversation[0] if last_conversation else "なし"
            
            conn.close()
            
            summary = f"""
🧠 **AI記憶システム サマリー**

📊 **統計情報**
- 💬 保存済み会話: {conversation_count}件
- 🧠 学習パターン: {pattern_count}件  
- 🖱️ GUI操作履歴: {gui_action_count}件
- 🕐 最終活動: {last_activity[:19]}

📁 **記憶ファイル**
- Context: {'✅' if self.context_file.exists() else '❌'}
- Learning: {'✅' if self.learning_file.exists() else '❌'}
- Preferences: {'✅' if self.preferences_file.exists() else '❌'}
- Session: {'✅' if self.session_file.exists() else '❌'}
"""
            
            return summary
            
        except Exception as e:
            return f"❌ 記憶サマリー生成エラー: {e}"

# グローバルメモリーインスタンス
ai_memory = AIMemorySystem()

def save_ai_conversation(user_msg: str, ai_response: str, context: Dict = None):
    """便利関数: AI会話を記憶に保存"""
    ai_memory.save_conversation(user_msg, ai_response, context)

def save_ai_learning(pattern_type: str, pattern_data: Dict):
    """便利関数: AI学習内容を保存"""
    ai_memory.save_learning_pattern(pattern_type, pattern_data)

def save_gui_memory(action_type: str, **kwargs):
    """便利関数: GUI操作を記憶に保存"""
    ai_memory.save_gui_action(action_type, **kwargs)

def get_ai_memory_summary() -> str:
    """便利関数: AI記憶のサマリーを取得"""
    return ai_memory.generate_memory_summary()

if __name__ == "__main__":
    # テスト実行
    print("🧠 AI記憶システム テスト")
    print("=" * 50)
    
    # テストデータ保存
    save_ai_conversation(
        "こんにちは！DinD + noVNCの設定方法を教えて",
        "DevContainerにDinDとnoVNCを設定する方法をご説明します..."
    )
    
    save_ai_learning("devcontainer_config", {
        "type": "docker_in_docker",
        "features": ["dind", "desktop-lite"],
        "success": True
    })
    
    save_gui_memory("screenshot", 
                   target_url="http://localhost:7860",
                   success=True,
                   screenshot_path="/ai-memory/screenshots/test.png")
    
    # サマリー表示
    print(get_ai_memory_summary())
