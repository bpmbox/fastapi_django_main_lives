"""
ハイブリッド承認システム
GitHub ISSUE → SQLite承認 → 実行 → GitHub結果通知
"""

import sqlite3
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class ApprovalStatus(Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved" 
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class HybridApprovalSystem:
    """GitHub ISSUE + SQLite承認システム"""
    
    def __init__(self, github_token: str, db_path: str = "prompts.db"):
        self.github_token = github_token
        self.db_path = db_path
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.init_approval_db()
    
    def init_approval_db(self):
        """承認管理用のテーブルを追加"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 承認管理テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approval_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                github_issue_number INTEGER,
                github_repo TEXT,
                issue_title TEXT,
                issue_body TEXT,
                requester TEXT,
                approval_status TEXT DEFAULT 'pending_review',
                priority INTEGER DEFAULT 5,
                estimated_time TEXT,
                reviewer_notes TEXT,
                approved_by TEXT,
                approved_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 実行ログテーブル  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                approval_id INTEGER,
                execution_start TIMESTAMP,
                execution_end TIMESTAMP,
                status TEXT,
                result_summary TEXT,
                github_repo_url TEXT,
                error_message TEXT,
                FOREIGN KEY (approval_id) REFERENCES approval_queue (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 承認システムデータベース初期化完了")
    
    def import_issue_to_approval_queue(self, repo_owner: str, repo_name: str, issue_number: int) -> Dict:
        """GitHub ISSUEを承認キューに追加"""
        try:
            # GitHub APIからISSUE情報を取得
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            issue_data = response.json()
            
            # 承認キューに追加
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 重複チェック
            cursor.execute(
                'SELECT id FROM approval_queue WHERE github_issue_number = ? AND github_repo = ?',
                (issue_number, f"{repo_owner}/{repo_name}")
            )
            
            if cursor.fetchone():
                conn.close()
                return {'success': False, 'error': 'ISSUE already in queue'}
            
            # 優先度を自動判定
            priority = self._calculate_priority(issue_data)
            estimated_time = self._estimate_execution_time(issue_data)
            
            cursor.execute('''
                INSERT INTO approval_queue 
                (github_issue_number, github_repo, issue_title, issue_body, 
                 requester, priority, estimated_time, approval_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                issue_number,
                f"{repo_owner}/{repo_name}",
                issue_data['title'],
                issue_data['body'],
                issue_data['user']['login'],
                priority,
                estimated_time,
                ApprovalStatus.PENDING_REVIEW.value
            ))
            
            approval_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # GitHub ISSUEにコメント追加
            self._post_approval_comment(repo_owner, repo_name, issue_number, approval_id)
            
            return {
                'success': True, 
                'approval_id': approval_id,
                'status': 'added_to_queue'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _calculate_priority(self, issue_data: Dict) -> int:
        """ISSUEの優先度を自動判定"""
        priority = 5  # デフォルト
        
        title = issue_data['title'].lower()
        body = (issue_data['body'] or '').lower()
        labels = [label['name'].lower() for label in issue_data.get('labels', [])]
        
        # 緊急度判定
        if any(word in title + body for word in ['urgent', '緊急', 'critical', '重要']):
            priority = 1
        elif any(word in title + body for word in ['security', 'セキュリティ', 'bug', 'バグ']):
            priority = 2
        elif any(word in title + body for word in ['api', 'database', 'データベース']):
            priority = 3
        elif any(word in title + body for word in ['enhancement', '機能追加', 'feature']):
            priority = 4
        
        # ラベルによる調整
        if 'high-priority' in labels:
            priority = min(priority, 2)
        elif 'low-priority' in labels:
            priority = max(priority, 6)
            
        return priority
    
    def _estimate_execution_time(self, issue_data: Dict) -> str:
        """実行時間を推定"""
        body = (issue_data['body'] or '').lower()
        title = issue_data['title'].lower()
        
        # 複雑度による推定
        if any(word in title + body for word in ['microservice', 'blockchain', 'ai', 'ml']):
            return "60-90 minutes"
        elif any(word in title + body for word in ['api', 'database', 'web']):
            return "30-60 minutes"
        elif any(word in title + body for word in ['simple', 'basic', 'シンプル']):
            return "15-30 minutes"
        else:
            return "30-45 minutes"
    
    def _post_approval_comment(self, repo_owner: str, repo_name: str, issue_number: int, approval_id: int):
        """承認待ちコメントを投稿"""
        comment = f"""🔍 **承認キューに追加されました**

こんにちは！システム生成リクエストを受信いたしました。

📋 **承認ID**: #{approval_id}
🔄 **ステータス**: 承認待ち
👀 **担当者**: GitHub Copilot

## 📝 次のステップ:
1. **要件確認**: プロンプト内容の精査
2. **優先度判定**: 他のリクエストとの優先順位決定
3. **承認・実行**: システム生成の開始
4. **結果通知**: 完成したシステムのお届け

⏰ **予想実行時間**: 承認後30-60分程度

承認され次第、自動でシステム生成を開始いたします。
進捗はこのISSUEで随時お知らせします。

---
**🤖 GitHub Copilot自動承認システム**
"""
        
        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
            response = requests.post(url, headers=self.headers, json={'body': comment})
            response.raise_for_status()
        except Exception as e:
            print(f"❌ コメント投稿エラー: {e}")
    
    def get_approval_queue(self, status: Optional[str] = None) -> List[Dict]:
        """承認キューを取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT id, github_issue_number, github_repo, issue_title, 
                       requester, approval_status, priority, estimated_time, created_at
                FROM approval_queue 
                WHERE approval_status = ?
                ORDER BY priority ASC, created_at ASC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT id, github_issue_number, github_repo, issue_title, 
                       requester, approval_status, priority, estimated_time, created_at
                FROM approval_queue 
                ORDER BY priority ASC, created_at ASC
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        queue = []
        for row in rows:
            queue.append({
                'id': row[0],
                'issue_number': row[1],
                'repo': row[2],
                'title': row[3],
                'requester': row[4],
                'status': row[5],
                'priority': row[6],
                'estimated_time': row[7],
                'created_at': row[8]
            })
        
        return queue
    
    def approve_request(self, approval_id: int, reviewer: str, notes: str = "") -> Dict:
        """リクエストを承認"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, approved_at = ?, 
                    reviewer_notes = ?, updated_at = ?
                WHERE id = ?
            ''', (
                ApprovalStatus.APPROVED.value,
                reviewer,
                datetime.now().isoformat(),
                notes,
                datetime.now().isoformat(),
                approval_id
            ))
            
            if cursor.rowcount == 0:
                conn.close()
                return {'success': False, 'error': 'Approval ID not found'}
            
            # 承認されたアイテムの情報を取得
            cursor.execute('''
                SELECT github_issue_number, github_repo, issue_title, issue_body
                FROM approval_queue WHERE id = ?
            ''', (approval_id,))
            
            item = cursor.fetchone()
            conn.commit()
            conn.close()
            
            if item:
                # GitHub ISSUEに承認通知
                repo_parts = item[1].split('/')
                self._post_approval_notification(repo_parts[0], repo_parts[1], item[0], approved=True)
                
                # 自動実行をキューに追加（実際の実行は別プロセス）
                return {
                    'success': True,
                    'status': 'approved',
                    'item': {
                        'issue_number': item[0],
                        'repo': item[1], 
                        'title': item[2],
                        'body': item[3]
                    }
                }
            
            return {'success': True, 'status': 'approved'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def reject_request(self, approval_id: int, reviewer: str, reason: str) -> Dict:
        """リクエストを拒否"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, approved_at = ?, 
                    reviewer_notes = ?, updated_at = ?
                WHERE id = ?
            ''', (
                ApprovalStatus.REJECTED.value,
                reviewer,
                datetime.now().isoformat(),
                reason,
                datetime.now().isoformat(),
                approval_id
            ))
            
            # 拒否されたアイテムの情報を取得
            cursor.execute('''
                SELECT github_issue_number, github_repo
                FROM approval_queue WHERE id = ?
            ''', (approval_id,))
            
            item = cursor.fetchone()
            conn.commit()
            conn.close()
            
            if item:
                # GitHub ISSUEに拒否通知
                repo_parts = item[1].split('/')
                self._post_rejection_notification(repo_parts[0], repo_parts[1], item[0], reason)
            
            return {'success': True, 'status': 'rejected'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _post_approval_notification(self, repo_owner: str, repo_name: str, issue_number: int, approved: bool):
        """承認・拒否通知を投稿"""
        if approved:
            comment = """✅ **承認完了 - システム生成開始！**

おめでとうございます！リクエストが承認されました。

🚀 **ステータス**: システム生成中
⏰ **開始時刻**: 今すぐ
🔧 **担当AI**: GitHub Copilot

GPT-ENGINEERでシステム生成を開始します。
完了次第、結果をこのISSUEでお知らせいたします。

---
**🤖 GitHub Copilot自動承認システム**
"""
        else:
            comment = """❌ **リクエスト拒否**

申し訳ございませんが、このリクエストは拒否されました。

詳細な理由については、承認者からの説明をご確認ください。
改善後、再度リクエストしていただけます。

---
**🤖 GitHub Copilot自動承認システム**
"""
        
        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
            response = requests.post(url, headers=self.headers, json={'body': comment})
            response.raise_for_status()
        except Exception as e:
            print(f"❌ 通知投稿エラー: {e}")
    
    def _post_rejection_notification(self, repo_owner: str, repo_name: str, issue_number: int, reason: str):
        """拒否通知を投稿"""
        comment = f"""❌ **リクエスト拒否**

申し訳ございませんが、このリクエストは拒否されました。

📝 **拒否理由:**
{reason}

🔄 **次のステップ:**
- 要件の見直し・詳細化
- 技術的制約の確認
- 改善後の再投稿

ご不明な点がございましたら、お気軽にお声がけください。

---
**🤖 GitHub Copilot自動承認システム**
"""
        
        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
            response = requests.post(url, headers=self.headers, json={'body': comment})
            response.raise_for_status()
        except Exception as e:
            print(f"❌ 拒否通知投稿エラー: {e}")


def create_approval_interface():
    """承認管理のGradioインターフェース"""
    import gradio as gr
    
    approval_system = None
    
    def initialize_system(github_token):
        global approval_system
        try:
            approval_system = HybridApprovalSystem(github_token)
            return "✅ 承認システム初期化完了"
        except Exception as e:
            return f"❌ 初期化エラー: {str(e)}"
    
    def import_issue(repo_owner, repo_name, issue_number):
        if not approval_system:
            return "❌ システムが初期化されていません"
        
        try:
            result = approval_system.import_issue_to_approval_queue(repo_owner, repo_name, int(issue_number))
            # Ensure we always return a string for Gradio components
            if isinstance(result, dict):
                if result.get('success'):
                    return f"✅ ISSUE #{issue_number} を承認キューに追加しました (ID: {result.get('approval_id', 'Unknown')})"
                else:
                    return f"❌ エラー: {result.get('error', '不明なエラー')}"
            else:
                return str(result)
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    def get_queue_display():
        if not approval_system:
            return []
        
        queue = approval_system.get_approval_queue()
        table_data = []
        
        for item in queue:
            priority_icon = "🔴" if item['priority'] <= 2 else "🟡" if item['priority'] <= 4 else "🟢"
            status_icon = {
                'pending_review': '⏳',
                'approved': '✅', 
                'rejected': '❌',
                'in_progress': '🚀',
                'completed': '🎉',
                'failed': '💥'
            }.get(item['status'], '❓')
            
            table_data.append([
                item['id'],
                f"{priority_icon} {item['priority']}",
                f"{status_icon} {item['status']}",
                item['title'][:50] + '...' if len(item['title']) > 50 else item['title'],
                item['requester'],
                item['estimated_time'],
                item['created_at'][:16]
            ])
        
        return table_data
    
    def approve_item(approval_id, reviewer, notes):
        if not approval_system:
            return "❌ システムが初期化されていません"
        
        try:
            result = approval_system.approve_request(int(approval_id), reviewer, notes)
            # Ensure we always return a string for Gradio components
            if isinstance(result, dict):
                if result.get('success'):
                    return f"✅ 承認ID {approval_id} を承認しました"
                else:
                    return f"❌ エラー: {result.get('error', '不明なエラー')}"
            else:
                return str(result)
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    def reject_item(approval_id, reviewer, reason):
        if not approval_system:
            return "❌ システムが初期化されていません"
        
        try:
            result = approval_system.reject_request(int(approval_id), reviewer, reason)
            # Ensure we always return a string for Gradio components
            if isinstance(result, dict):
                if result.get('success'):
                    return f"✅ 承認ID {approval_id} を拒否しました"
                else:
                    return f"❌ エラー: {result.get('error', '不明なエラー')}"
            else:
                return str(result)
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    with gr.Blocks(title="🔍 承認管理システム") as interface:
        gr.Markdown("# 🔍 承認管理システム")
        gr.Markdown("GitHub ISSUE → 承認 → 実行の管理")
        
        with gr.Row():
            github_token_input = gr.Textbox(label="GitHub Token", type="password")
            init_btn = gr.Button("初期化", variant="primary")
            init_result = gr.Textbox(label="初期化結果", interactive=False)
        
        with gr.Tabs():
            with gr.TabItem("📥 ISSUE取り込み"):
                with gr.Row():
                    repo_owner_input = gr.Textbox(label="リポジトリオーナー", placeholder="username")
                    repo_name_input = gr.Textbox(label="リポジトリ名", placeholder="repository")
                    issue_number_input = gr.Number(label="ISSUE番号", precision=0)
                    import_btn = gr.Button("取り込み", variant="primary")
                
                import_result = gr.Textbox(label="取り込み結果", interactive=False)
            
            with gr.TabItem("⏳ 承認キュー"):
                refresh_queue_btn = gr.Button("🔄 キュー更新")
                approval_queue = gr.Dataframe(
                    headers=["ID", "優先度", "ステータス", "タイトル", "依頼者", "予想時間", "作成日時"],
                    datatype=["number", "str", "str", "str", "str", "str", "str"],
                    value=[],
                    interactive=False,
                    height=400
                )
            
            with gr.TabItem("✅ 承認・拒否"):
                with gr.Row():
                    approval_id_input = gr.Number(label="承認ID", precision=0)
                    reviewer_input = gr.Textbox(label="承認者", placeholder="GitHub Copilot")
                
                with gr.Row():
                    notes_input = gr.Textbox(label="承認メモ", placeholder="承認理由・注意事項")
                    reason_input = gr.Textbox(label="拒否理由", placeholder="拒否する理由")
                
                with gr.Row():
                    approve_btn = gr.Button("✅ 承認", variant="primary")
                    reject_btn = gr.Button("❌ 拒否", variant="stop")
                
                action_result = gr.Textbox(label="操作結果", interactive=False)
        
        # イベントハンドラー
        init_btn.click(fn=initialize_system, inputs=github_token_input, outputs=init_result)
        import_btn.click(
            fn=import_issue, 
            inputs=[repo_owner_input, repo_name_input, issue_number_input],
            outputs=import_result
        )
        refresh_queue_btn.click(fn=get_queue_display, outputs=approval_queue)
        approve_btn.click(
            fn=approve_item,
            inputs=[approval_id_input, reviewer_input, notes_input],
            outputs=action_result
        )
        reject_btn.click(
            fn=reject_item,
            inputs=[approval_id_input, reviewer_input, reason_input],
            outputs=action_result
        )
        
        # 初期読み込み
        interface.load(fn=get_queue_display, outputs=approval_queue)
    
    return interface

# 承認管理インターフェース
approval_interface = create_approval_interface()
