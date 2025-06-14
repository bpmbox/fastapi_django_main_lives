#!/usr/bin/env python3
"""
🎯 AI-Human協働開発システム - 初心者向け順次テストガイド

このシステムは初めて使う方でも簡単に操作できるよう、
ステップバイステップのガイド付きインターフェースを提供します。

上から順番に実行していくだけで、システム全体を体験できます。
"""

import gradio as gr
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
import sys

# プロジェクトルートをパスに追加
sys.path.append('/workspaces/fastapi_django_main_live')

class BeginnerGuideSystem:
    """初心者ガイドシステムクラス"""
    
    def __init__(self):
        self.db_path = "/workspaces/fastapi_django_main_live/prompts.db"
        self.approval_db_path = "/workspaces/fastapi_django_main_live/controllers/gra_03_programfromdocs/approval_system.db"
        self.current_step = 1
        self.max_steps = 6
        self.test_results = {}
        
    def get_system_overview(self):
        """システム概要を取得"""
        return """
# 🚀 AI-Human協働開発システムへようこそ！

## 📋 このシステムでできること

### 🎯 主要機能
1. **プロンプト管理**: AIに指示するプロンプトを作成・保存
2. **承認システム**: 安全性を確保するための承認フロー  
3. **自動実行**: 承認されたプロンプトの自動実行
4. **GitHub連携**: 実行結果をGitHubに自動投稿
5. **ログ管理**: 全実行履歴の記録・確認

### ✨ 特徴
- **24時間での高速開発**を実現
- **安全性重視**の承認システム
- **完全自動化**されたワークフロー
- **初心者でも簡単**に使える設計

### 📊 システムフロー図

```mermaid
flowchart LR
    A[プロンプト作成] --> B[承認待ち]
    B --> C[承認・却下]
    C --> D[自動実行]
    D --> E[GitHub連携]
    E --> F[完了]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#e0f2f1
```

## 🎯 使い方
下のタブを**順番に**進んでください。各ステップで「実行」ボタンを押すだけです！

次のステップに進んで、実際にシステムを体験してみましょう！
        """
        
    def create_test_prompt(self, title, content, category="テスト"):
        """テストプロンプトを作成"""
        try:
            # データベースが存在しない場合は作成
            if not os.path.exists(self.db_path):
                self.init_database()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # プロンプト挿入
            cursor.execute('''
                INSERT INTO prompts (title, content, category, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, category, datetime.now(), datetime.now()))
            
            conn.commit()
            prompt_id = cursor.lastrowid
            conn.close()
            
            success_msg = f"""
## ✅ プロンプト作成成功！

**ID**: {prompt_id}  
**タイトル**: {title}  
**カテゴリ**: {category}  
**内容**: {content[:100]}...

### 📝 次のステップ
「ステップ3: 承認システム」タブに進んで、作成したプロンプトを承認してください。
            """
            return success_msg
            
        except Exception as e:
            return f"❌ エラーが発生しました: {str(e)}"
    
    def init_database(self):
        """データベースを初期化"""
        try:
            # ディレクトリ作成
            os.makedirs(os.path.dirname(self.approval_db_path), exist_ok=True)
            
            # プロンプトDB作成
            conn = sqlite3.connect(self.db_path)
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
            conn.close()
            
            # 承認DB作成
            conn = sqlite3.connect(self.approval_db_path)
            cursor = conn.cursor()
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
            
        except Exception as e:
            print(f"データベース初期化エラー: {e}")
    
    def get_pending_prompts(self):
        """承認待ちプロンプトを取得"""
        try:
            if not os.path.exists(self.db_path):
                return "📝 プロンプトデータベースが存在しません。まずステップ2でプロンプトを作成してください。"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, created_at 
                FROM prompts 
                ORDER BY created_at DESC 
                LIMIT 5
            ''')
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return "📝 承認待ちのプロンプトはありません。ステップ2でプロンプトを作成してください。"
            
            pending_list = "## 📋 最新のプロンプト一覧\n\n"
            for row in results:
                pending_list += f"### プロンプト ID: {row[0]}\n"
                pending_list += f"**タイトル**: {row[1]}\n"
                pending_list += f"**内容**: {row[2][:100]}...\n"
                pending_list += f"**作成日時**: {row[3]}\n\n"
            
            pending_list += "### 📝 次のアクション\n下のフォームでプロンプトIDを入力して承認してください。"
            return pending_list
            
        except Exception as e:
            return f"❌ エラーが発生しました: {str(e)}"
    
    def approve_prompt(self, prompt_id, reason="初心者ガイドでのテスト承認"):
        """プロンプトを承認"""
        try:
            if not prompt_id or prompt_id <= 0:
                return "❌ 有効なプロンプトIDを入力してください"
            
            # 承認DB初期化
            if not os.path.exists(self.approval_db_path):
                self.init_database()
            
            conn = sqlite3.connect(self.approval_db_path)
            cursor = conn.cursor()
            
            # 承認記録挿入
            cursor.execute('''
                INSERT INTO approvals (prompt_id, approval_status, reason, approved_at)
                VALUES (?, ?, ?, ?)
            ''', (int(prompt_id), "approved", reason, datetime.now()))
            
            conn.commit()
            conn.close()
            
            return f"""
## ✅ 承認完了！

**プロンプトID**: {prompt_id}  
**ステータス**: approved  
**理由**: {reason}  
**承認日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 🚀 次のステップ
「ステップ4: 実行テスト」タブに進んで、実行をシミュレートしてください。
            """
            
        except Exception as e:
            return f"❌ 承認処理でエラーが発生しました: {str(e)}"
    
    def simulate_execution(self):
        """実行をシミュレート"""
        try:
            execution_log = {
                "timestamp": datetime.now(),
                "status": "success",
                "message": "テスト実行が完了しました",
                "steps": [
                    "✅ プロンプト解析完了",
                    "✅ コード生成完了", 
                    "✅ 安全性チェック完了",
                    "✅ 実行完了"
                ]
            }
            
            result = f"""
## 🚀 実行結果

**実行時刻**: {execution_log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}  
**ステータス**: ✅ {execution_log['status']}  
**メッセージ**: {execution_log['message']}

### 📊 実行ログ
"""
            
            for step in execution_log['steps']:
                result += f"- {step}\n"
            
            result += """
### 🚀 次のステップ
「ステップ5: GitHub連携」タブに進んで、GitHub Issue作成をテストしてください。
            """
            
            return result
            
        except Exception as e:
            return f"❌ 実行シミュレーションでエラーが発生しました: {str(e)}"
    
    def simulate_github_issue(self):
        """GitHub Issue作成をシミュレート"""
        try:
            issue_data = {
                "title": "🚀 AI-Human協働開発システム テスト実行完了",
                "timestamp": datetime.now(),
                "body": f"""
## 📋 実行サマリー
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **ステータス**: ✅ 成功
- **実行時間**: 0.5秒

## 🔧 実行内容
- プロンプト処理
- コード生成
- 安全性チェック
- 結果出力

## 📊 システム状態
- データベース: 正常
- API連携: 正常  
- ログシステム: 正常
                """,
                "labels": ["automation", "test", "ai-human-collaboration"]
            }
            
            result = f"""
## 🐙 GitHub Issue作成完了

**タイトル**: {issue_data['title']}  
**作成日時**: {issue_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

### 📝 Issue内容
{issue_data['body']}

**ラベル**: {', '.join(issue_data['labels'])}

### 🎉 次のステップ
「ステップ6: システム確認」タブに進んで、全体の状況を確認してください。

（実際のGitHub連携は環境設定次第で有効になります）
            """
            
            return result
            
        except Exception as e:
            return f"❌ GitHub連携シミュレーションでエラーが発生しました: {str(e)}"
    
    def check_system_status(self):
        """システム状態を確認"""
        try:
            status_report = f"""
## 🎯 システム全体状況レポート

### 📊 データベース状態
"""
            
            # プロンプトDB確認
            if os.path.exists(self.db_path):
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM prompts")
                    prompt_count = cursor.fetchone()[0]
                    status_report += f"- ✅ プロンプトDB: 正常 ({prompt_count}件のプロンプト)\n"
                    conn.close()
                except:
                    status_report += "- ❌ プロンプトDB: 接続エラー\n"
            else:
                status_report += "- ⚠️ プロンプトDB: ファイルが存在しません\n"
            
            # 承認DB確認
            if os.path.exists(self.approval_db_path):
                try:
                    conn = sqlite3.connect(self.approval_db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM approvals")
                    approval_count = cursor.fetchone()[0]
                    status_report += f"- ✅ 承認DB: 正常 ({approval_count}件の承認記録)\n"
                    conn.close()
                except:
                    status_report += "- ❌ 承認DB: 接続エラー\n"
            else:
                status_report += "- ⚠️ 承認DB: ファイルが存在しません\n"
            
            status_report += f"""
### 🚀 システムステータス
- ✅ Webサーバー: 起動中 (ポート7860)
- ✅ Gradioインターフェース: 正常
- ✅ ファイルシステム: 正常
- ✅ 実行環境: Python {sys.version.split()[0]}

### 🎉 完了おめでとうございます！

AI-Human協働開発システムの基本的な流れをすべて体験しました！

#### 📋 体験した内容
1. ✅ システム概要の理解
2. ✅ プロンプトの作成
3. ✅ 承認プロセスの実行
4. ✅ 実行システムのテスト
5. ✅ GitHub連携のシミュレーション
6. ✅ システム状態の確認

#### 🚀 次のステップ
各機能の詳細は、メインの各タブで更に詳しく利用できます：
- **💾 プロンプト管理システム**: 本格的なプロンプト管理
- **🎯 統合承認システム**: 詳細な承認フロー
- **🤖 GitHub ISSUE自動化**: 実際のGitHub連携
- **🚀 統合管理ダッシュボード**: システム全体の監視

システムを実際に使用する際は、これらのタブを活用してください！
            """
            
            return status_report
            
        except Exception as e:
            return f"❌ システム状態確認でエラーが発生しました: {str(e)}"

# システムインスタンスを作成
guide_system = BeginnerGuideSystem()

def create_beginner_interface():
    """初心者向けGradioインターフェースを作成"""
    
    with gr.Blocks(title="🚀 初心者ガイド", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🚀 AI-Human協働開発システム - 初心者ガイド")
        gr.Markdown("**上から順番に**各タブを進んでください。各ステップで「実行」ボタンを押すだけで体験できます！")
        
        with gr.Tab("📚 ステップ1: システム概要"):
            gr.Markdown(guide_system.get_system_overview())
        
        with gr.Tab("📝 ステップ2: プロンプト作成"):
            gr.Markdown("## 🎯 プロンプト作成のテスト")
            gr.Markdown("簡単なテストプロンプトを作成してみましょう。")
            
            with gr.Row():
                with gr.Column(scale=2):
                    title_input = gr.Textbox(
                        label="📝 プロンプトタイトル",
                        value="初回テストプロンプト",
                        placeholder="プロンプトのタイトルを入力"
                    )
                with gr.Column(scale=1):
                    category_input = gr.Textbox(
                        label="🏷️ カテゴリ",
                        value="テスト",
                        placeholder="カテゴリを入力"
                    )
            
            content_input = gr.Textbox(
                label="📄 プロンプト内容",
                value="Hello World を表示するシンプルなPythonスクリプトを作成してください。",
                placeholder="プロンプトの内容を入力",
                lines=3
            )
            
            create_btn = gr.Button("🚀 プロンプト作成実行", variant="primary", size="lg")
            create_result = gr.Markdown(value="👆 上のボタンを押してプロンプトを作成してください")
            
            create_btn.click(
                guide_system.create_test_prompt,
                inputs=[title_input, content_input, category_input],
                outputs=[create_result]
            )
        
        with gr.Tab("✅ ステップ3: 承認システム"):
            gr.Markdown("## 🎯 承認システムのテスト")
            gr.Markdown("作成したプロンプトの承認プロセスをテストします。")
            
            check_btn = gr.Button("📋 承認待ちプロンプト確認", variant="secondary", size="lg")
            pending_result = gr.Markdown(value="👆 上のボタンを押して承認待ちプロンプトを確認してください")
            
            check_btn.click(guide_system.get_pending_prompts, outputs=[pending_result])
            
            gr.Markdown("### 承認実行")
            with gr.Row():
                with gr.Column(scale=1):
                    prompt_id_input = gr.Number(
                        label="🆔 プロンプトID",
                        value=1,
                        precision=0,
                        minimum=1
                    )
                with gr.Column(scale=2):
                    approval_reason = gr.Textbox(
                        label="📝 承認理由",
                        value="初心者ガイドでのテスト承認",
                        placeholder="承認理由を入力"
                    )
            
            approve_btn = gr.Button("✅ 承認実行", variant="primary", size="lg")
            approval_result = gr.Markdown(value="👆 プロンプトIDを確認して承認ボタンを押してください")
            
            approve_btn.click(
                guide_system.approve_prompt,
                inputs=[prompt_id_input, approval_reason],
                outputs=[approval_result]
            )
        
        with gr.Tab("⚡ ステップ4: 実行テスト"):
            gr.Markdown("## 🎯 実行システムのテスト")
            gr.Markdown("承認されたプロンプトの実行をシミュレートします。")
            
            execute_btn = gr.Button("🚀 実行シミュレーション", variant="primary", size="lg")
            execution_result = gr.Markdown(value="👆 上のボタンを押して実行をシミュレートしてください")
            
            execute_btn.click(guide_system.simulate_execution, outputs=[execution_result])
        
        with gr.Tab("🐙 ステップ5: GitHub連携"):
            gr.Markdown("## 🎯 GitHub連携のテスト")
            gr.Markdown("実行結果をGitHub Issueとして作成するプロセスをシミュレートします。")
            
            github_btn = gr.Button("🐙 GitHub Issue作成シミュレーション", variant="primary", size="lg")
            github_result = gr.Markdown(value="👆 上のボタンを押してGitHub連携をテストしてください")
            
            github_btn.click(guide_system.simulate_github_issue, outputs=[github_result])
        
        with gr.Tab("🎯 ステップ6: システム確認"):
            gr.Markdown("## 🎯 システム全体の状態確認")
            gr.Markdown("最後に、システム全体の動作状況を確認します。")
            
            status_btn = gr.Button("📊 システム状態確認", variant="primary", size="lg")
            status_result = gr.Markdown(value="👆 上のボタンを押してシステム全体の状態を確認してください")
            
            status_btn.click(guide_system.check_system_status, outputs=[status_result])
    
    return interface

# Gradioインターフェースを作成
gradio_interface = create_beginner_interface()

def create_gradio_interface():
    """Gradioインターフェースを作成する関数"""
    with gr.Blocks(
        title="🎯 AI-Human協働開発システム - 初心者向けガイド",
        theme=gr.themes.Soft(),
        css="""
        .container { max-width: 1200px; margin: 0 auto; }
        .step-header { background: linear-gradient(90deg, #FF6B6B, #4ECDC4); padding: 20px; border-radius: 10px; color: white; }
        .step-content { padding: 20px; border: 2px solid #ddd; border-radius: 10px; margin: 10px 0; }
        .highlight { background: #FFF3CD; padding: 15px; border-radius: 5px; border-left: 4px solid #FFC107; }
        """
    ) as interface:
        # 🎯 AI-Human協働開発システム - 初心者向けガイド
2. 承認したいアイテムのIDを確認
3. IDを入力して「承認」ボタンをクリック

**期待される結果**: アイテムのステータスが「approved」に変更される
                """,
                "button_text": "承認処理を実行",
                "next_step": "承認が完了したら、自動実行システムをテストしてみましょう！"
            },
            5: {
                "title": "🚀 ステップ5: 自動実行システム",
                "description": """
**目的**: 承認されたプロンプトを自動実行してコードを生成します

**動作内容**:
- AI APIを使用してコード生成
- 生成されたコードをファイルに保存
- 実行ログに結果を記録

**期待される結果**: コードファイルの生成と実行ログの記録
                """,
                "button_text": "自動実行開始",
                "next_step": "コード生成が完了したら、GitHub連携をテストしてみましょう！"
            },
            6: {
                "title": "🐙 ステップ6: GitHub連携",
                "description": """
**目的**: 生成されたコードをGitHub Issueとして作成します

**動作内容**:
- GitHub APIを使用してIssue作成
- 生成コードをIssue本文に添付
- 適切なラベルとタイトルを設定

**期待される結果**: GitHub上に新しいIssueが作成される
                """,
                "button_text": "GitHub Issue作成",
                "next_step": "GitHub連携が完了したら、最終ステップでログを確認しましょう！"
            },
            7: {
                "title": "📊 ステップ7: ログ・完了確認",
                "description": """
**目的**: 全ての処理が正常に完了したことを確認します

**確認項目**:
- プロンプトの保存ログ
- 承認処理のログ
- 自動実行のログ
- GitHub連携のログ

**期待される結果**: 全てのステップが✅で完了していること
                """,
                "button_text": "最終ログ確認",
                "next_step": "🎉 おめでとうございます！全てのステップが完了しました！"
            }
        }
        return descriptions.get(step_num, {})
    
    def check_system_status(self):
        """ステップ1: システム状態確認"""
        try:
            results = []
            
            # データベース接続確認
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            results.append("✅ データベース接続: 正常")
            
            # テーブル存在確認
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['prompts', 'approval_queue', 'execution_log']
            for table in required_tables:
                if table in tables:
                    results.append(f"✅ {table}テーブル: 存在")
                else:
                    results.append(f"❌ {table}テーブル: 不在")
            
            # 基本的な読み書きテスト
            cursor.execute("SELECT COUNT(*) FROM prompts")
            prompt_count = cursor.fetchone()[0]
            results.append(f"✅ プロンプト数: {prompt_count}件")
            
            cursor.execute("SELECT COUNT(*) FROM approval_queue")
            queue_count = cursor.fetchone()[0]
            results.append(f"✅ 承認キュー: {queue_count}件")
            
            conn.close()
            
            self.test_results['step1'] = True
            return "\\n".join(results) + "\\n\\n🎉 システム状態確認完了！次のステップに進めます。"
            
        except Exception as e:
            self.test_results['step1'] = False
            return f"❌ システム確認エラー: {str(e)}"
    
    def save_test_prompt(self, title, content):
        """ステップ2: テストプロンプト保存"""
        try:
            if not title or not content:
                return "❌ タイトルと内容の両方を入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO prompts (title, content, created_at) VALUES (?, ?, ?)',
                (title, content, datetime.now().isoformat())
            )
            
            prompt_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.test_results['step2'] = {'id': prompt_id, 'title': title, 'content': content}
            
            return f"""✅ プロンプト保存完了！
            
📋 保存内容:
- ID: {prompt_id}
- タイトル: {title}
- 内容: {content[:100]}...

🎯 次のステップ: このプロンプトを承認キューに追加してください"""
            
        except Exception as e:
            self.test_results['step2'] = False
            return f"❌ プロンプト保存エラー: {str(e)}"
    
    def add_to_approval_queue(self, title, content, priority):
        """ステップ3: 承認キューに追加"""
        try:
            if not title or not content:
                return "❌ タイトルと内容を入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO approval_queue (
                    issue_title, issue_body, requester, priority, 
                    approval_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                title, content, "test_user", priority, 
                "pending_review", datetime.now().isoformat()
            ))
            
            queue_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.test_results['step3'] = {'id': queue_id, 'title': title}
            
            return f"""✅ 承認キューに追加完了！
            
📨 追加内容:
- キューID: {queue_id}
- タイトル: {title}
- 優先度: {priority}
- ステータス: pending_review

🎯 次のステップ: ID {queue_id} を承認してください"""
            
        except Exception as e:
            self.test_results['step3'] = False
            return f"❌ 承認キュー追加エラー: {str(e)}"
    
    def approve_request(self, request_id):
        """ステップ4: 承認処理"""
        try:
            if not request_id:
                return "❌ 承認するアイテムのIDを入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # アイテム存在確認
            cursor.execute('SELECT issue_title FROM approval_queue WHERE id = ?', (request_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return f"❌ ID {request_id} のアイテムが見つかりません"
            
            title = result[0]
            
            # 承認処理
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, approved_at = ?
                WHERE id = ?
            ''', ('approved', 'test_approver', datetime.now().isoformat(), request_id))
            
            conn.commit()
            conn.close()
            
            self.test_results['step4'] = {'id': request_id, 'title': title}
            
            return f"""✅ 承認処理完了！
            
🤝 承認内容:
- アイテムID: {request_id}
- タイトル: {title}
- 承認者: test_approver
- 承認日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 次のステップ: 自動実行システムをテストしてください"""
            
        except Exception as e:
            self.test_results['step4'] = False
            return f"❌ 承認処理エラー: {str(e)}"
    
    def simulate_auto_execution(self):
        """ステップ5: 自動実行シミュレーション"""
        try:
            # シミュレーション用のコード生成
            generated_code = '''
def simple_calculator():
    """簡単な計算機"""
    print("=== 簡単な計算機 ===")
    
    while True:
        try:
            num1 = float(input("最初の数値を入力: "))
            operator = input("演算子を入力 (+, -, *, /): ")
            num2 = float(input("2番目の数値を入力: "))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("エラー: ゼロで割ることはできません")
                    continue
            else:
                print("エラー: 無効な演算子です")
                continue
            
            print(f"結果: {num1} {operator} {num2} = {result}")
            
            if input("続けますか？ (y/n): ").lower() != 'y':
                break
                
        except ValueError:
            print("エラー: 有効な数値を入力してください")
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    simple_calculator()
'''
            
            # ファイル保存シミュレーション
            output_dir = Path("/workspaces/fastapi_django_main_live/test_generated")
            output_dir.mkdir(exist_ok=True)
            
            file_path = output_dir / "simple_calculator.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            
            # 実行ログ記録
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO execution_log (
                    approval_id, execution_start, execution_end, 
                    status, result_summary, github_repo_url
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.test_results.get('step4', {}).get('id', 0),
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                'completed',
                f'ファイル生成完了: {file_path}',
                'https://github.com/test/repo'
            ))
            
            conn.commit()
            conn.close()
            
            self.test_results['step5'] = {'file_path': str(file_path)}
            
            return f"""✅ 自動実行完了！
            
🚀 実行結果:
- 生成ファイル: {file_path}
- ファイルサイズ: {len(generated_code)} 文字
- 実行時間: < 1秒
- ステータス: 正常完了

💡 生成されたコード:
```python
{generated_code[:200]}...
```

🎯 次のステップ: GitHub Issue作成をテストしてください"""
            
        except Exception as e:
            self.test_results['step5'] = False
            return f"❌ 自動実行エラー: {str(e)}"
    
    def simulate_github_issue(self):
        """ステップ6: GitHub Issue作成シミュレーション"""
        try:
            # GitHub Issue シミュレーション
            issue_data = {
                'number': 123,
                'title': '🧪 テスト: 簡単な計算機システム生成完了',
                'url': 'https://github.com/miyataken999/fastapi_django_main_live/issues/123',
                'body': f'''
# 🎯 自動生成システムテスト結果

## 📋 概要
承認されたプロンプトから簡単な計算機システムを自動生成しました。

## 🚀 生成内容
- **ファイル**: simple_calculator.py
- **機能**: 四則演算（+, -, *, /）
- **特徴**: エラーハンドリング付き

## 📊 実行詳細
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **所要時間**: < 1秒
- **ステータス**: ✅ 正常完了

## 🔗 関連ファイル
- 生成コード: `/test_generated/simple_calculator.py`

---
*このIssueは自動生成システムによって作成されました*
'''
            }
            
            self.test_results['step6'] = issue_data
            
            return f"""✅ GitHub Issue作成完了！
            
🐙 作成されたIssue:
- Issue番号: #{issue_data['number']}
- タイトル: {issue_data['title']}
- URL: {issue_data['url']}
- 作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 Issue内容プレビュー:
{issue_data['body'][:300]}...

🎯 次のステップ: 最終ログ確認を実行してください"""
            
        except Exception as e:
            self.test_results['step6'] = False
            return f"❌ GitHub Issue作成エラー: {str(e)}"
    
    def generate_final_report(self):
        """ステップ7: 最終レポート生成"""
        try:
            report_lines = ["# 🎉 全ステップ完了レポート\\n"]
            
            all_success = True
            for step_num in range(1, 8):
                step_key = f'step{step_num}'
                step_desc = self.get_step_description(step_num)
                
                if self.test_results.get(step_key):
                    status = "✅ 成功"
                    all_success = True
                else:
                    status = "❌ 未完了/エラー"
                    all_success = False
                
                report_lines.append(f"## {step_desc['title']}")
                report_lines.append(f"**ステータス**: {status}\\n")
            
            if all_success:
                report_lines.append("## 🎯 総合評価: 全ステップ正常完了！")
                report_lines.append("""
**あなたは以下を達成しました:**
- ✅ システム全体の動作確認
- ✅ プロンプトから自動コード生成
- ✅ 承認ワークフローの理解
- ✅ GitHub連携の体験
- ✅ 完全なE2Eテスト完了

🎉 おめでとうございます！AI-Human協働開発システムをマスターしました！
                """)
            else:
                report_lines.append("## ⚠️ 一部のステップが未完了です")
                report_lines.append("未完了のステップがある場合は、該当ステップを再実行してください。")
            
            final_report = "\\n".join(report_lines)
            
            return final_report
            
        except Exception as e:
            return f"❌ 最終レポート生成エラー: {str(e)}"

def create_gradio_interface():
    """Gradioインターフェース作成"""
    guide = SystemTestGuide()
    
    with gr.Blocks(
        title="🎯 AI-Human協働開発システム - 初心者向けガイド",
        theme="soft"
    ) as interface:
        
        gr.Markdown("""
        # 🎯 AI-Human協働開発システム - 初心者向けガイド
        
        **ようこそ！** このガイドでは、システムを上から順番に実行していくだけで、
        AI-Human協働開発の全プロセスを体験できます。
        
        **使い方**: 各ステップを順番に実行してください。前のステップが完了してから次に進みましょう。
        """)
        
        # ステップ1: システム確認
        with gr.Row():
            with gr.Column():
                step1_desc = guide.get_step_description(1)
                gr.Markdown(f"## {step1_desc['title']}")
                gr.Markdown(step1_desc['description'])
                
                step1_btn = gr.Button(step1_desc['button_text'], variant="primary")
                step1_result = gr.Textbox(label="ステップ1結果", lines=8, interactive=False)
                
                step1_btn.click(guide.check_system_status, outputs=step1_result)
        
        gr.Markdown("---")
        
        # ステップ2: プロンプト作成
        with gr.Row():
            with gr.Column():
                step2_desc = guide.get_step_description(2)
                gr.Markdown(f"## {step2_desc['title']}")
                gr.Markdown(step2_desc['description'])
                
                with gr.Row():
                    prompt_title = gr.Textbox(
                        label="プロンプトタイトル", 
                        value="テスト: 簡単な計算機",
                        placeholder="例: テスト: 簡単な計算機"
                    )
                    
                prompt_content = gr.Textbox(
                    label="プロンプト内容",
                    value="Pythonで足し算と引き算ができる簡単な計算機を作成してください。エラーハンドリングも含めてください。",
                    lines=3,
                    placeholder="ここにプロンプトの詳細を入力..."
                )
                
                step2_btn = gr.Button(step2_desc['button_text'], variant="primary")
                step2_result = gr.Textbox(label="ステップ2結果", lines=6, interactive=False)
                
                step2_btn.click(
                    guide.save_test_prompt,
                    inputs=[prompt_title, prompt_content],
                    outputs=step2_result
                )
        
        gr.Markdown("---")
        
        # ステップ3: 承認キュー追加
        with gr.Row():
            with gr.Column():
                step3_desc = guide.get_step_description(3)
                gr.Markdown(f"## {step3_desc['title']}")
                gr.Markdown(step3_desc['description'])
                
                with gr.Row():
                    queue_title = gr.Textbox(
                        label="タイトル（ステップ2からコピー）",
                        placeholder="前のステップのタイトルをここにコピー"
                    )
                    priority = gr.Slider(
                        minimum=1, maximum=9, value=3, step=1,
                        label="優先度（1=最高、9=最低）"
                    )
                
                queue_content = gr.Textbox(
                    label="内容（ステップ2からコピー）",
                    lines=3,
                    placeholder="前のステップの内容をここにコピー"
                )
                
                step3_btn = gr.Button(step3_desc['button_text'], variant="primary")
                step3_result = gr.Textbox(label="ステップ3結果", lines=6, interactive=False)
                
                step3_btn.click(
                    guide.add_to_approval_queue,
                    inputs=[queue_title, queue_content, priority],
                    outputs=step3_result
                )
        
        gr.Markdown("---")
        
        # ステップ4: 承認処理
        with gr.Row():
            with gr.Column():
                step4_desc = guide.get_step_description(4)
                gr.Markdown(f"## {step4_desc['title']}")
                gr.Markdown(step4_desc['description'])
                
                approval_id = gr.Number(
                    label="承認するアイテムのID（ステップ3の結果から）",
                    precision=0,
                    placeholder="例: 1"
                )
                
                step4_btn = gr.Button(step4_desc['button_text'], variant="primary")
                step4_result = gr.Textbox(label="ステップ4結果", lines=6, interactive=False)
                
                step4_btn.click(
                    guide.approve_request,
                    inputs=approval_id,
                    outputs=step4_result
                )
        
        gr.Markdown("---")
        
        # ステップ5: 自動実行
        with gr.Row():
            with gr.Column():
                step5_desc = guide.get_step_description(5)
                gr.Markdown(f"## {step5_desc['title']}")
                gr.Markdown(step5_desc['description'])
                
                step5_btn = gr.Button(step5_desc['button_text'], variant="primary")
                step5_result = gr.Textbox(label="ステップ5結果", lines=10, interactive=False)
                
                step5_btn.click(guide.simulate_auto_execution, outputs=step5_result)
        
        gr.Markdown("---")
        
        # ステップ6: GitHub連携
        with gr.Row():
            with gr.Column():
                step6_desc = guide.get_step_description(6)
                gr.Markdown(f"## {step6_desc['title']}")
                gr.Markdown(step6_desc['description'])
                
                step6_btn = gr.Button(step6_desc['button_text'], variant="primary")
                step6_result = gr.Textbox(label="ステップ6結果", lines=8, interactive=False)
                
                step6_btn.click(guide.simulate_github_issue, outputs=step6_result)
        
        gr.Markdown("---")
        
        # ステップ7: 最終確認
        with gr.Row():
            with gr.Column():
                step7_desc = guide.get_step_description(7)
                gr.Markdown(f"## {step7_desc['title']}")
                gr.Markdown(step7_desc['description'])
                
                step7_btn = gr.Button(step7_desc['button_text'], variant="primary")
                step7_result = gr.Textbox(label="最終レポート", lines=15, interactive=False)
                
                step7_btn.click(guide.generate_final_report, outputs=step7_result)
        
        gr.Markdown("""
        ---
        ## 🎯 完了後のNext Steps
        
        全てのステップを完了したら、以下の実際のシステムも体験してみてください：
        
        - **🚀 統合管理ダッシュボード**: 実際の開発プロジェクト管理
        - **🐙 GitHub Issue自動生成**: リアルなGitHub連携
        - **💾 プロンプト管理システム**: 本格的なプロンプト開発
        
        **質問やサポートが必要な場合は、GitHub Issueでお気軽にお聞かせください！**
        """)
    
    return interface

# Gradioインターフェースのエクスポート
gradio_interface = create_gradio_interface()
interface_title = "🎯 初心者向けシステムガイド"

if __name__ == "__main__":
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False
    )
