"""
システム統合管理ダッシュボード
GPT-ENGINEERで生成されたシステムの統合管理
"""

import gradio as gr
import sqlite3
import os
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List

class SystemDashboard:
    """システム統合管理ダッシュボード"""
    
    def __init__(self, db_path: str = "prompts.db"):
        self.db_path = db_path
        self.workspace_root = Path("/workspaces/fastapi_django_main_live")
        
    def get_system_overview(self) -> Dict:
        """システム全体の概要を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 基本統計
            cursor.execute('SELECT COUNT(*) FROM prompts')
            total_prompts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM prompts WHERE execution_status = "completed"')
            completed_systems = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM prompts WHERE execution_status = "running"')
            running_systems = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM prompts WHERE execution_status = "failed"')
            failed_systems = cursor.fetchone()[0]
            
            # システムタイプ別統計
            cursor.execute('''
                SELECT system_type, COUNT(*) 
                FROM prompts 
                GROUP BY system_type
            ''')
            system_types = dict(cursor.fetchall())
            
            # 最近の実行履歴
            cursor.execute('''
                SELECT title, execution_status, created_at 
                FROM prompts 
                ORDER BY created_at DESC 
                LIMIT 10
            ''')
            recent_executions = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_prompts': total_prompts,
                'completed_systems': completed_systems,
                'running_systems': running_systems,
                'failed_systems': failed_systems,
                'system_types': system_types,
                'recent_executions': recent_executions,
                'success_rate': (completed_systems / total_prompts * 100) if total_prompts > 0 else 0
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def scan_generated_systems(self) -> List[Dict]:
        """生成されたシステムをスキャン"""
        systems = []
        
        # Controllers ディレクトリをスキャン
        controllers_dir = self.workspace_root / "controllers"
        if controllers_dir.exists():
            for subdir in controllers_dir.iterdir():
                if subdir.is_dir() and not subdir.name.startswith('.'):
                    py_files = list(subdir.glob("*.py"))
                    if py_files:
                        systems.append({
                            'name': subdir.name,
                            'type': 'controller',
                            'path': str(subdir),
                            'files': len(py_files),
                            'size': sum(f.stat().st_size for f in py_files if f.exists())
                        })
        
        # Routers ディレクトリをスキャン
        routers_dir = self.workspace_root / "routers"
        if routers_dir.exists():
            for py_file in routers_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    systems.append({
                        'name': py_file.stem,
                        'type': 'router',
                        'path': str(py_file),
                        'files': 1,
                        'size': py_file.stat().st_size if py_file.exists() else 0
                    })
        
        return systems
    
    def get_system_health(self) -> Dict:
        """システムヘルス状態を取得"""
        health = {
            'database': False,
            'workspace': False,
            'git': False,
            'dependencies': False
        }
        
        try:
            # データベース接続確認
            conn = sqlite3.connect(self.db_path)
            conn.close()
            health['database'] = True
        except:
            pass
        
        # ワークスペースディレクトリ確認
        health['workspace'] = self.workspace_root.exists()
        
        # Git確認
        try:
            os.system('git --version > /dev/null 2>&1')
            health['git'] = True
        except:
            pass
        
        # 依存関係確認
        try:
            import gradio, sqlite3, requests
            health['dependencies'] = True
        except:
            pass
        
        return health

def create_dashboard_interface():
    """ダッシュボードのGradioインターフェース"""
    
    dashboard = SystemDashboard()
    
    def refresh_overview():
        """概要情報を更新"""
        overview = dashboard.get_system_overview()
        
        if 'error' in overview:
            return f"❌ エラー: {overview['error']}", "", ""
        
        # 基本統計
        stats = f"""📊 **システム統計**
- 📝 総プロンプト数: {overview['total_prompts']}
- ✅ 完了済みシステム: {overview['completed_systems']}
- 🚀 実行中: {overview['running_systems']}
- ❌ 失敗: {overview['failed_systems']}
- 📈 成功率: {overview['success_rate']:.1f}%
"""
        
        # システムタイプ別統計
        types_stats = "🏗️ **システムタイプ別**\n"
        type_icons = {
            'web_system': '🌐',
            'api_system': '🔗',
            'interface_system': '🖥️',
            'line_system': '📱',
            'ai_generated': '🤖',
            'general': '📄'
        }
        
        for system_type, count in overview['system_types'].items():
            icon = type_icons.get(system_type, '📄')
            types_stats += f"- {icon} {system_type}: {count}件\n"
        
        # 最近の実行履歴
        recent = "📅 **最近の実行履歴**\n"
        for title, status, created_at in overview['recent_executions']:
            status_icon = {'pending': '⏳', 'running': '🚀', 'completed': '✅', 'failed': '❌'}.get(status, '⏳')
            date_str = created_at[:16] if created_at else ""
            recent += f"- {status_icon} {title[:30]}... ({date_str})\n"
        
        return stats, types_stats, recent
    
    def refresh_systems():
        """生成されたシステム一覧を更新"""
        systems = dashboard.scan_generated_systems()
        
        if not systems:
            return [["システムが見つかりません", "", "", "", ""]]
        
        table_data = []
        for system in systems:
            size_mb = system['size'] / (1024 * 1024)
            table_data.append([
                system['name'],
                system['type'],
                str(system['files']),
                f"{size_mb:.2f} MB",
                system['path']
            ])
        
        return table_data
    
    def refresh_health():
        """システムヘルス状態を更新"""
        health = dashboard.get_system_health()
        
        health_status = "🏥 **システムヘルス**\n"
        for component, status in health.items():
            icon = "✅" if status else "❌"
            health_status += f"- {icon} {component}: {'正常' if status else '異常'}\n"
        
        overall_health = sum(health.values()) / len(health) * 100
        health_status += f"\n📊 **総合ヘルス: {overall_health:.1f}%**"
        
        return health_status
    
    with gr.Blocks(title="🚀 システム統合管理ダッシュボード") as interface:
        gr.Markdown("# 🚀 システム統合管理ダッシュボード")
        gr.Markdown("GPT-ENGINEERで生成されたシステムの統合管理・監視")
        
        with gr.Row():
            refresh_btn = gr.Button("🔄 全体更新", variant="primary")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📊 システム概要")
                overview_stats = gr.Markdown("読み込み中...")
                
                gr.Markdown("## 🏗️ システムタイプ")
                system_types = gr.Markdown("読み込み中...")
                
                gr.Markdown("## 🏥 システムヘルス")
                health_status = gr.Markdown("読み込み中...")
            
            with gr.Column(scale=2):
                gr.Markdown("## 📅 最近の実行履歴")
                recent_executions = gr.Markdown("読み込み中...")
                
                gr.Markdown("## 💾 生成されたシステム一覧")
                systems_table = gr.Dataframe(
                    headers=["システム名", "タイプ", "ファイル数", "サイズ", "パス"],
                    datatype=["str", "str", "str", "str", "str"],
                    value=[],
                    interactive=False
                )
        
        with gr.Row():
            gr.Markdown("## 📋 クイックアクション")
            with gr.Column():
                backup_btn = gr.Button("💾 データベースバックアップ")
                cleanup_btn = gr.Button("🧹 不要ファイル削除")
                export_btn = gr.Button("📤 システムエクスポート")
        
        # イベントハンドラー
        def full_refresh():
            stats, types, recent = refresh_overview()
            systems = refresh_systems()
            health = refresh_health()
            return stats, types, recent, systems, health
        
        refresh_btn.click(
            fn=full_refresh,
            outputs=[overview_stats, system_types, recent_executions, systems_table, health_status]
        )
        
        # 初期読み込み
        interface.load(
            fn=full_refresh,
            outputs=[overview_stats, system_types, recent_executions, systems_table, health_status]
        )
    
    return interface

# ダッシュボードインターフェースを作成
dashboard_interface = create_dashboard_interface()
