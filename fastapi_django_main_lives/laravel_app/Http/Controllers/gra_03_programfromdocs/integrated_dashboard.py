#!/usr/bin/env python3
"""
統合管理ダッシュボード - 最終版
GitHub ISSUE監視、GPT-ENGINEER統合、システム自動化の総合管理画面
"""

import gradio as gr
import sqlite3
import os
import threading
import time
from datetime import datetime
from pathlib import Path

# 依存モジュールの安全なインポート
try:
    from .github_issue_monitor import GitHubIssueMonitor
except ImportError:
    try:
        from github_issue_monitor import GitHubIssueMonitor
    except ImportError:
        # フォールバック: モックclass
        class GitHubIssueMonitor:
            def __init__(self, *args, **kwargs):
                self.monitoring = False
            def start_monitoring(self):
                return "⚠️ GitHub監視モジュールが利用できません"
            def stop_monitoring(self):
                return "⚠️ GitHub監視モジュールが利用できません"
            def get_monitoring_status(self):
                return {'monitoring': False, 'repo': 'N/A', 'check_interval': 0, 'processed_count': 0}

try:
    from .system_automation import SystemAutomation
except ImportError:
    try:
        from system_automation import SystemAutomation
    except ImportError:
        # フォールバック: モックclass
        class SystemAutomation:
            def __init__(self, *args, **kwargs):
                pass

class IntegratedDashboard:
    """統合管理ダッシュボード"""
    
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        self.repo_owner = "miyataken999"  # 実際のユーザー名
        self.repo_name = "fastapi_django_main_live"  # 実際のリポジトリ名
        self.issue_monitor = None
        self.automation = None
        
        if self.github_token and len(self.github_token) > 10:
            self.automation = SystemAutomation(self.github_token)
    
    def get_system_status(self):
        """システム全体の状況取得"""
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
        if self.issue_monitor and self.issue_monitor.monitoring:
            status['issue_monitoring'] = 'Running'
        
        # プロンプトDB状況
        try:
            conn = sqlite3.connect('/workspaces/fastapi_django_main_live/prompts.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM prompts')
            count = cursor.fetchone()[0]
            conn.close()
            status['prompt_database'] = f'Active ({count} prompts)'
        except:
            status['prompt_database'] = 'Error'
        
        # GPT-ENGINEER状況
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        if openai_key and len(openai_key) > 10:
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
            # プロンプト実行履歴
            conn = sqlite3.connect('/workspaces/fastapi_django_main_live/prompts.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, execution_status, created_at, system_type
                FROM prompts 
                ORDER BY created_at DESC 
                LIMIT 10
            ''')
            prompts = cursor.fetchall()
            
            for prompt in prompts:
                activities.append({
                    'time': prompt[2],
                    'type': 'Prompt',
                    'title': prompt[0],
                    'status': prompt[1],
                    'system_type': prompt[3]
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
        
        try:
            if self.issue_monitor and self.issue_monitor.monitoring:
                return "⚠️ 監視は既に実行中です", ""
            
            self.issue_monitor = GitHubIssueMonitor(
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
            if self.issue_monitor:
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
        
        status = self.issue_monitor.get_monitoring_status()
        
        formatted = f"""🎯 **ISSUE監視状況**

📡 **監視状態**: {'🟢 稼働中' if status['monitoring'] else '🔴 停止'}
📁 **リポジトリ**: {status['repo']}
⏱️ **チェック間隔**: {status['check_interval']}秒
📊 **処理済み**: {status['processed_count']}件
"""
        return formatted
    
    def create_dashboard_interface(self):
        """ダッシュボードインターフェース作成"""
        
        with gr.Blocks(title="🚀 統合管理ダッシュボード", theme="soft") as dashboard:
            gr.Markdown("# 🚀 統合プロンプト管理システム - 管理ダッシュボード")
            gr.Markdown("""
            **GitHub ISSUE監視 + GPT-ENGINEER自動生成 + システム統合**の総合管理画面
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # システム状況
                    system_status = gr.Markdown(
                        value=self.format_system_status(),
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
                            value=self.format_monitoring_status(),
                            label="監視状況"
                        )
                
                with gr.Column(scale=3):
                    # 最近のアクティビティ
                    activities = gr.Markdown(
                        value=self.format_recent_activities(),
                        label="最近のアクティビティ"
                    )
            
            with gr.Row():
                # 更新ボタン
                refresh_btn = gr.Button("🔄 画面更新", variant="secondary")
                
                # 設定リンク
                gr.Markdown("""
                ### 🔗 クイックリンク
                - [プロンプト管理](http://localhost:7861) - メインシステム
                - [GitHub Repository](https://github.com/miyataken999/fastapi_django_main_live) - ISSUE投稿
                - [API Documentation](http://localhost:8000/docs) - 生成システムAPI
                """)
            
            # 設定情報表示
            with gr.Accordion("⚙️ システム設定", open=False):
                config_info = gr.Markdown(f"""
                ### 📋 現在の設定
                
                **GitHub設定**
                - Repository: {self.repo_owner}/{self.repo_name}
                - Token: {'✅ 設定済み' if self.github_token else '❌ 未設定'}
                
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
                    self.format_system_status(),
                    self.format_recent_activities(),
                    self.format_monitoring_status()
                )
            
            start_btn.click(
                fn=self.start_issue_monitoring,
                outputs=[monitor_result, monitoring_status]
            )
            
            stop_btn.click(
                fn=self.stop_issue_monitoring,
                outputs=[monitor_result, monitoring_status]
            )
            
            refresh_btn.click(
                fn=refresh_all,
                outputs=[system_status, activities, monitoring_status]
            )
            
            # 自動更新（30秒間隔）
            def auto_refresh():
                while True:
                    time.sleep(30)
                    yield refresh_all()
            
            # 初期表示時に自動更新開始
            dashboard.load(
                fn=refresh_all,
                outputs=[system_status, activities, monitoring_status]
            )
        
        return dashboard

# メインアプリ用のGradioインターフェースオブジェクト
# Use a factory function to avoid rendering during import
def create_gradio_interface():
    dashboard_instance = IntegratedDashboard()
    return dashboard_instance.create_dashboard_interface()

gradio_interface = create_gradio_interface

# インターフェースタイトル（自動検出用）
interface_title = "🚀 統合管理ダッシュボード"

if __name__ == "__main__":
    # 直接実行時の処理
    interface = gradio_interface
    interface.launch(
        share=True,
        server_name="0.0.0.0", 
        server_port=7863
    )
