#!/usr/bin/env python3
"""
データベース初期化スクリプト
必要なテーブルとサンプルデータを作成します
"""
import sqlite3
import os
from datetime import datetime

def create_databases():
    """必要なデータベースとテーブルを作成"""
    try:
        # 現在のディレクトリ（database/）に作成
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f'📂 データベース作成ディレクトリ: {current_dir}')

        # プロンプトデータベースを作成
        print('📋 プロンプトデータベースを作成中...')
        prompts_db_path = os.path.join(current_dir, 'prompts.db')
        conn = sqlite3.connect(prompts_db_path)
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

        # テストデータを挿入
        cursor.execute('''
            INSERT OR IGNORE INTO prompts (id, title, content, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, '初回テストプロンプト', 'Hello World を表示するシンプルなPythonスクリプトを作成してください。', 'テスト', datetime.now(), datetime.now()))

        conn.commit()
        conn.close()
        print('✅ プロンプトデータベース作成完了')

        # 承認システムデータベースを作成
        print('📋 承認システムデータベースを作成中...')
        approval_db_path = os.path.join(current_dir, 'approval_system.db')
        conn = sqlite3.connect(approval_db_path)
        cursor = conn.cursor()

        # 承認キューテーブル
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

        # 旧形式の承認テーブル（後方互換性のため）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                approval_status TEXT,
                reason TEXT,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print('✅ 承認システムデータベース作成完了')

        # チャット履歴データベースを作成
        print('📋 チャット履歴データベースを作成中...')
        chat_db_path = os.path.join(current_dir, 'chat_history.db')
        conn = sqlite3.connect(chat_db_path)
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
        conn.close()
        print('✅ チャット履歴データベース作成完了')

        print('🎉 全てのデータベースが正常に作成されました!')
        
        # 確認
        if os.path.exists(prompts_db_path):
            print(f'✅ prompts.db 作成確認: {prompts_db_path}')
        if os.path.exists(approval_db_path):
            print(f'✅ approval_system.db 作成確認: {approval_db_path}')
        if os.path.exists(chat_db_path):
            print(f'✅ chat_history.db 作成確認: {chat_db_path}')
            
        return True
        
    except Exception as e:
        print(f'❌ エラーが発生しました: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_databases()
