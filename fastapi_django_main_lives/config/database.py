import os
import sqlite3
from datetime import datetime

# データベースファイルのベースパス
DB_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")

# 各データベースファイルのパス
DATABASE_PATHS = {
    'prompts': os.path.join(DB_BASE_PATH, 'prompts.db'),
    'approval_system': os.path.join(DB_BASE_PATH, 'approval_system.db'),
    'chat_history': os.path.join(DB_BASE_PATH, 'chat_history.db'),
    'conversation_history': os.path.join(DB_BASE_PATH, 'conversation_history.db'),
    'github_issues': os.path.join(DB_BASE_PATH, 'github_issues.db'),
    'github_issues_automation': os.path.join(DB_BASE_PATH, 'github_issues_automation.db'),
    'rpa_history': os.path.join(DB_BASE_PATH, 'rpa_history.db'),
    'rpa_debug': os.path.join(DB_BASE_PATH, 'rpa_debug.db'),
    'ai_long_term_memory': os.path.join(DB_BASE_PATH, 'ai_long_term_memory.db'),
    'simple_ai_chat': os.path.join(DB_BASE_PATH, 'simple_ai_chat.db'),
    'users': os.path.join(DB_BASE_PATH, 'users.db')
}

def get_db_connection(db_name='chat_history'):
    """
    データベース接続を取得
    
    Args:
        db_name: データベース名
    
    Returns:
        sqlite3.Connection: データベース接続
    """
    db_path = get_db_path(db_name)
    return sqlite3.connect(db_path)

def get_db_path(db_name):
    """データベースパスを取得"""
    if db_name in DATABASE_PATHS:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(DATABASE_PATHS[db_name]), exist_ok=True)
        return DATABASE_PATHS[db_name]
    else:
        # 従来の形式（ルート直下）をdatabase/配下に変更
        if db_name.endswith('.db'):
            db_path = os.path.join(DB_BASE_PATH, db_name)
        else:
            db_path = os.path.join(DB_BASE_PATH, f"{db_name}.db")
        
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return db_path

def add_chat_message(role, message_type, content, db_name='chat_history'):
    """チャットメッセージを追加"""
    with get_db_connection(db_name) as conn:
        cursor = conn.cursor()
        # テーブルが存在しない場合は作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                type TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            INSERT INTO history (role, type, content)
            VALUES (?, ?, ?)
        ''', (role, message_type, content))
        conn.commit()

def get_chat_history(limit=50, db_name='chat_history'):
    """チャット履歴を取得"""
    with get_db_connection(db_name) as conn:
        cursor = conn.cursor()
        # テーブルが存在しない場合は作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                type TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            SELECT role, type, content, timestamp
            FROM history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

def ensure_tables_exist():
    """全てのテーブルが存在することを確認"""
    # チャット履歴テーブル確認
    with get_db_connection('chat_history') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                type TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    
    # プロンプトテーブル確認
    with get_db_connection('prompts') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    
    # 承認システムテーブル確認
    with get_db_connection('approval_system') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approval_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_title TEXT NOT NULL,
                issue_body TEXT NOT NULL,
                requester TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                approval_status TEXT DEFAULT 'pending_review',
                github_repo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP,
                approved_by TEXT,
                reviewer_notes TEXT
            )
        ''')
        conn.commit()

# 後方互換性のための関数
def get_legacy_db_path(filename):
    """従来のパス指定を新しいパスに変換"""
    if filename.startswith('./') or filename.startswith('../'):
        # 相対パスの場合
        basename = os.path.basename(filename)
        return get_db_path(basename)
    elif '/' not in filename:
        # ファイル名のみの場合
        return get_db_path(filename)
    else:
        # 絶対パスの場合はそのまま
        return filename

if __name__ == "__main__":
    print("🔧 データベース設定テスト...")
    ensure_tables_exist()
    print("✅ 全てのテーブルが正常に作成されました")
    
    # テストデータ追加
    add_chat_message("user", "message", "テストメッセージ")
    
    # 履歴取得テスト
    history = get_chat_history(5)
    print(f"📊 履歴件数: {len(history)}")
    for row in history:
        print(f"  {row[0]}: {row[2][:50]}...")
