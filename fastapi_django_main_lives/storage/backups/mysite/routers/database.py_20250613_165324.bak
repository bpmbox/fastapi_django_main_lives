import duckdb
import pandas as pd
from fastapi import FastAPI
import gradio as gr
import os

# データベースディレクトリを作成
os.makedirs("./workspace", exist_ok=True)

# DuckDB接続をtry-catch文で囲む
try:
    con = duckdb.connect(database="./workspace/mydatabase.duckdb")
    con.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, name VARCHAR);")
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    # フォールバック：メモリ内データベースを使用
    con = duckdb.connect(database=":memory:")
    con.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, name VARCHAR);")
    print("✓ Using in-memory database as fallback")

# Extract the 'content' field from all elements in the result
def insert(full_response,message):
    age = 28
    # データベースファイルのパス
    db_path = "./workspace/sample.duckdb"

    try:
        # DuckDBに接続（データベースファイルが存在しない場合は新規作成）
        con = duckdb.connect(database=db_path)
        con.execute(
            """
        CREATE SEQUENCE IF NOT EXISTS sample_id_seq START 1;
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER DEFAULT nextval('sample_id_seq'),
            name VARCHAR,
            age INTEGER,
            PRIMARY KEY(id)
        );
        """
        )
        cur = con.cursor()
        con.execute("INSERT INTO samples (name, age) VALUES (?, ?)", (full_response, age))
        con.execute("INSERT INTO samples (name, age) VALUES (?, ?)", (message, age))
        # データをCSVファイルにエクスポート
        con.execute("COPY samples TO 'sample.csv' (FORMAT CSV, HEADER)")
        # データをコミット
        con.commit()
        # データを選択
        cur = con.execute("SELECT * FROM samples")
        # 結果をフェッチ
        res = cur.fetchall()
        rows = ""
        # 結果を表示
        # 結果を文字列に整形
        rows = "\n".join([f"name: {row[0]}, age: {row[1]}" for row in res])
        # コネクションを閉じる
        con.close()
        print(f"Database insert successful: {rows}")
        return rows
    except Exception as e:
        print(f"Database insert failed: {e}")
        return f"Error: {e}"

def setup_database_routes(app: FastAPI):
    def create_item(name):
        con.execute("INSERT INTO items (name) VALUES (?);", (name,))
        con.commit()
        return "Item created successfully!"

    def read_items():
        cursor = con.cursor()
        cursor.execute("SELECT * FROM items;")
        items = cursor.fetchall()
        df = pd.DataFrame(items, columns=["ID", "Name"])
        return df

    def update_item(id, name):
        con.execute("UPDATE items SET name = ? WHERE id = ?;", (name, id))
        con.commit()
        return "Item updated successfully!"

    def delete_item(id):
        con.execute("DELETE FROM items WHERE id = ?;", (id,))
        con.commit()
        return "Item deleted successfully!"

    with gr.Blocks() as appdb:
        gr.Markdown("CRUD Application")
        with gr.Row():
            with gr.Column():
                create_name = gr.Textbox(label="Create Item")
                create_btn = gr.Button("Create")
            with gr.Column():
                read_btn = gr.Button("Read Items")
        with gr.Row():
            with gr.Column():
                update_id = gr.Textbox(label="Update Item ID")
                update_name = gr.Textbox(label="Update Item Name")
                update_btn = gr.Button("Update")
            with gr.Column():
                delete_id = gr.Textbox(label="Delete Item ID")
                delete_btn = gr.Button("Delete")
        output_text = gr.Textbox(label="Output")
        output_table = gr.DataFrame(label="Items")

        create_btn.click(fn=create_item, inputs=create_name, outputs=output_text)
        read_btn.click(fn=read_items, outputs=output_table)
        update_btn.click(fn=update_item, inputs=[update_id, update_name], outputs=output_text)
        delete_btn.click(fn=delete_item, inputs=delete_id, outputs=output_text)

    app.mount("/db", appdb, name="database_app")
