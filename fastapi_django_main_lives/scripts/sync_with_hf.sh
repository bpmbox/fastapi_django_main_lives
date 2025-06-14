#!/bin/bash

echo "🚀 Hugging Face リポジトリ同期スクリプト"
echo "=========================================="

# 環境変数の確認
if [ -z "$HF_TOKEN" ]; then
    echo "❌ HF_TOKEN環境変数が設定されていません"
    echo "以下のコマンドで設定してください:"
    echo "export HF_TOKEN=\$HF_TOKEN"
    exit 1
fi

# 作業ディレクトリの設定
WORKSPACE_DIR="/workspaces/fastapi_django_main_live"
HF_REPO_URL="https://huggingface.co/spaces/mohsinbabur/fastapi-django-main-live"
TEMP_DIR="/tmp/hf_sync_$(date +%s)"

echo "📁 作業ディレクトリ: $WORKSPACE_DIR"
echo "🔗 HFリポジトリ: $HF_REPO_URL"
echo "📂 一時ディレクトリ: $TEMP_DIR"

# 一時ディレクトリの作成
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo -e "\n📥 Hugging Faceリポジトリをクローン中..."
git clone "https://oauth2:$HF_TOKEN@huggingface.co/spaces/mohsinbabur/fastapi-django-main-live" hf_repo

if [ $? -ne 0 ]; then
    echo "❌ リポジトリのクローンに失敗しました"
    exit 1
fi

cd hf_repo

# Gitの設定
echo -e "\n🔧 Git設定を更新中..."
git config user.name "System Workflow Updater"
git config user.email "mohsinbabur@example.com"

# リモートURLを認証トークン付きに更新
git remote set-url origin "https://oauth2:$HF_TOKEN@huggingface.co/spaces/mohsinbabur/fastapi-django-main-live"

# 現在のファイルをバックアップ（重要なものだけ）
echo -e "\n💾 重要ファイルのバックアップ中..."
mkdir -p backup
cp README.md backup/ 2>/dev/null || echo "README.mdが見つかりません"
cp .gitignore backup/ 2>/dev/null || echo ".gitignoreが見つかりません"
cp app.py backup/ 2>/dev/null || echo "app.pyが見つかりません"

# 既存のファイルを削除（.gitディレクトリは保持）
echo -e "\n🧹 既存ファイルを削除中..."
find . -type f ! -path "./.git/*" ! -name ".git*" -delete
find . -type d -empty ! -path "./.git/*" -delete

# 現在のワークスペースからファイルをコピー
echo -e "\n📋 ワークスペースファイルをコピー中..."

# 重要なファイルとディレクトリをコピー
rsync -av --exclude='.git/' \
          --exclude='__pycache__/' \
          --exclude='*.pyc' \
          --exclude='node_modules/' \
          --exclude='.env' \
          --exclude='*.log' \
          --exclude='cache/' \
          --exclude='chroma/' \
          --exclude='flagged/' \
          "$WORKSPACE_DIR/" ./

# Hugging Face Spacesに必要なファイルがあるか確認
if [ ! -f "app.py" ]; then
    echo "⚠️ app.pyが見つかりません。デフォルトを作成します..."
    cat > app.py << 'EOF'
import gradio as gr
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main_interface():
    """Main Gradio interface for the system workflow analysis."""
    
    with gr.Blocks(title="System Workflow Analysis") as demo:
        gr.Markdown("# 🔄 Advanced Prompt Management System")
        gr.Markdown("This system provides comprehensive workflow analysis and management capabilities.")
        
        with gr.Tab("📊 Dashboard"):
            gr.Markdown("## System Dashboard")
            gr.HTML("<p>Access the integrated dashboard for system monitoring and management.</p>")
            
        with gr.Tab("📋 Approval Queue"):
            gr.Markdown("## Approval Management")
            gr.HTML("<p>Manage approval workflows and queue items.</p>")
            
        with gr.Tab("📈 Analytics"):
            gr.Markdown("## System Analytics")
            gr.HTML("<p>View system performance and workflow analytics.</p>")
    
    return demo

if __name__ == "__main__":
    demo = main_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
EOF
fi

# requirements.txtを更新
echo -e "\n📦 requirements.txtを更新中..."
cat > requirements.txt << 'EOF'
gradio>=4.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
sqlite3
pandas>=2.0.0
numpy>=1.24.0
python-multipart>=0.0.6
jinja2>=3.1.2
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
streamlit>=1.28.0
EOF

# README.mdを更新
echo -e "\n📝 README.mdを更新中..."
cat > README.md << 'EOF'
---
title: FastAPI Django Main Live
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🔄 Advanced Prompt Management System

A comprehensive system for analyzing complex workflows, managing approval processes, and integrating with GitHub and Google Chat.

## Features

- 📊 **System Dashboard**: Real-time monitoring and management
- 📋 **Approval Workflow**: Queue management and execution tracking
- 🔗 **GitHub Integration**: Automatic repository creation and management
- 💬 **Google Chat Notifications**: Rich card notifications for system events
- 📈 **Analytics**: Comprehensive workflow analysis and reporting

## Quick Start

The system automatically launches a Gradio interface for easy interaction with all features.

## Architecture

Built with FastAPI, Django components, and modern web technologies for scalable workflow management.
EOF

# .gitignoreを更新
echo -e "\n🔒 .gitignoreを更新中..."
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.sqlite3
*.db
.env
.env.*
node_modules/
*.tmp
*.temp
cache/
chroma/
flagged/
EOF

# 変更をステージング
echo -e "\n📤 変更をステージング中..."
git add .

# コミット
echo -e "\n💾 変更をコミット中..."
git commit -m "🚀 System workflow analysis update - Complete prompt management system

- Added comprehensive Jupyter Notebook for workflow analysis
- Implemented approval queue management system
- Added GitHub API integration for repository creation
- Integrated Google Chat notifications with rich cards
- Created interactive dashboards for system monitoring
- Updated all dependencies and configurations

Features:
- ApprovedItemExecutor class for workflow automation
- SQLite database for approval queue and execution logs
- Mermaid flowcharts for system visualization
- Modern Gradio interface for easy access"

# 強制プッシュ
echo -e "\n🚀 Hugging Faceにプッシュ中..."
git push origin main --force

if [ $? -eq 0 ]; then
    echo -e "\n✅ Hugging Faceへのプッシュが成功しました！"
    echo "🔗 アプリケーションURL: https://huggingface.co/spaces/mohsinbabur/fastapi-django-main-live"
    echo -e "\n📊 デプロイ状況："
    echo "- Gradioアプリケーションが自動的に起動します"
    echo "- システムダッシュボードにアクセス可能"
    echo "- 全ての機能が利用可能"
else
    echo -e "\n❌ プッシュに失敗しました"
    echo "エラーログを確認してください"
fi

# クリーンアップ
echo -e "\n🧹 一時ファイルをクリーンアップ中..."
cd "$WORKSPACE_DIR"
rm -rf "$TEMP_DIR"

echo -e "\n🎉 同期完了！"
