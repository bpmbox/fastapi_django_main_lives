import pandas as pd
import re
import os
from sqlalchemy import create_engine, inspect, Table, MetaData, Column, Integer, String, text
import psycopg2

# チャット履歴ファイルを読み込む関数（最初の3行をスキップ）
def load_chat_history(file_path):
    return pd.read_csv(file_path, skiprows=3)

# 個人情報をマスクする関数
def mask_personal_info(text):
    # 電話番号のマスク
    text = re.sub(r'\b\d{2,4}-\d{2,4}-\d{4}\b', '[電話番号]', text)
    
    # メールアドレスのマスク
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[メールアドレス]', text)
    
    # 名前のマスク（例として"えみいわし"をマスク）
    names = ['えみいわし']
    for name in names:
        text = re.sub(r'\b' + name + r'\b', '[名前]', text)
    
    return text

# データフレームの特定の列の個人情報をマスクする関数
def mask_specific_columns(df, columns):
    for column in columns:
        df[column] = df[column].astype(str).apply(mask_personal_info)
    return df

# データベースに接続する関数
def connect_to_db():
    conn = psycopg2.connect(
        dbname="neondb",
        user=os.getenv("postgre_user"),
        password=os.getenv("postgre_pass"),
        host=os.getenv("postgre_host"),
        port=5432,
        sslmode="require"
    )
    return conn

# フォルダー内のすべてのCSVファイルを処理し、PostgreSQLにインポートする関数
def process_and_import_csv_folder(folder_path, engine):
    # フォルダー内のすべてのCSVファイルを取得
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        
        # チャット履歴を読み込み、特定の列の個人情報をマスク
        chat_history_df = load_chat_history(file_path)
        columns_to_mask = ['送信者タイプ', '送信者名', '送信日', '送信時刻', '内容']
        masked_chat_history_df = mask_specific_columns(chat_history_df, columns_to_mask)
        
        # マスクされたデータをPostgreSQLにインポート
        masked_chat_history_df.to_sql('fasis_chat_history', engine, if_exists='append', index=False)

# ファイルパスの設定
folder_path = '/home/user/app/polls/databases'  # CSVファイルが格納されているフォルダーのパス

# データベースの接続設定
engine = create_engine('postgresql+psycopg2://miyataken999:yz1wPf4KrWTm@ep-odd-mode-93794521.us-east-2.aws.neon.tech:5432/neondb')

# テーブルを再作成
metadata = MetaData()

if inspect(engine).has_table("fasis_chat_history"):
    table = Table('fasis_chat_history', metadata, autoload_with=engine)
    table.drop(engine)

table = Table('fasis_chat_history', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('送信者タイプ', String),
              Column('送信者名', String),
              Column('送信日', String),
              Column('送信時刻', String),
              Column('内容', String),
              Column('AnswerField', String),
              extend_existing=True)

metadata.create_all(engine)

# フォルダー内のすべてのCSVファイルを処理し、PostgreSQLにインポート
process_and_import_csv_folder(folder_path, engine)

print("すべてのCSVファイルのデータインポートが完了しました。")

# データベースに接続してクエリを実行する関数
def execute_query(query, engine):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()

# クエリの例: マスクされたデータを取得
query = "SELECT * FROM fasis_chat_history LIMIT 10;"
results = execute_query(query, engine)

# クエリ結果を表示
for row in results:
    print(row)
