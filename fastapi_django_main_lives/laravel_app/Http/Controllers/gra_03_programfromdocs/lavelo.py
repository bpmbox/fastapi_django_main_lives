import gradio as gr
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append('/workspaces/fastapi_django_main_live')

from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from mysite.interpreter.process import no_process_file,process_file,process_nofile
#from controllers.gra_04_database.rides import test_set_lide
import requests
import sqlite3
import os
from datetime import datetime
from controllers.gra_03_programfromdocs.system_automation import SystemAutomation

# データベース設定
DB_PATH = "/workspaces/fastapi_django_main_live/prompts.db"

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
                ("社員プロフィールシステム", "", "", "web_system", "社員プロフィール管理システム\n- ユーザー登録\n- プロフィール編集\n- 検索機能\n- 管理機能"),
                ("FastAPI + SQLAlchemy", "", "", "api_system", "FastAPIとSQLAlchemyを使用したAPIの作成\n- ユーザー管理\n- 認証機能\n- CRUD操作"),
                ("Gradio Interface", "", "", "interface_system", "Gradioインターフェースの作成\n- ファイルアップロード\n- チャット機能\n- データ表示"),
                ("LINE画像検索システム", "", "", "line_system", "LINEからの画像を検索するシステム\n- doPost受信\n- 画像保存\n- S3アップロード\n- シークレット管理"),
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

def save_prompt(title: str, content: str, github_url: str = "", system_type: str = "general") -> str:
    """プロンプトを保存"""
    try:
        if not title.strip() or not content.strip():
            return "❌ タイトルと内容は必須です"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # GitHubURLからリポジトリ名を抽出
        repo_name = ""
        if github_url:
            repo_name = github_url.split('/')[-1].replace('.git', '') if github_url.endswith('.git') else github_url.split('/')[-1]
        
        cursor.execute(
            'INSERT INTO prompts (title, github_url, repository_name, system_type, content) VALUES (?, ?, ?, ?, ?)',
            (title.strip(), github_url.strip(), repo_name, system_type, content.strip())
        )
        
        conn.commit()
        conn.close()
        print(f"✅ プロンプト保存: {title} (GitHub: {github_url})")
        return f"✅ プロンプト「{title}」を保存しました\n📁 リポジトリ: {repo_name}"
        
    except Exception as e:
        print(f"❌ プロンプト保存エラー: {e}")
        return f"❌ 保存エラー: {e}"

def get_prompts() -> List[Tuple]:
    """全プロンプトを取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, system_type, repository_name, execution_status, created_at 
            FROM prompts 
            ORDER BY created_at DESC
        ''')
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

def get_prompt_details(prompt_id: int) -> Tuple[str, str, str, str]:
    """指定IDのプロンプト詳細を取得"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT content, github_url, system_type, repository_name 
            FROM prompts WHERE id = ?
        ''', (prompt_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result
        else:
            return "", "", "", ""
            
    except Exception as e:
        print(f"❌ プロンプト詳細取得エラー: {e}")
        return "", "", "", ""

def update_execution_status(prompt_id: int, status: str) -> None:
    """実行ステータスを更新"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE prompts SET execution_status = ?, updated_at = ? WHERE id = ?',
            (status, datetime.now().isoformat(), prompt_id)
        )
        
        conn.commit()
        conn.close()
        print(f"✅ ステータス更新: ID {prompt_id} -> {status}")
        
    except Exception as e:
        print(f"❌ ステータス更新エラー: {e}")

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
        for prompt_id, title, system_type, repo_name, status, created_at in prompts:
            # 日時の表示を短くする
            date_str = created_at[:16] if created_at else ""
            # システムタイプのアイコンを追加
            type_icon = {
                'web_system': '🌐',
                'api_system': '🔗',
                'interface_system': '🖥️',
                'line_system': '📱',
                'general': '📄'
            }.get(system_type, '📄')
            
            # ステータスのアイコンを追加
            status_icon = {
                'pending': '⏳',
                'running': '🚀',
                'completed': '✅',
                'failed': '❌'
            }.get(status, '⏳')
            
            table_data.append([
                prompt_id, 
                f"{type_icon} {title}", 
                repo_name or "未設定",
                f"{status_icon} {status}",
                date_str
            ])
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
    # 実行前にステータスを更新
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # プロンプトIDを検索（完全一致で）
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            result = cursor.fetchone()
            if result:
                update_execution_status(result[0], 'running')
            conn.close()
    except Exception as e:
        print(f"実行前ステータス更新エラー: {e}")
    
    # プロンプトを実行
    result = process_nofile(*args, **kwargs)
    
    # Google Chatに通知
    send_to_google_chat(f"🚀 システム生成完了\n```\n{result[:500]}...\n```")
    
    # プロンプト実行後、内容をデータベースに保存・更新
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # 実行されたプロンプトのタイトルを生成（最初の行または最初の50文字）
            title_lines = prompt_content.strip().split('\n')
            title = title_lines[0][:50] if title_lines[0] else "実行されたプロンプト"
            if title.startswith('#'):
                title = title[1:].strip()
            
            # 既存のプロンプトか確認
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            existing = cursor.fetchone()
            
            if existing:
                # 既存プロンプトのステータスを更新
                update_execution_status(existing[0], 'completed')
            else:
                # 新しい実行履歴として保存
                save_prompt(f"実行履歴: {title}", prompt_content, "", "execution_log")
            
            conn.close()
    except Exception as e:
        print(f"実行履歴保存エラー: {e}")
        # エラー時はステータスを失敗に更新
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            result = cursor.fetchone()
            if result:
                update_execution_status(result[0], 'failed')
            conn.close()
        except:
            pass
    
    return result

def process_file_and_notify_enhanced(*args, **kwargs):
    """拡張版: プロンプト実行 + 自動GitHub連携"""
    # 実行前にステータスを更新
    try:
        prompt_content = args[0] if args else ""
        folder_name = args[1] if len(args) > 1 else "generated_systems"
        github_token = args[2] if len(args) > 2 else ""
        
        if prompt_content.strip():
            # プロンプトIDを検索（完全一致で）
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            result = cursor.fetchone()
            if result:
                update_execution_status(result[0], 'running')
            conn.close()
    except Exception as e:
        print(f"実行前ステータス更新エラー: {e}")
    
    # プロンプトを実行
    result = process_nofile(*args, **kwargs)
    
    # 自動化パイプラインを実行
    enhanced_result = result
    if github_token and len(github_token) > 10:  # GitHub tokenが設定されている場合
        try:
            automation = SystemAutomation(github_token)
            
            # リポジトリ名を生成
            title_lines = prompt_content.strip().split('\n')
            repo_name = title_lines[0][:30] if title_lines[0] else "generated-system"
            repo_name = repo_name.replace('#', '').strip().replace(' ', '-').lower()
            
            # 生成されたフォルダのパス
            generated_folder = f"/workspaces/fastapi_django_main_live/{folder_name}"
            
            # 自動化パイプライン実行
            automation_result = automation.full_automation_pipeline(
                generated_folder,
                repo_name,
                f"GPT-ENGINEERで生成されたシステム: {repo_name}"
            )
            
            if automation_result['success']:
                enhanced_result += f"\n\n🚀 自動化完了!\n"
                enhanced_result += f"📁 GitHub: {automation_result['github_repo']['url']}\n"
                enhanced_result += f"🔧 統合されたController: {len(automation_result.get('controllers_found', []))}件"
                
                # Google Chatに詳細通知
                send_to_google_chat(f"""🎉 システム自動生成・統合完了!
                
📊 **生成システム**: {repo_name}
🔗 **GitHub**: {automation_result['github_repo']['url']}
🔧 **Controller統合**: {len(automation_result.get('controllers_found', []))}件
📱 **ステータス**: 運用準備完了
""")
            else:
                enhanced_result += f"\n\n⚠️ 自動化エラー: {automation_result.get('error', '不明')}"
                
        except Exception as e:
            enhanced_result += f"\n\n❌ 自動化エラー: {str(e)}"
    else:
        # 従来の通知
        send_to_google_chat(f"🚀 システム生成完了\n```\n{result[:500]}...\n```")
    
    # プロンプト実行後、内容をデータベースに保存・更新
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # 実行されたプロンプトのタイトルを生成（最初の行または最初の50文字）
            title_lines = prompt_content.strip().split('\n')
            title = title_lines[0][:50] if title_lines[0] else "実行されたプロンプト"
            if title.startswith('#'):
                title = title[1:].strip()
            
            # 既存のプロンプトか確認
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            existing = cursor.fetchone()
            
            if existing:
                # 既存プロンプトのステータスを更新
                update_execution_status(existing[0], 'completed')
            else:
                # 新しい実行履歴として保存
                save_prompt(f"実行履歴: {title}", prompt_content, "", "execution_log")
            
            conn.close()
    except Exception as e:
        print(f"実行履歴保存エラー: {e}")
        # エラー時はステータスを失敗に更新
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM prompts WHERE content = ?', (prompt_content,))
            result = cursor.fetchone()
            if result:
                update_execution_status(result[0], 'failed')
            conn.close()
        except:
            pass
    
    return enhanced_result

# ...existing code...

def load_prompt_to_textbox(evt: gr.SelectData):
    """テーブルクリック時にプロンプト内容をテキストボックスに読み込む"""
    try:
        if evt.index is not None and len(evt.index) >= 2:
            # テーブルの行インデックスから prompt_id を取得
            prompts = get_prompts()
            if evt.index[0] < len(prompts):
                prompt_id = prompts[evt.index[0]][0]  # 最初の列がID
                content, github_url, system_type, repo_name = get_prompt_details(prompt_id)
                return content, github_url, system_type
    except Exception as e:
        print(f"プロンプト読み込みエラー: {e}")
    return "", "", "general"

# 自動検出システム用のメタデータ
interface_title = "💾 プロンプト管理システム"
interface_description = "SQLite3ベースのプロンプト管理とコード生成"

# AI用の高度なプロンプトテンプレート
ai_system_prompts = {
    "microservice_api": """
# 高性能マイクロサービスAPI設計

## 要件
- FastAPI + SQLAlchemy + Alembic
- JWT認証、RBAC権限管理
- OpenAPI仕様書自動生成
- Redis キャッシュ、Celery非同期処理
- Docker コンテナ化
- CI/CD パイプライン（GitHub Actions）
- 監視・ログ・メトリクス（Prometheus + Grafana）

## アーキテクチャ
- Clean Architecture パターン
- Repository パターン
- 依存性注入（DI）
- イベント駆動設計

## セキュリティ
- OWASP準拠
- SQL injection防止
- CORS設定
- Rate limiting

## テスト
- 単体テスト（pytest）
- 統合テスト
- E2Eテスト
- カバレッジ90%以上

作成してください。
""",
    
    "ai_chat_system": """
# AI チャットシステム（RAG対応）

## 機能
- リアルタイムチャット（WebSocket）
- AI応答（OpenAI API, Claude API）
- RAG（Retrieval-Augmented Generation）
- ベクトルデータベース（Chroma, Pinecone）
- ファイルアップロード・解析
- 会話履歴管理
- ユーザー管理・認証

## 技術スタック
- Frontend: React + TypeScript + Tailwind CSS
- Backend: FastAPI + SQLAlchemy
- Vector DB: Chroma
- Cache: Redis
- Queue: Celery

## AI機能
- 文書の埋め込み生成
- セマンティック検索
- コンテキスト理解
- マルチモーダル対応（画像、PDF）

gradio_interface として作成してください。
""",

    "blockchain_dapp": """
# ブロックチェーン DApp開発

## 要件
- Solidity スマートコントラクト
- Web3.js フロントエンド
- MetaMask連携
- IPFS ファイルストレージ
- OpenZeppelin セキュリティ
- Hardhat 開発環境

## 機能
- NFT マーケットプレイス
- DAO ガバナンス
- DeFi プロトコル
- ステーキング機能

## セキュリティ
- リエントランシー攻撃防止
- オーバーフロー対策
- アクセス制御

作成してください。
""",

    "devops_infrastructure": """
# DevOps インフラストラクチャ

## 要件
- Kubernetes クラスター設計
- Terraform インフラコード
- Ansible 設定管理
- CI/CD パイプライン
- 監視・アラート
- ログ集約
- セキュリティ

## 技術
- AWS/GCP/Azure
- Docker/Podman
- GitLab/GitHub Actions
- Prometheus/Grafana
- ELK Stack
- Helm Charts

## セキュリティ
- Secret管理（Vault）
- ネットワークセキュリティ
- コンプライアンス

作成してください。
"""
}

def add_ai_system_prompts():
    """AI用の高度なシステムプロンプトを追加"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for title, content in ai_system_prompts.items():
            # 既存チェック
            cursor.execute('SELECT id FROM prompts WHERE title LIKE ?', (f"%{title}%",))
            if not cursor.fetchone():
                system_type = "ai_generated"
                github_url = f"https://github.com/ai-systems/{title.replace('_', '-')}"
                
                cursor.execute(
                    'INSERT INTO prompts (title, github_url, repository_name, system_type, content) VALUES (?, ?, ?, ?, ?)',
                    (f"🤖 AI: {title}", github_url, title.replace('_', '-'), system_type, content)
                )
                print(f"✅ AI プロンプト追加: {title}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ AI プロンプト追加エラー: {e}")

# データベース初期化
init_db()
# AI用の高度なプロンプトを追加
add_ai_system_prompts()

with gr.Blocks() as gradio_interface:
    gr.Markdown("# 🚀 プロンプト管理＆自動システム生成")
    gr.Markdown("プロンプトでGPT-ENGINEERを使ってシステムを作成し、GitHubにアップして自動化")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📚 プロンプト一覧")
            
            # プロンプト一覧テーブル
            prompt_table = gr.Dataframe(
                headers=["ID", "タイトル", "リポジトリ", "ステータス", "作成日時"],
                datatype=["number", "str", "str", "str", "str"],
                value=update_prompt_display(),
                interactive=False
            )
            
            # 更新ボタン
            refresh_btn = gr.Button("🔄 一覧更新", variant="secondary")
            
            # プロンプト保存エリア
            gr.Markdown("## 💾 プロンプト保存")
            with gr.Row():
                save_title = gr.Textbox(label="タイトル", placeholder="プロンプトのタイトルを入力")
            with gr.Row():
                github_url_input = gr.Textbox(label="GitHub URL", placeholder="https://github.com/username/repository")
                system_type_dropdown = gr.Dropdown(
                    choices=["general", "web_system", "api_system", "interface_system", "line_system"],
                    value="general",
                    label="システムタイプ"
                )
            with gr.Row():
                save_btn = gr.Button("💾 保存", variant="primary")
            save_result = gr.Textbox(label="保存結果", interactive=False)
        
        with gr.Column(scale=2):
            gr.Markdown("## ⚡ プロンプト実行・システム生成")
            
            # メインのプロンプト入力エリア
            prompt_input = gr.Textbox(
                label="プロンプト内容", 
                lines=12,
                value=val,
                placeholder="プロンプトを入力するか、左の一覧からクリックして選択してください"
            )
            
            with gr.Row():
                selected_github_url = gr.Textbox(label="選択中のGitHub URL", interactive=False)
                selected_system_type = gr.Textbox(label="システムタイプ", interactive=False)
            
            with gr.Row():
                folder_name = gr.Textbox(label="フォルダ名", value="generated_systems")
                github_token = gr.Textbox(label="GitHub Token", value="***********************", type="password")
            
            execute_btn = gr.Button("🚀 システム生成実行", variant="primary", size="lg")
            
            with gr.Row():
                auto_github_checkbox = gr.Checkbox(label="🔄 GitHub自動連携", value=True)
                auto_integrate_checkbox = gr.Checkbox(label="🔧 Controller自動統合", value=True)
            
            result_output = gr.Textbox(label="実行結果", lines=8, interactive=False)
            
            gr.Markdown("## 📋 システム生成フロー")
            gr.Markdown("""
            1. **プロンプト入力** → GPT-ENGINEERでシステム生成
            2. **GitHubアップ** → 指定リポジトリに自動プッシュ  
            3. **Controller自動認識** → 新しいRouterが自動で利用可能に
            4. **Google Chat通知** → 生成完了をチームに通知
            """)
    
    # イベントハンドラー
    prompt_table.select(
        fn=load_prompt_to_textbox,
        outputs=[prompt_input, selected_github_url, selected_system_type]
    )
    
    refresh_btn.click(
        fn=update_prompt_display,
        outputs=prompt_table
    )
    
    save_btn.click(
        fn=lambda title, content, github_url, system_type: save_prompt(title, content, github_url, system_type),
        inputs=[save_title, prompt_input, github_url_input, system_type_dropdown],
        outputs=save_result
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    ).then(
        fn=lambda: ("", "", "general"),
        outputs=[save_title, github_url_input, system_type_dropdown]
    )
    
    execute_btn.click(
        fn=process_file_and_notify_enhanced,
        inputs=[prompt_input, folder_name, github_token],
        outputs=result_output
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    )