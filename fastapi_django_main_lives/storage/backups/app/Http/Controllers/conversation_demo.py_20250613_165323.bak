"""
会話履歴システム - 統合デモ
==========================

GitHub Copilotとの会話を自動記録し、
履歴を美しく表示するデモシステム

このファイルは:
1. 会話履歴の自動記録デモ
2. リアルタイム会話ログ機能
3. 履歴検索・エクスポート機能
を提供します
"""

import gradio as gr
import datetime
import uuid
from typing import List, Tuple
import json

# 会話ログシステムをインポート
from controllers.conversation_logger import (
    conversation_logger, 
    log_this_conversation,
    start_new_conversation_session,
    get_current_session_info
)
from controllers.conversation_history import conversation_manager

# インターフェースメタデータ
interface_title = "🎯 会話履歴統合デモ"
interface_description = "GitHub Copilotとの会話履歴を自動記録・管理するデモシステム"

def simulate_conversation_logging(user_input: str, context: str = "", tags: str = "") -> Tuple[str, str, str]:
    """
    会話ログのシミュレーション
    実際のCopilot会話を模擬して記録
    """
    if not user_input.strip():
        return "❓ ユーザー入力を入力してください", "", ""
    
    # シミュレートされたアシスタント応答を生成
    assistant_responses = {
        "contbk": "ContBK統合システムは、contbkフォルダーにある全てのGradioインターフェースを美しい絵文字タイトル付きで統合表示するシステムです。🎯",
        "履歴": "会話履歴システムにより、GitHub Copilotとの全ての会話がSQLiteデータベースに自動保存され、検索・分析が可能になります。💬",
        "gradio": "Gradioを使用することで、PythonコードをWebインターフェースとして簡単に公開できます。🌐",
        "デフォルト": f"「{user_input}」について説明いたします。この機能により、より効率的な開発が可能になります。✨"
    }
    
    # キーワードベースでレスポンス選択
    assistant_response = assistant_responses["デフォルト"]
    for keyword, response in assistant_responses.items():
        if keyword in user_input.lower():
            assistant_response = response
            break
    
    # タグ処理
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    tag_list.append("デモ")
    
    # 使用ツールを推定
    tools_used = []
    if "ファイル" in user_input or "作成" in user_input:
        tools_used.append("create_file")
    if "編集" in user_input or "修正" in user_input:
        tools_used.append("edit_file")
    if "検索" in user_input:
        tools_used.append("search")
    
    # 会話をログに記録
    conversation_id = log_this_conversation(
        user_msg=user_input,
        assistant_msg=assistant_response,
        context=context,
        files=["controllers/conversation_demo.py"],
        tools=tools_used,
        tags=tag_list
    )
    
    # 結果表示
    log_result = f"✅ 会話を記録しました (ID: {conversation_id})"
    session_info = get_current_session_info()
    session_display = f"""
## 🎯 現在のセッション情報
- **セッションID:** {session_info.get('session_id', 'N/A')[:8]}...
- **会話数:** {session_info.get('conversation_count', 0)}
- **経過時間:** {session_info.get('duration_minutes', 0):.1f}分
"""
    
    return assistant_response, log_result, session_display

def load_recent_conversations(limit: int = 10) -> str:
    """最近の会話履歴を表示"""
    try:
        conversations = conversation_manager.get_conversations(limit=limit)
        
        if not conversations:
            return "📭 まだ会話履歴がありません。上記で会話をシミュレートしてください。"
        
        display_text = "# 📚 最近の会話履歴\n\n"
        
        for i, conv in enumerate(conversations, 1):
            timestamp = conv['timestamp']
            user_msg = conv['user_message'][:80] + "..." if len(conv['user_message']) > 80 else conv['user_message']
            assistant_resp = conv['assistant_response'][:120] + "..." if len(conv['assistant_response']) > 120 else conv['assistant_response']
            
            display_text += f"""
### 🔹 会話 {i} - {timestamp}
**👤 ユーザー:** {user_msg}
**🤖 アシスタント:** {assistant_resp}
**🏷️ タグ:** {conv.get('tags', 'なし')}

---
"""
        
        return display_text
        
    except Exception as e:
        return f"❌ 履歴読み込みエラー: {str(e)}"

def search_conversations(query: str, limit: int = 5) -> str:
    """会話履歴を検索"""
    if not query.strip():
        return "🔍 検索クエリを入力してください"
    
    try:
        conversations = conversation_manager.get_conversations(
            limit=limit,
            search_query=query
        )
        
        if not conversations:
            return f"📭 「{query}」に関する会話が見つかりませんでした"
        
        display_text = f"# 🔍 検索結果: 「{query}」\n\n"
        
        for i, conv in enumerate(conversations, 1):
            timestamp = conv['timestamp']
            display_text += f"""
### 🎯 検索結果 {i} - {timestamp}
**👤 ユーザー:** {conv['user_message']}
**🤖 アシスタント:** {conv['assistant_response']}
**🏷️ タグ:** {conv.get('tags', 'なし')}

---
"""
        
        return display_text
        
    except Exception as e:
        return f"❌ 検索エラー: {str(e)}"

def get_conversation_statistics() -> str:
    """会話統計を取得"""
    try:
        stats = conversation_manager.get_statistics()
        
        stats_text = f"""
# 📊 会話統計ダッシュボード

## 📈 基本統計
- **📚 総会話数:** {stats['total_conversations']}
- **🎯 総セッション数:** {stats['total_sessions']}
- **📅 今日の会話数:** {stats['today_conversations']}

## 🔧 よく使用されるツール
"""
        
        if stats['top_tools']:
            for tool, count in stats['top_tools']:
                stats_text += f"- **{tool}:** {count}回\n"
        else:
            stats_text += "- まだツール使用履歴がありません\n"
        
        stats_text += f"""
## ⏰ 最終更新
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return stats_text
        
    except Exception as e:
        return f"❌ 統計取得エラー: {str(e)}"

def start_new_session_demo(session_name: str = "") -> str:
    """新しいセッションを開始"""
    try:
        session_id = start_new_conversation_session(
            session_name if session_name.strip() else None
        )
        return f"🆕 新しいセッションを開始しました\n**セッションID:** {session_id[:8]}..."
    except Exception as e:
        return f"❌ セッション開始エラー: {str(e)}"

# Gradioインターフェース作成
def create_demo_interface():
    """会話履歴統合デモインターフェースを作成"""
    
    with gr.Blocks(title="🎯 会話履歴統合デモ", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎯 会話履歴統合デモシステム")
        gr.Markdown("GitHub Copilotとの会話を自動記録し、履歴管理を行うデモです")
        
        with gr.Tab("💬 会話シミュレーション"):
            gr.Markdown("## ✍️ 会話ログ記録デモ")
            gr.Markdown("実際のGitHub Copilotとの会話をシミュレートして記録します")
            
            with gr.Row():
                user_input = gr.Textbox(
                    label="👤 ユーザーメッセージ",
                    placeholder="ContBK統合システムについて教えて...",
                    lines=2
                )
            
            with gr.Row():
                context_input = gr.Textbox(
                    label="📝 コンテキスト情報",
                    placeholder="開発中の機能、作業内容など...",
                    value=""
                )
                tags_input = gr.Textbox(
                    label="🏷️ タグ (カンマ区切り)",
                    placeholder="contbk, gradio, 統合システム",
                    value=""
                )
            
            simulate_btn = gr.Button("🚀 会話シミュレート & 記録", variant="primary")
            
            with gr.Row():
                with gr.Column(scale=2):
                    assistant_output = gr.Textbox(
                        label="🤖 アシスタント応答",
                        lines=3,
                        interactive=False
                    )
                with gr.Column(scale=1):
                    log_output = gr.Textbox(
                        label="💾 記録結果",
                        lines=2,
                        interactive=False
                    )
            
            session_info_display = gr.Markdown("## 🎯 セッション情報")
        
        with gr.Tab("📚 履歴閲覧"):
            gr.Markdown("## 📖 最近の会話履歴")
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 最新履歴を読み込み", variant="primary")
                limit_slider = gr.Slider(
                    label="📊 表示件数",
                    minimum=5,
                    maximum=20,
                    value=10,
                    step=1
                )
            
            conversation_list = gr.Markdown(
                value="🔄 「最新履歴を読み込み」ボタンを押してください"
            )
        
        with gr.Tab("🔍 履歴検索"):
            gr.Markdown("## 🕵️ 会話履歴検索")
            
            with gr.Row():
                search_query = gr.Textbox(
                    label="🔍 検索キーワード",
                    placeholder="contbk, gradio, システム...",
                    value=""
                )
                search_limit = gr.Slider(
                    label="📊 検索結果数",
                    minimum=3,
                    maximum=10,
                    value=5,
                    step=1
                )
            
            search_btn = gr.Button("🔍 検索実行", variant="primary")
            
            search_results = gr.Markdown(
                value="🔍 検索キーワードを入力して検索ボタンを押してください"
            )
        
        with gr.Tab("📊 統計・分析"):
            gr.Markdown("## 📈 会話統計ダッシュボード")
            
            stats_refresh_btn = gr.Button("📊 統計更新", variant="primary")
            
            statistics_display = gr.Markdown(
                value="📊 「統計更新」ボタンを押してください"
            )
        
        with gr.Tab("🎯 セッション管理"):
            gr.Markdown("## 🆕 新しいセッション管理")
            
            session_name_input = gr.Textbox(
                label="📝 セッション名",
                placeholder="例: ContBK機能追加, バグ修正作業...",
                value=""
            )
            
            new_session_btn = gr.Button("🆕 新しいセッション開始", variant="primary")
            
            session_result = gr.Textbox(
                label="📋 セッション管理結果",
                lines=3,
                interactive=False
            )
            
            current_session_display = gr.Markdown("## 🎯 現在のセッション")
        
        # イベントハンドラー
        simulate_btn.click(
            fn=simulate_conversation_logging,
            inputs=[user_input, context_input, tags_input],
            outputs=[assistant_output, log_output, session_info_display]
        )
        
        refresh_btn.click(
            fn=load_recent_conversations,
            inputs=[limit_slider],
            outputs=[conversation_list]
        )
        
        search_btn.click(
            fn=search_conversations,
            inputs=[search_query, search_limit],
            outputs=[search_results]
        )
        
        stats_refresh_btn.click(
            fn=get_conversation_statistics,
            outputs=[statistics_display]
        )
        
        new_session_btn.click(
            fn=start_new_session_demo,
            inputs=[session_name_input],
            outputs=[session_result]
        )
        
        # 初期表示
        interface.load(
            fn=lambda: (
                load_recent_conversations(10),
                get_conversation_statistics(),
                get_current_session_info()
            ),
            outputs=[conversation_list, statistics_display, current_session_display]
        )
    
    return interface

# Gradioインターフェースのファクトリー関数（遅延作成）
gradio_interface = create_demo_interface

if __name__ == "__main__":
    print("🎯 会話履歴統合デモ起動中...")
    interface = create_demo_interface()
    interface.launch(
        server_port=7873,  # ポート変更
        share=False,
        debug=True
    )
