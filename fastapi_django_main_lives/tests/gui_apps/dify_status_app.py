#!/usr/bin/env python3
"""
🚀 Dify Docker環境管理システム - Gradio UI
"""

import gradio as gr
import subprocess
import os
import json
from datetime import datetime

def get_docker_status():
    """Dockerコンテナの状態を取得"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        container = json.loads(line)
                        containers.append(f"✅ {container.get('Names', 'Unknown')} - {container.get('Status', 'Unknown')}")
                    except:
                        pass
            return "\n".join(containers) if containers else "🔍 コンテナが見つかりません"
        else:
            return f"❌ Docker確認エラー: {result.stderr}"
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def get_dify_status():
    """Difyの状態を取得"""
    try:
        result = subprocess.run(['curl', '-s', '-I', 'http://localhost'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "200\|30" in result.stdout:
            return "🟢 Dify正常稼働中 - http://localhost でアクセス可能"
        else:
            return "🔴 Dify接続不可 - 起動が必要かもしれません"
    except:
        return "❌ Dify状態確認エラー"

def create_github_issue_content(title, description):
    """GitHub Issue用のコンテンツを生成"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    issue_content = f"""# {title}

## 📅 作成日時
{timestamp}

## 📋 説明
{description}

## 🔧 技術詳細

### Docker環境
{get_docker_status()}

### Dify状態
{get_dify_status()}

## ✅ 完了項目
- [x] Docker環境セットアップ
- [x] Dify docker-compose起動
- [x] HTTP接続確認
- [x] Gradio UI作成

## 🎯 次のステップ
- [ ] Dify初期設定
- [ ] APIキー設定
- [ ] ワークフロー作成

---
*自動生成 by AI-Human協働開発システム*
"""
    return issue_content

def refresh_status():
    """ステータスを更新"""
    docker_status = get_docker_status()
    dify_status = get_dify_status()
    
    return f"""🚀 **システム状態** (更新: {datetime.now().strftime("%H:%M:%S")})

## 🐳 Docker コンテナ
{docker_status}

## 🤖 Dify サービス  
{dify_status}

## 📊 リソース情報
- 作業ディレクトリ: /workspaces/fastapi_django_main_live
- Gradio UI: https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/
- Dify Web: http://localhost (ローカル)
"""

# Gradio インターフェース
with gr.Blocks(
    title="🚀 AI-Human協働開発システム",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    """
) as app:
    
    gr.Markdown("""
    # 🚀 Dify Docker環境管理システム
    
    **AI-Human協働開発プロジェクト** - 24時間で30年の夢を実現
    """)
    
    with gr.Tabs():
        
        with gr.Tab("📊 システム状態"):
            status_display = gr.Textbox(
                value=refresh_status(),
                lines=15,
                label="現在のシステム状態",
                interactive=False
            )
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 状態更新", variant="primary")
                refresh_btn.click(refresh_status, outputs=status_display)
        
        with gr.Tab("📝 GitHub Issue作成"):
            with gr.Column():
                title_input = gr.Textbox(
                    value="🚀 Dify Docker環境セットアップ完了報告",
                    label="Issue タイトル",
                    placeholder="Issueのタイトルを入力"
                )
                
                description_input = gr.Textbox(
                    value="""DevContainer環境でDifyのdocker-compose環境を完全セットアップしました。

## 主な成果
- 全Dockerコンテナ正常起動
- HTTP接続確認完了  
- Gradio UI システム構築
- ドキュメント完全整備

24時間以内での完全セットアップを達成し、AI-Human協働開発環境が完成しました。""",
                    lines=8,
                    label="Issue 説明",
                    placeholder="Issueの詳細説明を入力"
                )
                
                generate_btn = gr.Button("📋 Issue内容生成", variant="secondary")
                
                issue_output = gr.Textbox(
                    lines=20,
                    label="生成されたIssue内容 (GitHubにコピー&ペースト)",
                    placeholder="「Issue内容生成」ボタンを押すと、GitHub Issue用の完全なマークダウンが生成されます"
                )
                
                generate_btn.click(
                    create_github_issue_content,
                    inputs=[title_input, description_input],
                    outputs=issue_output
                )
        
        with gr.Tab("🔧 システム管理"):
            gr.Markdown("""
            ## 🐳 Docker操作
            
            手動でのDocker操作が必要な場合は、以下のコマンドをターミナルで実行してください：
            
            ```bash
            # Dify起動
            cd /workspaces/fastapi_django_main_live/dify-setup/dify/docker
            docker compose up -d
            
            # 状態確認
            docker ps
            
            # ログ確認
            docker compose logs -f
            
            # 停止
            docker compose down
            ```
            
            ## 🌐 アクセスURL
            - **このGradio UI**: https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/
            - **Dify Web (ローカル)**: http://localhost
            - **VS Code**: 現在の開発環境
            """)

if __name__ == "__main__":
    print("🚀 Dify管理システム起動中...")
    print("📊 初期状態確認:")
    print(refresh_status())
    print("\n🌐 Gradio UI起動...")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        quiet=False
    )
