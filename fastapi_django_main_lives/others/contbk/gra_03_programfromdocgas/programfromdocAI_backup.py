import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file, no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

# データベース設定
DB_PATH = "prompts.db"

def init_db():
    """プロンプトデータベースの初期化"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            github_url TEXT,
            repository_name TEXT,
            system_type TEXT,
            execution_status TEXT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # デフォルトプロンプトの追加（初回のみ）
    cursor.execute('SELECT COUNT(*) FROM prompts')
    if cursor.fetchone()[0] == 0:
        default_prompt = """# gradio で miiboのナレッジに登録する画面の作成
  gradio_interface interfacec name

# fastapi
  gradio apiに接続するAPI
  router で作成

1ファイルで作成
仕様書の作成
plantumlで図にする

#sample fastapi
import requests
import json
import os

from fastapi import APIRouter, HTTPException
from gradio_client import Client

router = APIRouter(prefix="/gradio", tags=["gradio"])
@router.get("/route/gradio")

def get_senario(id,res):
    table = "LOG"
    client = Client("kenken999/fastapi_django_main_live")
    result = client.predict(
            message="Hello!!",
            request=0.95,
            param_3=512,
            api_name="/chat"
    )
    return result
"""
        cursor.execute(
            'INSERT INTO prompts (title, url, content) VALUES (?, ?, ?)',
            ('デフォルト：Gradio + FastAPI作成', 'https://example.com', default_prompt)
        )
    
    conn.commit()
    conn.close()

def save_prompt(title: str, url: str, content: str) -> str:
    """プロンプトを保存"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO prompts (title, url, content) VALUES (?, ?, ?)',
            (title, url, content)
        )
        
        conn.commit()
        conn.close()
        return f"✅ プロンプト '{title}' を保存しました！"
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def get_prompts() -> List[Tuple]:
    """全プロンプトを取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title, url, created_at FROM prompts ORDER BY created_at DESC')
        prompts = cursor.fetchall()
        
        conn.close()
        return prompts
    except Exception as e:
        print(f"プロンプト取得エラー: {e}")
        return []

def get_prompt_content(prompt_id: int) -> str:
    """指定IDのプロンプト内容を取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT content FROM prompts WHERE id = ?', (prompt_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else ""
    except Exception as e:
        print(f"プロンプト内容取得エラー: {e}")
        return ""

def delete_prompt(prompt_id: int) -> str:
    """プロンプトを削除"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM prompts WHERE id = ?', (prompt_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return "✅ プロンプトを削除しました"
        else:
            conn.close()
            return "❌ プロンプトが見つかりません"
    except Exception as e:
        return f"❌ 削除エラー: {str(e)}"

# データベース初期化
init_db()

def load_prompt_from_db(prompt_id):
    """選択されたプロンプトを読み込み"""
    if prompt_id:
        content = get_prompt_content(int(prompt_id))
        return content
    return ""

def refresh_prompt_list():
    """プロンプト一覧を更新"""
    prompts = get_prompts()
    choices = []
    for prompt in prompts:
        id_, title, url, created_at = prompt
        display_text = f"[{id_}] {title} ({created_at[:10]})"
        choices.append((display_text, str(id_)))
    return gr.Dropdown(choices=choices, label="📋 保存済みプロンプト一覧", value=None)

# Gradioインターフェース作成
with gr.Blocks(title="🚀 プロンプト管理 & コード生成") as gradio_interface:
    gr.Markdown("# 🚀 プロンプト管理 & ドキュメントからコード生成")
    
    with gr.Tabs():
        # タブ1: プロンプト管理
        with gr.TabItem("📝 プロンプト管理"):
            gr.Markdown("## プロンプトの保存・管理")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # プロンプト保存フォーム
                    save_title = gr.Textbox(label="📋 タイトル", placeholder="例: FastAPI + Gradio作成プロンプト")
                    save_url = gr.Textbox(label="🔗 参考URL (任意)", placeholder="https://example.com")
                    save_content = gr.Textbox(
                        label="📝 プロンプト内容", 
                        lines=10,
                        placeholder="プロンプトの内容を入力してください..."
                    )
                    save_btn = gr.Button("💾 プロンプトを保存", variant="primary")
                    save_status = gr.Textbox(label="保存結果", interactive=False)
                
                with gr.Column(scale=1):
                    # プロンプト一覧
                    prompt_dropdown = gr.Dropdown(
                        choices=[], 
                        label="📋 保存済みプロンプト一覧",
                        interactive=True
                    )
                    refresh_btn = gr.Button("🔄 一覧を更新")
                    load_btn = gr.Button("📥 選択したプロンプトを読み込み", variant="secondary")
                    delete_btn = gr.Button("🗑️ 選択したプロンプトを削除", variant="stop")
                    delete_status = gr.Textbox(label="削除結果", interactive=False)
        
        # タブ2: コード生成
        with gr.TabItem("⚡ コード生成"):
            gr.Markdown("## ドキュメントからコード生成")
            
            with gr.Row():
                with gr.Column():
                    # ファイルアップロード
                    input_file = gr.File(label="📄 ドキュメントファイル")
                    
                    # プロンプト表示・編集エリア
                    current_prompt = gr.Textbox(
                        label="📝 現在のプロンプト", 
                        lines=15,
                        value="",
                        placeholder="上のタブでプロンプトを選択するか、直接入力してください..."
                    )
                    
                with gr.Column():
                    # 生成設定
                    folder_name = gr.Textbox(label="📁 出力フォルダ名", value="generated_code")
                    github_token = gr.Textbox(label="🔑 GitHub Token (任意)", type="password", value="")
                    
                    # 生成ボタン
                    generate_btn = gr.Button("🚀 コード生成実行", variant="primary", size="lg")
                    
                    # 結果表示
                    result_output = gr.Textbox(label="📤 生成結果", lines=10, interactive=False)
    
    # イベントハンドラー
    def handle_save_prompt(title, url, content):
        if not title.strip() or not content.strip():
            return "❌ タイトルとプロンプト内容は必須です"
        return save_prompt(title, url, content)
    
    def handle_refresh_list():
        prompts = get_prompts()
        choices = []
        for prompt in prompts:
            id_, title, url, created_at = prompt
            display_text = f"[{id_}] {title} ({created_at[:10]})"
            choices.append((display_text, str(id_)))
        return gr.Dropdown(choices=choices, value=None)
    
    def handle_load_prompt(selected_prompt):
        if selected_prompt:
            prompt_id = selected_prompt.split(']')[0][1:]  # [1] から ] までを取得してIDを抽出
            content = get_prompt_content(int(prompt_id))
            return content
        return ""
    
    def handle_delete_prompt(selected_prompt):
        if selected_prompt:
            prompt_id = selected_prompt.split(']')[0][1:]  # IDを抽出
            return delete_prompt(int(prompt_id))
        return "❌ プロンプトが選択されていません"
    
    def handle_generate_code(file, prompt, folder, token):
        if not prompt.strip():
            return "❌ プロンプトが入力されていません"
        return process_file(file, prompt, folder, token)
    
    # イベント接続
    save_btn.click(
        handle_save_prompt,
        inputs=[save_title, save_url, save_content],
        outputs=[save_status]
    )
    
    refresh_btn.click(
        handle_refresh_list,
        outputs=[prompt_dropdown]
    )
    
    load_btn.click(
        handle_load_prompt,
        inputs=[prompt_dropdown],
        outputs=[current_prompt]
    )
    
    delete_btn.click(
        handle_delete_prompt,
        inputs=[prompt_dropdown],
        outputs=[delete_status]
    )
    
    generate_btn.click(
        handle_generate_code,
        inputs=[input_file, current_prompt, folder_name, github_token],
        outputs=[result_output]
    )
    
    # ページ読み込み時にプロンプト一覧を初期化
    gradio_interface.load(
        handle_refresh_list,
        outputs=[prompt_dropdown]
    )