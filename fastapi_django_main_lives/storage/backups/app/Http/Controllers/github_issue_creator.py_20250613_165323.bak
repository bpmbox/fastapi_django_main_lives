"""
GitHub Issue作成インターフェース
==============================

会話履歴から自動的にGitHub Issueを作成するGradioインターフェース
"""

import gradio as gr
import datetime
import sys
import os

# パスを追加
sys.path.append('/workspaces/fastapi_django_main_live')

from controllers.conversation_logger import create_quick_issue, get_current_session_info, conversation_logger

def create_github_issue_interface():
    """GitHub Issue作成インターフェース"""
    
    def create_issue_from_input(title, user_message, assistant_response, labels_text):
        """入力からGitHub Issueを作成"""
        try:
            # ラベルを処理
            labels = [label.strip() for label in labels_text.split(',') if label.strip()] if labels_text else []
            
            # Issue作成
            result = create_quick_issue(
                title=title,
                user_msg=user_message,
                assistant_msg=assistant_response,
                labels=labels
            )
            
            if result:
                return "✅ GitHub Issue作成成功！"
            else:
                return "❌ GitHub Issue作成失敗"
                
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    def get_session_info():
        """現在のセッション情報を取得"""
        try:
            info = get_current_session_info()
            return f"""
📊 **現在のセッション情報**
- セッションID: `{info.get('session_id', 'N/A')[:8]}`
- 会話数: {info.get('conversation_count', 0)}
- 継続時間: {info.get('duration_minutes', 0):.1f}分
            """
        except Exception as e:
            return f"⚠️ セッション情報取得エラー: {str(e)}"
    
    def get_suggested_labels():
        """おすすめラベルを取得"""
        return "enhancement, python, bug, documentation, question"
    
    with gr.Blocks(title="GitHub Issue Creator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🐙 GitHub Issue Creator
        
        会話内容から自動的にGitHub Issueを作成します。
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Issue作成フォーム
                with gr.Group():
                    gr.Markdown("## 📝 Issue作成")
                    
                    title_input = gr.Textbox(
                        label="Issue タイトル",
                        placeholder="例: ContBK統合システム：新機能開発",
                        lines=1
                    )
                    
                    user_msg_input = gr.Textbox(
                        label="ユーザーメッセージ",
                        placeholder="開発依頼や質問内容を入力...",
                        lines=4
                    )
                    
                    assistant_msg_input = gr.Textbox(
                        label="アシスタント回答",
                        placeholder="実装内容や解決方法を入力...",
                        lines=6
                    )
                    
                    labels_input = gr.Textbox(
                        label="ラベル (カンマ区切り)",
                        placeholder="enhancement, python",
                        lines=1
                    )
                    
                    with gr.Row():
                        create_btn = gr.Button("🚀 Issue作成", variant="primary")
                        clear_btn = gr.Button("🗑️ クリア", variant="secondary")
            
            with gr.Column(scale=1):
                # 情報パネル
                with gr.Group():
                    gr.Markdown("## ℹ️ 情報")
                    
                    session_info_display = gr.Markdown(get_session_info())
                    
                    refresh_info_btn = gr.Button("🔄 情報更新", size="sm")
                    
                    gr.Markdown("### 🏷️ 利用可能ラベル")
                    gr.Markdown("""
                    - `enhancement` - 新機能
                    - `python` - Python関連
                    - `bug` - バグ修正
                    - `documentation` - ドキュメント
                    - `question` - 質問
                    """)
                    
                    suggest_labels_btn = gr.Button("💡 ラベル提案", size="sm")
        
        # 結果表示
        with gr.Row():
            result_display = gr.Markdown("")
        
        # イベントハンドラー
        create_btn.click(
            fn=create_issue_from_input,
            inputs=[title_input, user_msg_input, assistant_msg_input, labels_input],
            outputs=[result_display]
        )
        
        clear_btn.click(
            fn=lambda: ("", "", "", ""),
            outputs=[title_input, user_msg_input, assistant_msg_input, labels_input]
        )
        
        refresh_info_btn.click(
            fn=get_session_info,
            outputs=[session_info_display]
        )
        
        suggest_labels_btn.click(
            fn=get_suggested_labels,
            outputs=[labels_input]
        )
        
        # サンプルデータ設定ボタン
        with gr.Row():
            sample_btn = gr.Button("📋 サンプルデータ設定", variant="secondary")
        
        def set_sample_data():
            return (
                "🤖 ContBK統合システム：GitHub Issue自動作成機能",
                "会話履歴をGitHub Issueに自動登録する機能が欲しい",
                "GitHub CLI(gh)を使用してIssue作成機能を実装しました。会話履歴から自動的にMarkdown形式のIssueを生成できます。",
                "enhancement, python"
            )
        
        sample_btn.click(
            fn=set_sample_data,
            outputs=[title_input, user_msg_input, assistant_msg_input, labels_input]
        )
    
    return interface

def create_gradio_interface():
    """Gradioインターフェースを作成"""
    return create_github_issue_interface()

# 自動検出用のgradio_interface（ファクトリー関数）
gradio_interface = create_gradio_interface
interface_title = "🐙 GitHub Issue Creator"
interface_description = "会話履歴からGitHub Issueを自動作成"

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        debug=True
    )
