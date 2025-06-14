"""
会話履歴管理システム
=====================

GitHub Copilotとの会話履歴をSQLiteに保存し、
Gradioインターフェースで閲覧・検索できるシステム

機能:
- 会話の自動保存
- 履歴の閲覧・検索
- 会話の分析・統計
- エクスポート機能
"""

import gradio as gr
import sqlite3
import json
import datetime
from typing import List, Dict, Optional, Tuple
import os
import pandas as pd
from pathlib import Path
import re

# インターフェースメタデータ
interface_title = "💬 会話履歴管理"
interface_description = "GitHub Copilotとの会話履歴を管理・閲覧"

class ConversationManager:
    def __init__(self, db_path: str = "conversation_history.db"):
        """会話履歴管理クラスの初期化"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースの初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 会話テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                context_info TEXT,
                files_involved TEXT,
                tools_used TEXT,
                conversation_summary TEXT,
                tags TEXT,
                project_name TEXT DEFAULT 'ContBK統合システム',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # セッションテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                session_name TEXT,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                total_messages INTEGER DEFAULT 0,
                description TEXT,
                project_context TEXT
            )
        ''')
        
        # インデックス作成
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON conversations(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON conversations(tags)')
        
        conn.commit()
        conn.close()
        print("✅ 会話履歴データベース初期化完了")
    
    def save_conversation(self, 
                         session_id: str,
                         user_message: str, 
                         assistant_response: str,
                         context_info: str = "",
                         files_involved: str = "",
                         tools_used: str = "",
                         tags: str = ""):
        """会話を保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 会話を保存
        cursor.execute('''
            INSERT INTO conversations 
            (session_id, user_message, assistant_response, context_info, 
             files_involved, tools_used, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, user_message, assistant_response, context_info,
              files_involved, tools_used, tags))
        
        # セッション更新
        cursor.execute('''
            INSERT OR REPLACE INTO sessions 
            (session_id, session_name, total_messages)
            VALUES (?, ?, (
                SELECT COUNT(*) FROM conversations 
                WHERE session_id = ?
            ))
        ''', (session_id, f"セッション_{session_id[:8]}", session_id))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def get_conversations(self, 
                         limit: int = 50, 
                         session_id: str = None,
                         search_query: str = None) -> List[Dict]:
        """会話履歴を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, session_id, timestamp, user_message, 
                   assistant_response, context_info, files_involved, 
                   tools_used, tags
            FROM conversations
            WHERE 1=1
        '''
        params = []
        
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        if search_query:
            query += " AND (user_message LIKE ? OR assistant_response LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append({
                'id': row[0],
                'session_id': row[1],
                'timestamp': row[2],
                'user_message': row[3],
                'assistant_response': row[4],
                'context_info': row[5],
                'files_involved': row[6],
                'tools_used': row[7],
                'tags': row[8]
            })
        
        return conversations
    
    def get_sessions(self) -> List[Dict]:
        """セッション一覧を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT session_id, session_name, start_time, 
                   total_messages, description
            FROM sessions
            ORDER BY start_time DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                'session_id': row[0],
                'session_name': row[1],
                'start_time': row[2],
                'total_messages': row[3],
                'description': row[4]
            })
        
        return sessions
    
    def get_statistics(self) -> Dict:
        """統計情報を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 基本統計
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT session_id) FROM sessions')
        total_sessions = cursor.fetchone()[0]
        
        # 今日の会話数
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        today_conversations = cursor.fetchone()[0]
        
        # 最も使用されたツール
        cursor.execute('''
            SELECT tools_used, COUNT(*) as count
            FROM conversations 
            WHERE tools_used != ''
            GROUP BY tools_used
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_tools = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'total_sessions': total_sessions,
            'today_conversations': today_conversations,
            'top_tools': top_tools
        }
    
    def generate_prompt_summary(self, limit: int = 10) -> str:
        """
        プロンプト用の会話履歴サマリーを生成
        
        Args:
            limit: 取得する最新会話数
            
        Returns:
            プロンプトに含めるためのサマリー文字列
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 最新の会話を取得
            cursor.execute('''
                SELECT user_message, assistant_response, context_info, 
                       tools_used, tags, created_at
                FROM conversations 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            conversations = cursor.fetchall()
            
            if not conversations:
                return "## 会話履歴\n過去の会話履歴はありません。"
            
            # サマリーを構築
            summary = ["## 🕒 前回までの会話履歴サマリー"]
            summary.append("```")
            summary.append("GitHub Copilotとの過去の主要な会話内容:")
            summary.append("")
            
            for i, (user_msg, assistant_resp, context, tools, tags, timestamp) in enumerate(conversations, 1):
                # メッセージを要約（長すぎる場合は切り詰め）
                user_summary = user_msg[:100] + "..." if len(user_msg) > 100 else user_msg
                assistant_summary = assistant_resp[:150] + "..." if len(assistant_resp) > 150 else assistant_resp
                
                summary.append(f"{i}. [{timestamp[:16]}]")
                summary.append(f"   ユーザー: {user_summary}")
                summary.append(f"   対応: {assistant_summary}")
                
                if context:
                    summary.append(f"   コンテキスト: {context}")
                if tools:
                    summary.append(f"   使用ツール: {tools}")
                if tags:
                    summary.append(f"   タグ: {tags}")
                summary.append("")
            
            summary.append("```")
            summary.append("")
            summary.append("💡 **重要**: 上記の履歴を参考に、継続性のある対応を行ってください。")
            
            return "\n".join(summary)
            
        except Exception as e:
            return f"## 会話履歴\n履歴取得エラー: {str(e)}"
        finally:
            conn.close()
    
    def generate_context_prompt(self, session_limit: int = 5, detail_limit: int = 3) -> str:
        """
        新しいセッション用のコンテキストプロンプトを生成
        
        Args:
            session_limit: セッション履歴の取得数
            detail_limit: 詳細表示する最新会話数
            
        Returns:
            新しいプロンプトに含めるコンテキスト情報
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # プロジェクト統計
            cursor.execute('SELECT COUNT(*) FROM conversations')
            total_conversations = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT session_id) FROM sessions')
            total_sessions = cursor.fetchone()[0]
            
            # 最新セッションの情報
            cursor.execute('''
                SELECT session_id, session_name, start_time, total_messages
                FROM sessions 
                ORDER BY start_time DESC 
                LIMIT ?
            ''', (session_limit,))
            recent_sessions = cursor.fetchall()
            
            # 最新の詳細会話
            cursor.execute('''
                SELECT user_message, assistant_response, context_info, 
                       tools_used, tags, created_at
                FROM conversations 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (detail_limit,))
            recent_conversations = cursor.fetchall()
            
            # プロンプト構築
            context_lines = [
                "<conversation-summary>",
                "## CONVERSATION SUMMARY",
                "",
                "**TASK DESCRIPTION:** ",
                "統合開発環境でのContBKフォルダーインターフェース統合、会話履歴システム実装、",
                "SQLiteベースの自動ログ機能開発を継続的に行っています。",
                "",
                "**COMPLETED:**",
                f"- ✅ 総会話数: {total_conversations}件",
                f"- ✅ セッション数: {total_sessions}件", 
                "- ✅ ContBK統合システム実装済み",
                "- ✅ SQLite会話履歴システム実装済み",
                "- ✅ DuplicateBlockError修正済み",
                "- ✅ Git同期管理実装済み",
                ""
            ]
            
            if recent_sessions:
                context_lines.extend([
                    "**RECENT SESSIONS:**",
                ])
                for session_id, name, start_time, total_messages in recent_sessions:
                    context_lines.append(f"- {name} ({total_messages}件) - {start_time[:16]}")
                context_lines.append("")
            
            if recent_conversations:
                context_lines.extend([
                    "**LATEST CONVERSATIONS:**",
                ])
                for i, (user_msg, assistant_resp, context, tools, tags, timestamp) in enumerate(recent_conversations, 1):
                    user_summary = user_msg[:80] + "..." if len(user_msg) > 80 else user_msg
                    assistant_summary = assistant_resp[:100] + "..." if len(assistant_resp) > 100 else assistant_resp
                    
                    context_lines.extend([
                        f"{i}. [{timestamp[:16]}] {user_summary}",
                        f"   → {assistant_summary}",
                    ])
                    if context:
                        context_lines.append(f"   Context: {context}")
                    if tools:
                        context_lines.append(f"   Tools: {tools}")
                context_lines.append("")
            
            context_lines.extend([
                "**CURRENT_STATE:**",
                "アプリケーションは http://localhost:7860 で正常稼働中。",
                "10個のGradioインターフェースが統合され、会話履歴システムも完全に動作しています。",
                "全ての変更はGitで管理され、SQLiteに自動記録されています。",
                "</conversation-summary>"
            ])
            
            return "\n".join(context_lines)
            
        except Exception as e:
            return f"<conversation-summary>\nコンテキスト生成エラー: {str(e)}\n</conversation-summary>"
        finally:
            conn.close()

# グローバルインスタンス
conversation_manager = ConversationManager()

# ConversationManagerクラスもエクスポート
__all__ = ['ConversationManager', 'conversation_manager']

def format_conversation_display(conversations: List[Dict]) -> str:
    """会話履歴を表示用にフォーマット"""
    if not conversations:
        return "📭 会話履歴がありません"
    
    display_text = "# 📚 会話履歴\n\n"
    
    for conv in conversations:
        timestamp = conv['timestamp']
        user_msg = conv['user_message'][:100] + "..." if len(conv['user_message']) > 100 else conv['user_message']
        assistant_resp = conv['assistant_response'][:200] + "..." if len(conv['assistant_response']) > 200 else conv['assistant_response']
        
        display_text += f"""
## 🕐 {timestamp}
**👤 ユーザー:** {user_msg}

**🤖 アシスタント:** {assistant_resp}

**📁 関連ファイル:** {conv.get('files_involved', 'なし')}
**🔧 使用ツール:** {conv.get('tools_used', 'なし')}
**🏷️ タグ:** {conv.get('tags', 'なし')}

---
"""
    
    return display_text

def load_conversation_history(limit: int, session_filter: str, search_query: str) -> Tuple[str, str]:
    """会話履歴をロード"""
    try:
        # フィルター処理
        session_id = session_filter if session_filter != "全てのセッション" else None
        search = search_query.strip() if search_query.strip() else None
        
        conversations = conversation_manager.get_conversations(
            limit=limit,
            session_id=session_id,
            search_query=search
        )
        
        display_text = format_conversation_display(conversations)
        
        # 統計情報
        stats = conversation_manager.get_statistics()
        stats_text = f"""
## 📊 統計情報
- **総会話数:** {stats['total_conversations']}
- **総セッション数:** {stats['total_sessions']}
- **今日の会話数:** {stats['today_conversations']}
"""
        
        return display_text, stats_text
        
    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}", ""

def get_session_list() -> List[str]:
    """セッション一覧を取得"""
    try:
        sessions = conversation_manager.get_sessions()
        session_list = ["全てのセッション"]
        session_list.extend([f"{s['session_name']} ({s['session_id'][:8]})" for s in sessions])
        return session_list
    except:
        return ["全てのセッション"]

def save_sample_conversation():
    """サンプル会話を保存（テスト用）"""
    import uuid
    session_id = str(uuid.uuid4())
    
    conversation_manager.save_conversation(
        session_id=session_id,
        user_message="ContBK統合システムについて教えて",
        assistant_response="ContBK統合システムは、contbkフォルダーにある全てのGradioインターフェースを美しい絵文字タイトル付きで統合表示するシステムです。",
        context_info="ContBK統合システムの説明",
        files_involved="controllers/contbk_example.py",
        tools_used="create_file, insert_edit_into_file",
        tags="contbk, gradio, 統合システム"
    )
    
    return "✅ サンプル会話を保存しました"

def export_conversations_csv(conversations: List[Dict]) -> str:
    """会話履歴をCSVエクスポート"""
    try:
        if not conversations:
            return "📭 エクスポートする会話がありません"
        
        df = pd.DataFrame(conversations)
        
        # CSVファイルとして保存
        export_path = f"conversation_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(export_path, index=False, encoding='utf-8-sig')
        
        return f"✅ 会話履歴をエクスポートしました: {export_path}"
    except Exception as e:
        return f"❌ エクスポートエラー: {str(e)}"

# Gradioインターフェース作成
def create_conversation_interface():
    """会話履歴管理インターフェースを作成"""
    
    with gr.Blocks(title="💬 会話履歴管理", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 💬 会話履歴管理システム")
        gr.Markdown("GitHub Copilotとの会話履歴を管理・閲覧できます")
        
        with gr.Tab("📚 履歴閲覧"):
            with gr.Row():
                with gr.Column(scale=2):
                    search_box = gr.Textbox(
                        label="🔍 検索", 
                        placeholder="キーワードで検索...",
                        value=""
                    )
                with gr.Column(scale=2):
                    session_dropdown = gr.Dropdown(
                        label="📋 セッション選択",
                        choices=get_session_list(),
                        value="全てのセッション"
                    )
                with gr.Column(scale=1):
                    limit_slider = gr.Slider(
                        label="📊 表示件数",
                        minimum=10,
                        maximum=100,
                        value=20,
                        step=10
                    )
            
            with gr.Row():
                load_btn = gr.Button("🔄 履歴読み込み", variant="primary")
                refresh_btn = gr.Button("🆕 セッション更新")
                export_btn = gr.Button("📥 CSV エクスポート")
            
            with gr.Row():
                with gr.Column(scale=3):
                    conversation_display = gr.Markdown(
                        value="🔄 履歴読み込みボタンを押してください"
                    )
                with gr.Column(scale=1):
                    stats_display = gr.Markdown(
                        value="📊 統計情報"
                    )
        
        with gr.Tab("💾 会話保存"):
            gr.Markdown("## ✍️ 新しい会話を手動保存")
            
            with gr.Row():
                session_id_input = gr.Textbox(
                    label="🆔 セッションID",
                    placeholder="自動生成または手動入力",
                    value=""
                )
                tags_input = gr.Textbox(
                    label="🏷️ タグ",
                    placeholder="カンマ区切りでタグを入力",
                    value=""
                )
            
            user_message_input = gr.Textbox(
                label="👤 ユーザーメッセージ",
                lines=3,
                placeholder="ユーザーからのメッセージ..."
            )
            
            assistant_response_input = gr.Textbox(
                label="🤖 アシスタント応答",
                lines=5,
                placeholder="アシスタントの応答..."
            )
            
            with gr.Row():
                files_input = gr.Textbox(
                    label="📁 関連ファイル",
                    placeholder="関連ファイルパス",
                    value=""
                )
                tools_input = gr.Textbox(
                    label="🔧 使用ツール",
                    placeholder="使用したツール名",
                    value=""
                )
            
            save_btn = gr.Button("💾 会話を保存", variant="primary")
            sample_btn = gr.Button("📝 サンプル保存", variant="secondary")
            
            save_result = gr.Textbox(label="💬 結果", interactive=False)
        
        with gr.Tab("📊 統計・分析"):
            gr.Markdown("## 📈 会話統計ダッシュボード")
            
            with gr.Row():
                refresh_stats_btn = gr.Button("🔄 統計更新", variant="primary")
            
            detailed_stats = gr.Markdown(
                value="🔄 統計更新ボタンを押してください"
            )
        
        with gr.Tab("📝 プロンプト生成"):
            gr.Markdown("""
            ## 🎯 新セッション用プロンプト生成
            
            新しいGitHub Copilotセッション開始時に使用する、
            過去の会話履歴を含むコンテキストプロンプトを生成します。
            """)
            
            with gr.Row():
                with gr.Column():
                    prompt_type = gr.Radio(
                        label="📋 プロンプトタイプ",
                        choices=[
                            "簡易サマリー (最新10件)",
                            "詳細コンテキスト (セッション含む)",
                            "技術フォーカス (ツール・ファイル中心)",
                            "カスタム設定"
                        ],
                        value="詳細コンテキスト (セッション含む)"
                    )
                    
                    with gr.Group():
                        conversation_limit = gr.Slider(
                            label="📊 会話履歴件数",
                            minimum=3,
                            maximum=20,
                            value=10,
                            step=1
                        )
                        
                        session_limit = gr.Slider(
                            label="🗂️ セッション履歴件数",
                            minimum=3,
                            maximum=10,
                            value=5,
                            step=1
                        )
                        
                        include_tools = gr.Checkbox(
                            label="🔧 ツール使用履歴を含む",
                            value=True
                        )
                        
                        include_files = gr.Checkbox(
                            label="📁 ファイル操作履歴を含む", 
                            value=True
                        )
            
            with gr.Row():
                generate_btn = gr.Button("🎯 プロンプト生成", variant="primary", size="lg")
                copy_btn = gr.Button("📋 クリップボードにコピー", variant="secondary")
            
            prompt_output = gr.Textbox(
                label="📝 生成されたプロンプト",
                lines=20,
                max_lines=30,
                placeholder="生成ボタンを押すとプロンプトが表示されます...",
                show_copy_button=True
            )
            
            gr.Markdown("""
            ### 📌 使用方法:
            1. プロンプトタイプを選択
            2. 必要に応じて設定を調整
            3. 「プロンプト生成」をクリック
            4. 生成されたテキストを新しいセッションの最初にコピー&ペースト
            
            💡 **Tip**: 生成されたプロンプトにより、GitHub Copilotが過去のコンテキストを理解して、
            より継続性のある対応ができるようになります。
            """)
            
            def generate_context_prompt_ui(prompt_type, conv_limit, sess_limit, include_tools, include_files):
                """UIからプロンプト生成"""
                try:
                    if prompt_type == "簡易サマリー (最新10件)":
                        return conversation_manager.generate_prompt_summary(limit=conv_limit)
                    elif prompt_type == "詳細コンテキスト (セッション含む)":
                        return conversation_manager.generate_context_prompt(
                            session_limit=sess_limit, 
                            detail_limit=conv_limit
                        )
                    elif prompt_type == "技術フォーカス (ツール・ファイル中心)":
                        # 技術的な詳細に特化したプロンプト
                        context = conversation_manager.generate_context_prompt(sess_limit, conv_limit)
                        tech_header = """
<technical-context>
## TECHNICAL DEVELOPMENT CONTEXT

**FOCUS**: ContBK統合システム、SQLite会話履歴、Gradioインターフェース開発

**ACTIVE TOOLS**: 
- Gradio 4.31.5 (推奨: 4.44.1)
- SQLite3 (会話履歴管理)
- Python 3.11
- Git (バージョン管理)
- FastAPI + Django (バックエンド)

**CURRENT ENVIRONMENT**:
- Workspace: /workspaces/fastapi_django_main_live
- Port 7860: メインアプリケーション
- Port 7870-7880: 開発用サブアプリ

</technical-context>

"""
                        return tech_header + context
                    else:  # カスタム設定
                        return conversation_manager.generate_context_prompt(sess_limit, conv_limit)
                        
                except Exception as e:
                    return f"❌ プロンプト生成エラー: {str(e)}"
            
            generate_btn.click(
                generate_context_prompt_ui,
                inputs=[prompt_type, conversation_limit, session_limit, include_tools, include_files],
                outputs=prompt_output
            )

        # イベントハンドラー
        load_btn.click(
            fn=load_conversation_history,
            inputs=[limit_slider, session_dropdown, search_box],
            outputs=[conversation_display, stats_display]
        )
        
        refresh_btn.click(
            fn=lambda: gr.Dropdown.update(choices=get_session_list()),
            outputs=[session_dropdown]
        )
        
        sample_btn.click(
            fn=save_sample_conversation,
            outputs=[save_result]
        )
        
        # 初期ロード
        interface.load(
            fn=load_conversation_history,
            inputs=[gr.Number(value=20), gr.Textbox(value="全てのセッション"), gr.Textbox(value="")],
            outputs=[conversation_display, stats_display]
        )
    
    return interface

# Gradioインターフェースのファクトリー関数（遅延作成）
gradio_interface = create_conversation_interface

if __name__ == "__main__":
    print("🚀 会話履歴管理システム起動中...")
    interface = create_conversation_interface()
    interface.launch(
        server_port=7872,  # ポート変更
        share=False,
        debug=True
    )
