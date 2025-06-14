"""
統合プロンプト管理システム - メインインターフェース
GPT-ENGINEERによる自動システム生成、GitHub連携、Controller統合の統合管理
"""

import gradio as gr
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lavelo import gradio_interface as prompt_manager
from system_automation import system_automation_interface
from system_dashboard import dashboard_interface

def create_integrated_interface():
    """統合プロンプト管理システムのメインインターフェース"""
    
    with gr.Blocks(title="🚀 統合プロンプト管理システム", theme="soft") as main_interface:
        gr.Markdown("""
        # 🚀 統合プロンプト管理システム
        
        **GPT-ENGINEERによる自動システム生成 → GitHub連携 → Controller自動統合**
        
        このシステムでは以下のことができます：
        
        1. **📝 プロンプト管理** - システム生成用プロンプトの保存・管理
        2. **🚀 自動システム生成** - GPT-ENGINEERによる高品質システム生成
        3. **🔗 GitHub自動連携** - 生成されたシステムを自動でGitHubにアップロード
        4. **🔧 Controller自動統合** - FastAPI Router、Gradio Interface等の自動認識・統合
        5. **📊 統合管理ダッシュボード** - システム全体の監視・管理
        6. **💬 Google Chat通知** - 生成完了時の自動通知
        
        ---
        """)
        
        with gr.Tabs():
            with gr.TabItem("📝 プロンプト管理"):
                # プロンプト管理システムを直接埋め込み
                with prompt_manager:
                    pass
            
            with gr.TabItem("🚀 システム自動化"):
                # システム自動化インターフェースを直接埋め込み
                with system_automation_interface:
                    pass
            
            with gr.TabItem("📊 管理ダッシュボード"):
                # ダッシュボードを直接埋め込み
                with dashboard_interface:
                    pass
            
            with gr.TabItem("📚 使い方ガイド"):
                gr.Markdown("""
                ## 📚 システム使用ガイド
                
                ### 🔄 基本的なワークフロー
                
                1. **プロンプト作成・保存**
                   - 「プロンプト管理」タブでシステム生成用プロンプトを作成
                   - GitHub URLとシステムタイプを設定
                   - 保存して管理
                
                2. **システム生成実行**
                   - プロンプト一覧から実行したいプロンプトを選択
                   - GitHub Tokenを設定
                   - 「システム生成実行」ボタンでGPT-ENGINEERを実行
                
                3. **自動統合確認**
                   - 生成されたシステムが自動でGitHubにアップロード
                   - FastAPI Router、Gradio Interface等が自動で検出・統合
                   - Google Chatに完了通知
                
                4. **統合管理**
                   - 「管理ダッシュボード」で全システムの状態を監視
                   - 成功率、システムタイプ別統計等を確認
                
                ### 🤖 AI生成プロンプトの活用
                
                このシステムには以下の高品質プロンプトが事前に用意されています：
                
                - **🔗 マイクロサービスAPI**: FastAPI + SQLAlchemy + JWT認証
                - **🤖 AIチャットシステム**: RAG対応、リアルタイムチャット
                - **⛓️ ブロックチェーンDApp**: Solidity + Web3.js
                - **🛠️ DevOpsインフラ**: Kubernetes + Terraform + CI/CD
                
                ### 💡 使用のコツ
                
                1. **明確なプロンプト**: 具体的な要件と技術スタックを明記
                2. **GitHub Token**: Personal Access Token（repo権限必要）
                3. **フォルダ構成**: 生成されたシステムの適切な配置
                4. **エラー対応**: ログを確認して問題を特定
                
                ### 🔧 トラブルシューティング
                
                - **GitHub連携エラー**: Token権限とリポジトリ名を確認
                - **Controller認識エラー**: ファイル構成とコード形式を確認
                - **実行エラー**: プロンプト内容とシステム要件を確認
                
                ### 📞 サポート
                
                システムに関する質問やエラーは Google Chat に自動通知されます。
                技術的な問題については開発チームまでお気軽にお声がけください。
                """)
            
            with gr.TabItem("⚙️ システム設定"):
                gr.Markdown("## ⚙️ システム設定")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 🔑 認証設定")
                        github_token_setting = gr.Textbox(
                            label="デフォルトGitHub Token",
                            type="password",
                            placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                        )
                        google_chat_webhook = gr.Textbox(
                            label="Google Chat Webhook URL",
                            placeholder="https://chat.googleapis.com/..."
                        )
                        
                        gr.Markdown("### 📁 パス設定")
                        workspace_path = gr.Textbox(
                            label="ワークスペースパス",
                            value="/workspaces/fastapi_django_main_live"
                        )
                        output_folder = gr.Textbox(
                            label="出力フォルダ名",
                            value="generated_systems"
                        )
                    
                    with gr.Column():
                        gr.Markdown("### 🚀 実行設定")
                        auto_github = gr.Checkbox(label="GitHub自動連携", value=True)
                        auto_integrate = gr.Checkbox(label="Controller自動統合", value=True)
                        auto_notify = gr.Checkbox(label="Google Chat自動通知", value=True)
                        
                        gr.Markdown("### 📊 システム情報")
                        system_info = gr.Textbox(
                            label="システム情報",
                            value=f"""Python Version: 3.11
Gradio Version: 4.31.5
Database: SQLite3
Workspace: /workspaces/fastapi_django_main_live""",
                            interactive=False,
                            lines=6
                        )
                
                save_settings_btn = gr.Button("💾 設定保存", variant="primary")
                settings_result = gr.Textbox(label="設定結果", interactive=False)
                
                def save_settings(*args):
                    return "✅ 設定を保存しました（※実装予定）"
                
                save_settings_btn.click(
                    fn=save_settings,
                    inputs=[github_token_setting, google_chat_webhook, workspace_path, output_folder, auto_github, auto_integrate, auto_notify],
                    outputs=settings_result
                )
        
        gr.Markdown("""
        ---
        
        **🔗 関連リンク:**
        - [GPT-ENGINEER GitHub](https://github.com/gpt-engineer-org/gpt-engineer)
        - [FastAPI ドキュメント](https://fastapi.tiangolo.com/)
        - [Gradio ドキュメント](https://gradio.app/docs/)
        
        **📞 開発者:** GitHub Copilot AI Assistant  
        **📅 最終更新:** 2025年6月11日
        """)
    
    return main_interface

# メインインターフェースを作成
if __name__ == "__main__":
    interface = create_integrated_interface()
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )
else:
    # モジュールとしてインポートされた場合
    gradio_interface = create_integrated_interface()
