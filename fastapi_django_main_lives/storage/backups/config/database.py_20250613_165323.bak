import os

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

def get_db_path(db_name):
    """データベースパスを取得"""
    if db_name in DATABASE_PATHS:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(DATABASE_PATHS[db_name]), exist_ok=True)
        return DATABASE_PATHS[db_name]
    else:
        # 従来の形式（ルート直下）をdatabase/配下に変更
        if db_name.endswith('.db'):
            return os.path.join(DB_BASE_PATH, db_name)
        else:
            return os.path.join(DB_BASE_PATH, f"{db_name}.db")

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
