import psycopg2
import os
# PostgreSQLの設定
conn_params = {
    "dbname": "neondb",
    "user": os.getenv("postgre_user"),
    "password": os.getenv("postgre_pass"),
    "host": os.getenv("postgre_host"),
    "port": 5432,
    "sslmode": "require"
}

def initialize_db():
    # PostgreSQLに接続
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # テーブルを作成するSQL文
    create_table_query = """
    CREATE TABLE IF NOT EXISTS chat_history (
        id SERIAL PRIMARY KEY,
        role TEXT,
        type TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)

    # 別のテーブルを作成するSQL文
    create_history_table_query = """
    CREATE TABLE IF NOT EXISTS history (
        id SERIAL PRIMARY KEY,
        role TEXT,
        type TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_history_table_query)

    conn.commit()
    cursor.close()
    conn.close()
    print("データベースとテーブルが作成されました。")

def add_message_to_db(role, message_type, content):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (role, type, content, timestamp) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
        (role, message_type, content)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_recent_messages(limit=5):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, type, content FROM history ORDER BY timestamp DESC LIMIT %s",
        (limit,)
    )
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages[::-1]  # 最新のlimit件を取得して逆順にする

# データベースの初期化
#initialize_db()
