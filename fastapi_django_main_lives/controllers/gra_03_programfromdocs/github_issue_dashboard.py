#!/usr/bin/env python3
"""
GitHub ISSUE自動化ダッシュボード - メインアプリ統合版
メインアプリケーション（7860番ポート）に統合されるGradioインターフェース
"""

import gradio as gr
import sqlite3
import os
import threading
import time
from datetime import datetime
from pathlib import Path
import importlib.util

# 既存のモジュールを動的にインポート
def load_module_from_path(module_name: str, file_path: str):
    """ファイルパスからモジュールを動的に読み込み"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"Failed to load {module_name}: {e}")
    return None

# GitHub ISSUE監視モジュールを読み込み
base_path = "/workspaces/fastapi_django_main_live/controllers/gra_03_programfromdocs"
github_monitor_module = load_module_from_path("github_issue_monitor", f"{base_path}/github_issue_monitor.py")
system_automation_module = load_module_from_path("system_automation", f"{base_path}/system_automation.py")

class GitHubIssueDashboard:
    """GitHub ISSUE自動化ダッシュボード"""
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_owner = "miyataken999"
        self.repo_name = "fastapi_django_main_live"
        self.issue_monitor = None
        self.automation = None
        
        # モジュールが正常に読み込まれた場合のみ初期化
        if github_monitor_module and system_automation_module and self.github_token:
            try:
                self.automation = system_automation_module.SystemAutomation(self.github_token)
            except Exception as e:
                print(f"Failed to initialize SystemAutomation: {e}")
    
    def get_system_status(self):
        """システム状況取得"""
        status = {
            'github_api': 'Unknown',
            'issue_monitoring': 'Stopped',
            'prompt_database': 'Unknown',
            'gpt_engineer': 'Unknown',
            'automation': 'Unknown'
        }
        
        # GitHub API状況
        if self.github_token and len(self.github_token) > 10:
            status['github_api'] = 'Connected'
        else:
            status['github_api'] = 'No Token'
        
        # ISSUE監視状況
        if self.issue_monitor and hasattr(self.issue_monitor, 'monitoring') and self.issue_monitor.monitoring:
            status['issue_monitoring'] = 'Running'
        
        # プロンプトDB状況
        try:
            prompt_db = '/workspaces/fastapi_django_main_live/prompts.db'
            if Path(prompt_db).exists():
                status['prompt_database'] = 'Active'
            else:
                status['prompt_database'] = 'Not Found'
        except:
            status['prompt_database'] = 'Error'
        
        # GPT-ENGINEER状況
        if os.environ.get('OPENAI_API_KEY'):
            status['gpt_engineer'] = 'API Key Set'
        else:
            status['gpt_engineer'] = 'No API Key'
        
        # 自動化システム状況
        if self.automation:
            status['automation'] = 'Ready'
        else:
            status['automation'] = 'Not Configured'
        
        return status
    
    def get_recent_activities(self):
        """最近のアクティビティ取得"""
        activities = []
        
        try:
            # プロンプト登録履歴
            prompt_db = '/workspaces/fastapi_django_main_live/prompts.db'
            if Path(prompt_db).exists():
                conn = sqlite3.connect(prompt_db)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT title, created_at 
                    FROM prompts 
                    ORDER BY created_at DESC 
                    LIMIT 5
                ''')
                prompts = cursor.fetchall()
                
                for prompt in prompts:
                    activities.append({
                        'time': prompt[1],
                        'type': 'Prompt',
                        'title': prompt[0],
                        'status': 'completed',
                        'system_type': 'internal'
                    })
                
                conn.close()
            
            # GitHub ISSUE履歴
            issue_db = '/workspaces/fastapi_django_main_live/github_issues.db'
            if Path(issue_db).exists():
                conn = sqlite3.connect(issue_db)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT title, status, processed_at, issue_number
                    FROM processed_issues 
                    ORDER BY processed_at DESC 
                    LIMIT 5
                ''')
                issues = cursor.fetchall()
                
                for issue in issues:
                    activities.append({
                        'time': issue[2],
                        'type': 'GitHub Issue',
                        'title': f"#{issue[3]} {issue[0]}",
                        'status': issue[1],
                        'system_type': 'external'
                    })
                
                conn.close()
        
        except Exception as e:
            activities.append({
                'time': datetime.now().isoformat(),
                'type': 'Error',
                'title': f'Activity fetch error: {str(e)}',
                'status': 'error',
                'system_type': 'system'
            })
        
        # 時間順でソート
        activities.sort(key=lambda x: x['time'], reverse=True)
        return activities[:15]
    
    def start_issue_monitoring(self):
        """ISSUE監視開始"""
        if not self.github_token or len(self.github_token) < 10:
            return "❌ GitHub Token が設定されていません", ""
        
        if not github_monitor_module:
            return "❌ GitHub監視モジュールが利用できません", ""
        
        try:
            if self.issue_monitor and hasattr(self.issue_monitor, 'monitoring') and self.issue_monitor.monitoring:
                return "⚠️ 監視は既に実行中です", ""
            
            self.issue_monitor = github_monitor_module.GitHubIssueMonitor(
                self.github_token, 
                self.repo_owner, 
                self.repo_name
            )
            self.issue_monitor.start_monitoring()
            
            return "✅ GitHub ISSUE監視を開始しました", self.format_monitoring_status()
        
        except Exception as e:
            return f"❌ 監視開始エラー: {str(e)}", ""
    
    def stop_issue_monitoring(self):
        """ISSUE監視停止"""
        try:
            if self.issue_monitor and hasattr(self.issue_monitor, 'stop_monitoring'):
                self.issue_monitor.stop_monitoring()
                return "⏹️ GitHub ISSUE監視を停止しました", ""
            else:
                return "⚠️ 監視は実行されていません", ""
        
        except Exception as e:
            return f"❌ 監視停止エラー: {str(e)}", ""
    
    def format_system_status(self):
        """システム状況のフォーマット"""
        status = self.get_system_status()
        
        formatted = "🖥️ **システム状況**\n\n"
        
        status_icons = {
            'Connected': '✅',
            'Running': '🟢',
            'Active': '✅',
            'Ready': '✅',
            'API Key Set': '✅',
            'Stopped': '🔴',
            'No Token': '❌',
            'No API Key': '⚠️',
            'Not Configured': '⚠️',
            'Error': '❌',
            'Unknown': '❓'
        }
        
        items = [
            ('GitHub API', status['github_api']),
            ('ISSUE監視', status['issue_monitoring']),
            ('プロンプトDB', status['prompt_database']),
            ('GPT-ENGINEER', status['gpt_engineer']),
            ('自動化システム', status['automation'])
        ]
        
        for name, state in items:
            icon = next((icon for key, icon in status_icons.items() if key in state), '❓')
            formatted += f"{icon} **{name}**: {state}\n"
        
        return formatted
    
    def format_recent_activities(self):
        """最近のアクティビティのフォーマット"""
        activities = self.get_recent_activities()
        
        if not activities:
            return "📭 最近のアクティビティはありません"
        
        formatted = "📋 **最近のアクティビティ**\n\n"
        
        for activity in activities:
            time_str = activity['time'][:16] if activity['time'] else 'Unknown'
            type_icon = {
                'Prompt': '📝',
                'GitHub Issue': '🔗',
                'Error': '❌'
            }.get(activity['type'], '📌')
            
            status_icon = {
                'completed': '✅',
                'running': '🔄',
                'pending': '⏳',
                'failed': '❌',
                'approved': '👍',
                'processing': '🔄',
                'error': '❌'
            }.get(activity['status'], '❓')
            
            formatted += f"{type_icon} **{activity['title'][:50]}**\n"
            formatted += f"   {status_icon} {activity['status']} - {time_str}\n\n"
        
        return formatted
    
    def format_monitoring_status(self):
        """監視状況のフォーマット"""
        if not self.issue_monitor:
            return "🔴 ISSUE監視: 未開始"
        
        try:
            if hasattr(self.issue_monitor, 'get_monitoring_status'):
                status = self.issue_monitor.get_monitoring_status()
                formatted = f"""🎯 **ISSUE監視状況**

📡 **監視状態**: {'🟢 稼働中' if status.get('monitoring', False) else '🔴 停止'}
📁 **リポジトリ**: {status.get('repo', 'Unknown')}
⏱️ **チェック間隔**: {status.get('check_interval', 'Unknown')}秒
📊 **処理済み**: {status.get('processed_count', 0)}件
"""
                return formatted
            else:
                return "🔴 ISSUE監視: ステータス不明"
        except Exception as e:
            return f"🔴 ISSUE監視: エラー ({str(e)})"

# Gradioインターフェース定義
def gradio_interface():
    """メインアプリに統合されるGradioインターフェース"""
    
    dashboard = GitHubIssueDashboard()
    
    with gr.Blocks(title="🚀 GitHub ISSUE自動化", theme="soft") as interface:
        gr.Markdown("# 🚀 GitHub ISSUE自動化システム")
        gr.Markdown("""
        **GitHub ISSUE監視 + AI解析 + GPT-ENGINEER自動生成**の統合システム
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # システム状況
                system_status = gr.Markdown(
                    value=dashboard.format_system_status(),
                    label="システム状況"
                )
                
                # 監視制御
                with gr.Group():
                    gr.Markdown("## 🎛️ 監視制御")
                    
                    with gr.Row():
                        start_btn = gr.Button("🚀 ISSUE監視開始", variant="primary")
                        stop_btn = gr.Button("⏹️ 監視停止", variant="secondary")
                    
                    monitor_result = gr.Textbox(
                        label="実行結果",
                        lines=2,
                        interactive=False
                    )
                    
                    monitoring_status = gr.Markdown(
                        value=dashboard.format_monitoring_status(),
                        label="監視状況"
                    )
            
            with gr.Column(scale=3):
                # 最近のアクティビティ
                activities = gr.Markdown(
                    value=dashboard.format_recent_activities(),
                    label="最近のアクティビティ"
                )
        
        with gr.Row():
            # 更新ボタン
            refresh_btn = gr.Button("🔄 画面更新", variant="secondary")
            
            # 設定リンク
            gr.Markdown("""
            ### 🔗 クイックリンク
            - [GitHub Repository](https://github.com/miyataken999/fastapi_django_main_live) - ISSUE投稿
            - [API Documentation](http://localhost:8000/docs) - 生成システムAPI
            """)
        
        # 設定情報表示
        with gr.Accordion("⚙️ システム設定", open=False):
            gr.Markdown(f"""
            ### 📋 現在の設定
            
            **GitHub設定**
            - Repository: {dashboard.repo_owner}/{dashboard.repo_name}
            - Token: {'✅ 設定済み' if dashboard.github_token else '❌ 未設定'}
            
            **API設定**
            - OpenAI: {'✅ 設定済み' if os.environ.get('OPENAI_API_KEY') else '❌ 未設定'}
            
            **データベース**
            - プロンプトDB: /workspaces/fastapi_django_main_live/prompts.db
            - ISSUE履歴DB: /workspaces/fastapi_django_main_live/github_issues.db
            
            **監視設定**
            - チェック間隔: 30秒
            - 対象ラベル: system-generation, prompt-request
            """)
        
        # イベントハンドラー
        def refresh_all():
            return (
                dashboard.format_system_status(),
                dashboard.format_recent_activities(),
                dashboard.format_monitoring_status()
            )
        
        start_btn.click(
            fn=dashboard.start_issue_monitoring,
            outputs=[monitor_result, monitoring_status]
        )
        
        stop_btn.click(
            fn=dashboard.stop_issue_monitoring,
            outputs=[monitor_result, monitoring_status]
        )
        
        refresh_btn.click(
            fn=refresh_all,
            outputs=[system_status, activities, monitoring_status]
        )
        
        # 初期表示時に自動更新
        interface.load(
            fn=refresh_all,
            outputs=[system_status, activities, monitoring_status]
        )
    
    return interface

# インターフェースタイトル（自動検出用）
interface_title = "🚀 GitHub ISSUE自動化"

if __name__ == "__main__":
    # テスト実行
    interface = gradio_interface()
    interface.launch(share=False, server_name="0.0.0.0", server_port=7865)
