"""
会話履歴自動記録システム
=======================

GitHub Copilotとの会話を自動的にSQLiteに保存するためのフックシステム

使用方法:
1. このモジュールをインポート
2. log_conversation()を呼び出すだけで自動保存
3. セッション管理も自動化
"""

import uuid
import datetime
import json
import os
import traceback
import sqlite3
import subprocess
from typing import Optional, Dict, List
from controllers.conversation_history import ConversationManager

class ConversationLogger:
    def __init__(self):
        """会話ログシステムの初期化"""
        self.conversation_manager = ConversationManager()
        self.current_session_id = self.generate_session_id()
        self.session_start_time = datetime.datetime.now()
        
        print(f"🎯 会話ログシステム開始 - セッションID: {self.current_session_id[:8]}")
    
    def generate_session_id(self) -> str:
        """新しいセッションIDを生成"""
        return str(uuid.uuid4())
    
    def start_new_session(self, session_name: str = None) -> str:
        """新しいセッションを開始"""
        self.current_session_id = self.generate_session_id()
        self.session_start_time = datetime.datetime.now()
        
        if session_name:
            # セッション名を更新
            try:
                conn = sqlite3.connect(self.conversation_manager.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE sessions 
                    SET session_name = ?
                    WHERE session_id = ?
                ''', (session_name, self.current_session_id))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ セッション名更新エラー: {e}")
        
        print(f"🆕 新しいセッション開始: {self.current_session_id[:8]}")
        return self.current_session_id
    
    def log_conversation(self,
                        user_message: str,
                        assistant_response: str,
                        context_info: str = "",
                        files_involved: List[str] = None,
                        tools_used: List[str] = None,
                        tags: List[str] = None,
                        project_name: str = "ContBK統合システム") -> Optional[int]:
        """
        会話を自動記録
        
        Args:
            user_message: ユーザーからのメッセージ
            assistant_response: アシスタントの応答
            context_info: コンテキスト情報
            files_involved: 関連ファイルのリスト
            tools_used: 使用ツールのリスト
            tags: タグのリスト
            project_name: プロジェクト名
        
        Returns:
            会話ID (保存に成功した場合)
        """
        try:
            # リストを文字列に変換
            files_str = ", ".join(files_involved) if files_involved else ""
            tools_str = ", ".join(tools_used) if tools_used else ""
            tags_str = ", ".join(tags) if tags else ""
            
            # 会話を保存
            conversation_id = self.conversation_manager.save_conversation(
                session_id=self.current_session_id,
                user_message=user_message,
                assistant_response=assistant_response,
                context_info=context_info,
                files_involved=files_str,
                tools_used=tools_str,
                tags=tags_str
            )
            
            print(f"✅ 会話を記録しました (ID: {conversation_id})")
            return conversation_id
            
        except Exception as e:
            print(f"❌ 会話記録エラー: {e}")
            print(traceback.format_exc())
            return None
    
    def log_tool_usage(self, tool_name: str, parameters: Dict, result: str):
        """ツール使用ログを記録"""
        tool_info = {
            "tool": tool_name,
            "parameters": parameters,
            "result": result[:500],  # 結果は500文字まで
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 直前の会話にツール情報を追加
        try:
            conn = sqlite3.connect(self.conversation_manager.db_path)
            cursor = conn.cursor()
            
            # 最新の会話を取得
            cursor.execute('''
                SELECT id, tools_used FROM conversations 
                WHERE session_id = ?
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (self.current_session_id,))
            
            row = cursor.fetchone()
            if row:
                conversation_id, existing_tools = row
                
                # 既存のツール情報に追加
                updated_tools = existing_tools + f", {tool_name}" if existing_tools else tool_name
                
                cursor.execute('''
                    UPDATE conversations 
                    SET tools_used = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (updated_tools, conversation_id))
                
                conn.commit()
            
            conn.close()
            print(f"🔧 ツール使用を記録: {tool_name}")
            
        except Exception as e:
            print(f"⚠️ ツール使用記録エラー: {e}")
    
    def get_session_summary(self) -> Dict:
        """現在のセッションの要約を取得"""
        try:
            conversations = self.conversation_manager.get_conversations(
                session_id=self.current_session_id
            )
            
            return {
                "session_id": self.current_session_id,
                "start_time": self.session_start_time.isoformat(),
                "conversation_count": len(conversations),
                "duration_minutes": (datetime.datetime.now() - self.session_start_time).total_seconds() / 60,
                "latest_conversation": conversations[0] if conversations else None
            }
        except Exception as e:
            print(f"⚠️ セッション要約取得エラー: {e}")
            return {}
    
    def export_session(self, session_id: str = None) -> str:
        """セッションをJSON形式でエクスポート"""
        target_session = session_id or self.current_session_id
        
        try:
            conversations = self.conversation_manager.get_conversations(
                session_id=target_session
            )
            
            export_data = {
                "session_id": target_session,
                "export_time": datetime.datetime.now().isoformat(),
                "conversation_count": len(conversations),
                "conversations": conversations
            }
            
            filename = f"session_export_{target_session[:8]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"📥 セッションエクスポート完了: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ セッションエクスポートエラー: {e}")
            return ""
    
    def create_github_issue(self, 
                           title: str = None,
                           session_id: str = None,
                           labels: List[str] = None,
                           assignee: str = None) -> bool:
        """
        GitHub Issueを作成
        
        Args:
            title: Issue のタイトル（未指定の場合は自動生成）
            session_id: 対象セッションID（未指定の場合は現在のセッション）
            labels: 付与するラベル
            assignee: アサイニー
        
        Returns:
            作成成功の可否
        """
        try:
            target_session = session_id or self.current_session_id
            
            # 会話履歴を取得
            conversations = self.conversation_manager.get_conversations(
                session_id=target_session
            )
            
            if not conversations:
                print("⚠️ 会話履歴が見つかりません")
                return False
            
            # タイトルを自動生成（未指定の場合）
            if not title:
                first_conversation = conversations[-1]  # 最初の会話
                title = f"開発セッション: {first_conversation.get('user_message', '')[:50]}..."
            
            # Issue本文を生成
            issue_body = self._generate_issue_body(conversations, target_session)
            
            # GitHub CLI を使用してIssue作成
            cmd = [
                'gh', 'issue', 'create',
                '--title', title,
                '--body', issue_body
            ]
            
            # ラベルを追加
            if labels:
                for label in labels:
                    cmd.extend(['--label', label])
            
            # アサイニーを追加
            if assignee:
                cmd.extend(['--assignee', assignee])
            
            # コマンド実行
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='/workspaces/fastapi_django_main_live')
            
            if result.returncode == 0:
                issue_url = result.stdout.strip()
                print(f"✅ GitHub Issue作成成功: {issue_url}")
                
                # セッションにIssue URLを記録
                self._update_session_issue_url(target_session, issue_url)
                
                return True
            else:
                print(f"❌ GitHub Issue作成失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ GitHub Issue作成エラー: {e}")
            print(traceback.format_exc())
            return False
    
    def _generate_issue_body(self, conversations: List[Dict], session_id: str) -> str:
        """Issue本文を生成"""
        
        # セッション情報
        session_info = self.get_session_summary()
        
        body_parts = [
            "# 開発セッション記録",
            "",
            "## 📊 セッション情報",
            f"- **セッションID**: `{session_id[:8]}`",
            f"- **開始時刻**: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **会話数**: {len(conversations)}",
            f"- **継続時間**: {session_info.get('duration_minutes', 0):.1f}分",
            "",
            "## 🗣️ 会話履歴",
            ""
        ]
        
        # 会話履歴を追加（最新10件まで）
        recent_conversations = conversations[:10] if len(conversations) > 10 else conversations
        
        for i, conv in enumerate(reversed(recent_conversations), 1):
            body_parts.extend([
                f"### {i}. {conv.get('timestamp', '')}",
                "",
                "**👤 User:**",
                "```",
                conv.get('user_message', ''),
                "```",
                "",
                "**🤖 Assistant:**",
                "```",
                conv.get('assistant_response', '')[:1000] + ('...' if len(conv.get('assistant_response', '')) > 1000 else ''),
                "```",
                ""
            ])
            
            # コンテキスト情報があれば追加
            if conv.get('context_info'):
                body_parts.extend([
                    "**📝 Context:**",
                    "```",
                    conv.get('context_info', ''),
                    "```",
                    ""
                ])
            
            # 関連ファイルがあれば追加
            if conv.get('files_involved'):
                body_parts.extend([
                    "**📁 Files:**",
                    f"`{conv.get('files_involved', '')}`",
                    ""
                ])
            
            # 使用ツールがあれば追加
            if conv.get('tools_used'):
                body_parts.extend([
                    "**🔧 Tools:**",
                    f"`{conv.get('tools_used', '')}`",
                    ""
                ])
            
            body_parts.append("---")
            body_parts.append("")
        
        # 要約とタグ
        all_files = set()
        all_tools = set()
        all_tags = set()
        
        for conv in conversations:
            if conv.get('files_involved'):
                all_files.update(conv.get('files_involved', '').split(', '))
            if conv.get('tools_used'):
                all_tools.update(conv.get('tools_used', '').split(', '))
            if conv.get('tags'):
                all_tags.update(conv.get('tags', '').split(', '))
        
        body_parts.extend([
            "## 📋 セッション要約",
            "",
            "### 関連ファイル",
            "",
        ])
        
        for file in sorted(all_files):
            if file.strip():
                body_parts.append(f"- `{file.strip()}`")
        
        body_parts.extend([
            "",
            "### 使用ツール",
            "",
        ])
        
        for tool in sorted(all_tools):
            if tool.strip():
                body_parts.append(f"- `{tool.strip()}`")
        
        if all_tags:
            body_parts.extend([
                "",
                "### タグ",
                "",
            ])
            
            for tag in sorted(all_tags):
                if tag.strip():
                    body_parts.append(f"- `{tag.strip()}`")
        
        body_parts.extend([
            "",
            "---",
            f"*自動生成: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        ])
        
        return "\n".join(body_parts)
    
    def _update_session_issue_url(self, session_id: str, issue_url: str):
        """セッションにIssue URLを記録"""
        try:
            conn = sqlite3.connect(self.conversation_manager.db_path)
            cursor = conn.cursor()
            
            # sessions テーブルにissue_url カラムを追加（存在しない場合）
            cursor.execute('''
                ALTER TABLE sessions ADD COLUMN issue_url TEXT
            ''')
            
        except sqlite3.OperationalError:
            # カラムが既に存在する場合
            pass
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO sessions (session_id, issue_url)
                VALUES (?, ?)
            ''', (session_id, issue_url))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Issue URL記録エラー: {e}")
    
    def create_issue_for_current_session(self, 
                                       title: str = None,
                                       labels: List[str] = None) -> bool:
        """現在のセッションのGitHub Issueを作成"""
        default_labels = []  # デフォルトラベルを空に
        if labels:
            default_labels.extend(labels)
        
        return self.create_github_issue(
            title=title,
            session_id=self.current_session_id,
            labels=default_labels
        )
    
    def create_quick_issue(title: str, 
                     user_msg: str, 
                     assistant_msg: str,
                     labels: List[str] = None):
        """
        会話内容から直接GitHub Issueを作成
        
        使用例:
        create_quick_issue(
            title="ContBK統合システム開発",
            user_msg="このやりとりをGit Issueへ登録したい",
            assistant_msg="GitHub Issue作成機能を実装しました",
            labels=["development", "enhancement"]
        )
        """
        # 一時的に会話を記録
        conversation_logger.log_conversation(
            user_message=user_msg,
            assistant_response=assistant_msg,
            context_info="GitHub Issue直接作成",
            tags=["quick-issue"] + (labels or [])
        )
        
        # すぐにIssue作成
        return conversation_logger.create_issue_for_current_session(
            title=title,
            labels=labels or ["development", "conversation-log"]
        )

# グローバルログインスタンス
conversation_logger = ConversationLogger()

def log_this_conversation(user_msg: str, assistant_msg: str, 
                         context: str = "", files: List[str] = None, 
                         tools: List[str] = None, tags: List[str] = None):
    """
    簡単な会話ログ記録関数
    
    使用例:
    log_this_conversation(
        user_msg="ContBK統合システムについて教えて",
        assistant_msg="ContBK統合システムは...",
        files=["controllers/contbk_example.py"],
        tools=["create_file", "insert_edit_into_file"],
        tags=["contbk", "gradio"]
    )
    """
    return conversation_logger.log_conversation(
        user_message=user_msg,
        assistant_response=assistant_msg,
        context_info=context,
        files_involved=files,
        tools_used=tools,
        tags=tags
    )

def start_new_conversation_session(session_name: str = None):
    """新しい会話セッションを開始"""
    return conversation_logger.start_new_session(session_name)

def create_quick_issue(title: str, 
                     user_msg: str, 
                     assistant_msg: str,
                     labels: List[str] = None):
    """
    会話内容から直接GitHub Issueを作成
    
    使用例:
    create_quick_issue(
        title="ContBK統合システム開発",
        user_msg="このやりとりをGit Issueへ登録したい",
        assistant_msg="GitHub Issue作成機能を実装しました",
        labels=["development", "enhancement"]
    )
    """
    # 一時的に会話を記録
    conversation_logger.log_conversation(
        user_message=user_msg,
        assistant_response=assistant_msg,
        context_info="GitHub Issue直接作成",
        tags=["quick-issue"] + (labels or [])
    )
    
    # すぐにIssue作成
    return conversation_logger.create_issue_for_current_session(
        title=title,
        labels=labels or []  # デフォルトラベルを空に
    )

def create_github_issue_for_session(title: str = None, 
                                   labels: List[str] = None,
                                   session_id: str = None):
    """
    現在のセッションまたは指定セッションのGitHub Issueを作成
    
    使用例:
    create_github_issue_for_session(
        title="ContBK統合システム開発セッション",
        labels=["enhancement", "contbk"]
    )
    """
    return conversation_logger.create_github_issue(
        title=title,
        session_id=session_id,
        labels=labels or ["development", "conversation-log"]
    )

def create_issue_now(title: str = "開発セッション記録"):
    """ワンクリックでGitHub Issue作成"""
    return conversation_logger.create_issue_for_current_session(title=title)

def get_current_session_info():
    """現在のセッション情報を取得"""
    return conversation_logger.get_session_summary()

# 自動ログ記録のデコレーター
def auto_log_conversation(tags: List[str] = None):
    """
    関数の実行を自動的にログに記録するデコレーター
    
    使用例:
    @auto_log_conversation(tags=["gradio", "interface"])
    def create_interface():
        # 関数の処理
        pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            
            try:
                result = func(*args, **kwargs)
                
                # 成功した場合のログ
                conversation_logger.log_conversation(
                    user_message=f"関数実行: {func.__name__}",
                    assistant_response=f"関数 {func.__name__} が正常に実行されました",
                    context_info=f"実行時間: {(datetime.datetime.now() - start_time).total_seconds():.2f}秒",
                    tools_used=[func.__name__],
                    tags=tags or ["自動実行"]
                )
                
                return result
                
            except Exception as e:
                # エラーの場合のログ
                conversation_logger.log_conversation(
                    user_message=f"関数実行エラー: {func.__name__}",
                    assistant_response=f"エラーが発生しました: {str(e)}",
                    context_info=f"実行時間: {(datetime.datetime.now() - start_time).total_seconds():.2f}秒",
                    tools_used=[func.__name__],
                    tags=(tags or []) + ["エラー"]
                )
                raise
                
        return wrapper
    return decorator

if __name__ == "__main__":
    # テスト実行
    print("🧪 会話ログシステムテスト")
    
    # サンプル会話を記録
    log_this_conversation(
        user_msg="GitHub Issue作成機能のテストです",
        assistant_msg="GitHub Issue作成機能が正常に動作しています！",
        context="GitHub Issue機能追加",
        files=["controllers/conversation_logger.py"],
        tools=["create_github_issue", "gh"],
        tags=["github", "issue", "automation"]
    )
    
    # セッション情報表示
    session_info = get_current_session_info()
    print(f"📊 セッション情報: {session_info}")
    
    # GitHub Issue作成テスト（コメントアウト）
    # create_issue_now("テスト用GitHub Issue")
    
    print("✅ テスト完了")
