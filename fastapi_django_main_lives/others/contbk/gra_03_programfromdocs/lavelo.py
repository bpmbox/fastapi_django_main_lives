import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import gradio as gr
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from mysite.interpreter.process import no_process_file,process_file,process_nofile
#from controllers.gra_04_database.rides import test_set_lide
import requests
import sqlite3
import os
from datetime import datetime

# データベース設定
DB_PATH = "prompts.db"

def init_db():
    """プロンプトデータベースの初期化"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                github_url TEXT,
                repository_name TEXT,
                system_type TEXT DEFAULT 'general',
                content TEXT NOT NULL,
                execution_status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # デフォルトプロンプトの追加（初回のみ）
        cursor.execute('SELECT COUNT(*) FROM prompts')
        if cursor.fetchone()[0] == 0:
            default_prompts = [
                ("社員プロフィールシステム", "", "", "web_system", val),
                ("FastAPI + SQLAlchemy", "", "", "api_system", "FastAPIとSQLAlchemyを使用したAPIの作成\n- ユーザー管理\n- 認証機能\n- CRUD操作"),
                ("Gradio Interface", "", "", "interface_system", "Gradioインターフェースの作成\n- ファイルアップロード\n- チャット機能\n- データ表示"),
            ]
            
            for title, github_url, repo_name, system_type, content in default_prompts:
                cursor.execute(
                    'INSERT INTO prompts (title, github_url, repository_name, system_type, content) VALUES (?, ?, ?, ?, ?)',
                    (title, github_url, repo_name, system_type, content)
                )
        
        conn.commit()
        conn.close()
        print("✅ プロンプトデータベース初期化完了")
        
    except Exception as e:
        print(f"❌ データベース初期化エラー: {e}")

def save_prompt(title: str, content: str) -> str:
    """プロンプトを保存"""
    try:
        if not title.strip() or not content.strip():
            return "❌ タイトルと内容は必須です"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO prompts (title, github_url, repository_name, system_type, content) VALUES (?, ?, ?, ?, ?)',
            (title.strip(), "", "", "general", content.strip())
        )
        
        conn.commit()
        conn.close()
        print(f"✅ プロンプト保存: {title}")
        return f"✅ プロンプト「{title}」を保存しました"
        
    except Exception as e:
        print(f"❌ プロンプト保存エラー: {e}")
        return f"❌ 保存エラー: {e}"

def get_prompts() -> List[Tuple]:
    """全プロンプトを取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title, created_at FROM prompts ORDER BY created_at DESC')
        prompts = cursor.fetchall()
        
        conn.close()
        print(f"✅ プロンプト取得: {len(prompts)}件")
        return prompts
    except Exception as e:
        print(f"❌ プロンプト取得エラー: {e}")
        return []

def get_prompt_content(prompt_id: int) -> str:
    """指定IDのプロンプト内容を取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT content FROM prompts WHERE id = ?', (prompt_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            print(f"✅ プロンプト内容取得: ID {prompt_id}")
            return result[0]
        else:
            print(f"❌ プロンプトが見つかりません: ID {prompt_id}")
            return ""
            
    except Exception as e:
        print(f"❌ プロンプト内容取得エラー: {e}")
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
            print(f"✅ プロンプト削除: ID {prompt_id}")
            return f"✅ プロンプト ID {prompt_id} を削除しました"
        else:
            conn.close()
            return f"❌ プロンプト ID {prompt_id} が見つかりません"
            
    except Exception as e:
        print(f"❌ プロンプト削除エラー: {e}")
        return f"❌ 削除エラー: {e}"

def update_prompt_display():
    """プロンプト一覧の表示を更新"""
    prompts = get_prompts()
    if prompts:
        # テーブル形式でデータを準備
        table_data = []
        for prompt_id, title, created_at in prompts:
            # 日時の表示を短くする
            date_str = created_at[:16] if created_at else ""
            table_data.append([prompt_id, title, date_str])
        return table_data
    return []

val = """
# 社員がプロフィールを登録・公開し、お互いに参照できるシステム

## 機能

## LINEのクレーム対応システムの作成
- クレームがあった用語をAPIでナレッジに登録するシステム
- APIキー agentキーをいれ
- 否定語に対する　文言に隊しての設定をする

### ユーザー登録

- ユーザー登録画面で、ユーザー名とパスワードを入力して登録ボタンを押すことにより、新規ユーザーを登録することができる。
- ユーザー名は、既存のユーザーと重複してはいけない。
- ユーザー登録に成功したら、ログイン済み状態として、ユーザー一覧画面へ遷移する。

### ログイン

- ログイン画面で、ユーザー名とパスワードを入力してログインボタンを押すことにより、ログインすることができる。
- ログインに成功したら、ユーザー一覧画面へ遷移する。

### チーム一覧・作成

- チームの一覧が、チームの作成日時降順で表示される。
- チーム名を入力して作成ボタンを押すと、チームが作成される。
- チームの作成後、本画面が再表示される。

### プロフィール編集

- 自身の`所属チーム`・`プロフィール`・`タグ`を編集できる。
- 所属チームは、既存チームからの選択式とする。
- プロフィールは自由入力とする。
- タグは自由入力で、複数入力できるようにする。

### ユーザー一覧・検索

- デフォルトでは全てのユーザーが一覧表示される。
- 検索条件を入力して検索ボタンを押すと、検索条件がプロフィールに部分一致するユーザーのみにフィルタリングできる。
- 一覧は、ユーザー登録日時の降順で表示される。
- 表示内容は、`ユーザー名`・`プロフィール`で、`プロフィール`は先頭10文字と三点リーダーを表示する。
- ユーザー名をクリックすると、そのユーザーのユーザー詳細画面へ遷移する。
- `チーム一覧へ`をクリックすると、チーム一覧画面へ遷移する。

### ユーザー詳細画面

- 特定のユーザーの、`ユーザー名`・`所属チーム`・`プロフィール`・`タグ`が表示される。
- プロフィールの表示はマークダウンに対応させる。
- `一覧へ`リンクをクリックすると、ユーザー一覧画面へ遷移する。

## あなたが作成するもの

バックエンドのプログラム一式を作成してください。
フロントエンドのプログラムは不要です。

- `/api`ディレクトリ以下に作成。
- Python/FastAPI/SQLAlchemyを使う。
- DBはSQLiteを使う。
- 必要に応じて外部ライブラリを使う。
- クラウドや外部サービス(外部API)は使わない。
- .gitignoreを含めること。
- バックエンド
@app.post("
def lumbda_function():

gradio_interface でメイン関数から読み込めるようにして

googleappsscript
ラインの画像検索システム

ファイルは１ファイルで作成して。
１ファイル１機能で難しくしたくない

1,lineからデータがくる
2,doPostで取得
3.typeがイメージの場合はドライブに保存
4,保存したデータをS3にアップロード
5.データはシークレットから取得
6,plantumlでフローの作成
7,システムドキュメントの作成

gradio は gradio_interface というBlock名で作成
fastapiはrouter の作成

"""

def send_to_google_chat(message: str):
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAANwDF_KE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=qSigSPSbTINJITgO30iGKnyeY48emcUJd9LST7FBLLY'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, json=data)
    response.raise_for_status()

def process_file_and_notify(*args, **kwargs):
    result = process_nofile(*args, **kwargs)
    send_to_google_chat(result)
    
    # プロンプト実行後、内容をデータベースに保存
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # 実行されたプロンプトのタイトルを生成（最初の行または最初の50文字）
            title_lines = prompt_content.strip().split('\n')
            title = title_lines[0][:50] if title_lines[0] else "実行されたプロンプト"
            if title.startswith('#'):
                title = title[1:].strip()
            
            save_prompt(f"実行履歴: {title}", prompt_content)
    except Exception as e:
        print(f"実行履歴保存エラー: {e}")
    
    return result

def load_prompt_to_textbox(evt: gr.SelectData):
    """テーブルクリック時にプロンプト内容をテキストボックスに読み込む"""
    try:
        if evt.index is not None and len(evt.index) >= 2:
            # テーブルの行インデックスから prompt_id を取得
            prompts = get_prompts()
            if evt.index[0] < len(prompts):
                prompt_id = prompts[evt.index[0]][0]  # 最初の列がID
                content = get_prompt_content(prompt_id)
                return content
    except Exception as e:
        print(f"プロンプト読み込みエラー: {e}")
    return ""

# データベース初期化
init_db()

with gr.Blocks() as gradio_interface:
    gr.Markdown("# プロンプト管理システム")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📚 プロンプト一覧")
            
            # プロンプト一覧テーブル
            prompt_table = gr.Dataframe(
                headers=["ID", "タイトル", "作成日時"],
                datatype=["number", "str", "str"],
                value=update_prompt_display(),
                interactive=False
            )
            
            # 更新ボタン
            refresh_btn = gr.Button("🔄 一覧更新", variant="secondary")
            
            # プロンプト保存エリア
            gr.Markdown("## 💾 プロンプト保存")
            with gr.Row():
                save_title = gr.Textbox(label="タイトル", placeholder="プロンプトのタイトルを入力")
                save_btn = gr.Button("💾 保存", variant="primary")
            save_result = gr.Textbox(label="保存結果", interactive=False)
        
        with gr.Column(scale=2):
            gr.Markdown("## ⚡ プロンプト実行")
            
            # メインのプロンプト入力エリア
            prompt_input = gr.Textbox(
                label="プロンプト内容", 
                lines=15,
                value=val,
                placeholder="プロンプトを入力するか、左の一覧からクリックして選択してください"
            )
            
            with gr.Row():
                folder_name = gr.Textbox(label="フォルダ名", value="test_folders")
                github_token = gr.Textbox(label="GitHub Token", value="***********************", type="password")
            
            execute_btn = gr.Button("🚀 実行", variant="primary", size="lg")
            result_output = gr.Textbox(label="実行結果", lines=10, interactive=False)
    
    # イベントハンドラー
    prompt_table.select(
        fn=load_prompt_to_textbox,
        outputs=prompt_input
    )
    
    refresh_btn.click(
        fn=update_prompt_display,
        outputs=prompt_table
    )
    
    save_btn.click(
        fn=lambda title, content: save_prompt(title, content),
        inputs=[save_title, prompt_input],
        outputs=save_result
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    ).then(
        fn=lambda: "",
        outputs=save_title
    )
    
    execute_btn.click(
        fn=process_file_and_notify,
        inputs=[prompt_input, folder_name, github_token],
        outputs=result_output
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    )