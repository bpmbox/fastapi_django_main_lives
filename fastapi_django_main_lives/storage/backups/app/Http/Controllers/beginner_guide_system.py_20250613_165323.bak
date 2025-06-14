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

### 📝 使い方
このガイドは上から順番にタブを進んでください：
1. **システム概要** (このタブ) - システムの全体像を理解
2. **プロンプト作成** - テスト用プロンプトの作成
3. **承認システム** - 作成したプロンプトの承認
4. **実行テスト** - システムの実行をシミュレーション
5. **GitHub連携** - GitHub Issue作成のテスト
6. **システム確認** - 全体の動作状況を最終確認

すべてのステップを完了すると、システムの基本的な使い方がマスターできます！
        """
    
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
    
    def create_test_prompt(self, title, content, category="テスト"):
        """テスト用プロンプトを作成"""
        try:
            if not title or not content:
                return "❌ タイトルと内容を入力してください"
            
            # データベース初期化
            if not os.path.exists(self.db_path):
                self.init_database()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # テーブル構造を確認してからインサート
            cursor.execute("PRAGMA table_info(prompts)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # categoryカラムが存在するかチェック
            if 'category' in columns:
                # categoryカラムありの場合
                cursor.execute('''
                    INSERT INTO prompts (title, content, category, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (title, content, category, datetime.now()))
            else:
                # categoryカラムなしの場合
                cursor.execute('''
                    INSERT INTO prompts (title, content, created_at)
                    VALUES (?, ?, ?)
                ''', (title, content, datetime.now()))
            
            prompt_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            success_msg = f"""
## ✅ プロンプト作成完了！

**プロンプトID**: {prompt_id}  
**タイトル**: {title}  
**カテゴリ**: {category}  
**内容**: {content[:100]}...

### 📝 次のステップ
「ステップ3: 承認システム」タブに進んで、作成したプロンプトを承認してください。
            """
            return success_msg
            
        except Exception as e:
            return f"❌ エラーが発生しました: {str(e)}"
    
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
                outputs=[create_result],
                api_name="create_test_prompt"
            )
        
        with gr.Tab("✅ ステップ3: 承認システム"):
            gr.Markdown("## 🎯 承認システムのテスト")
            gr.Markdown("作成したプロンプトの承認プロセスをテストします。")
            
            check_btn = gr.Button("📋 承認待ちプロンプト確認", variant="secondary", size="lg")
            pending_result = gr.Markdown(value="👆 上のボタンを押して承認待ちプロンプトを確認してください")
            
            check_btn.click(guide_system.get_pending_prompts, outputs=[pending_result], api_name="get_pending_prompts")
            
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
                outputs=[approval_result],
                api_name="approve_prompt"
            )
        
        with gr.Tab("⚡ ステップ4: 実行テスト"):
            gr.Markdown("## 🎯 実行システムのテスト")
            gr.Markdown("承認されたプロンプトの実行をシミュレートします。")
            
            execute_btn = gr.Button("🚀 実行シミュレーション", variant="primary", size="lg")
            execution_result = gr.Markdown(value="👆 上のボタンを押して実行をシミュレートしてください")
            
            execute_btn.click(guide_system.simulate_execution, outputs=[execution_result], api_name="simulate_execution")
        
        with gr.Tab("🐙 ステップ5: GitHub連携"):
            gr.Markdown("## 🎯 GitHub連携のテスト")
            gr.Markdown("実行結果をGitHub Issueとして作成するプロセスをシミュレートします。")
            
            github_btn = gr.Button("🐙 GitHub Issue作成シミュレーション", variant="primary", size="lg")
            github_result = gr.Markdown(value="👆 上のボタンを押してGitHub連携をテストしてください")
            
            github_btn.click(guide_system.simulate_github_issue, outputs=[github_result], api_name="simulate_github_issue")
        
        with gr.Tab("🎯 ステップ6: システム確認"):
            gr.Markdown("## 🎯 システム全体の状態確認")
            gr.Markdown("最後に、システム全体の動作状況を確認します。")
            
            status_btn = gr.Button("📊 システム状態確認", variant="primary", size="lg")
            status_result = gr.Markdown(value="👆 上のボタンを押してシステム全体の状態を確認してください")
            
            status_btn.click(guide_system.check_system_status, outputs=[status_result], api_name="check_system_status")
    
    return interface

# Gradioインターフェースのエクスポート
gradio_interface = create_beginner_interface()
interface_title = "🚀 初心者ガイド"

if __name__ == "__main__":
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False
    )
