#!/bin/bash

echo "🚀 Hugging Face Space 作成 & デプロイスクリプト"
echo "=============================================="

# 環境変数の確認
if [ -z "$HF_TOKEN" ]; then
    echo "❌ HF_TOKEN環境変数が設定されていません"
    echo "以下のコマンドで設定してください:"
    echo "export HF_TOKEN=\$HF_TOKEN"
    exit 1
fi

# 作業ディレクトリの設定
WORKSPACE_DIR="/workspaces/fastapi_django_main_live"
TEMP_DIR="/tmp/hf_create_$(date +%s)"
SPACE_NAME="fastapi-django-main-live"
USERNAME="mohsinbabur"

echo "📁 作業ディレクトリ: $WORKSPACE_DIR"
echo "👤 ユーザー名: $USERNAME"
echo "🏷️ スペース名: $SPACE_NAME"
echo "📂 一時ディレクトリ: $TEMP_DIR"

# 一時ディレクトリの作成
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# 新しいリポジトリディレクトリを作成
mkdir -p "$SPACE_NAME"
cd "$SPACE_NAME"

# Gitリポジトリを初期化
echo -e "\n🔧 Gitリポジトリを初期化中..."
git init
git config user.name "System Workflow Updater"
git config user.email "mohsinbabur@example.com"

# Hugging Face Spacesに必要なファイルを作成
echo -e "\n📝 必要ファイルを作成中..."

# README.mdを作成
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

## Components

### Core System Files
- `system_workflow_analysis.ipynb`: Comprehensive Jupyter Notebook with workflow analysis
- `controllers/gra_03_programfromdocs/`: Core system controllers and executors
- `prompts.db`: SQLite database for approval queue management

### Key Features
- **ApprovedItemExecutor**: Automated workflow execution
- **Integrated Dashboard**: Real-time system monitoring
- **GitHub API Integration**: Repository creation and management
- **Google Chat Integration**: Rich notification system
- **Mermaid Flowcharts**: Visual workflow representation

## Technology Stack

- **Backend**: FastAPI, SQLite, Python
- **Frontend**: Gradio, Streamlit
- **Integration**: GitHub API, Google Chat Webhooks
- **Visualization**: Mermaid.js, Matplotlib, Plotly
- **Data**: Pandas, NumPy

## Usage

1. Access the Gradio interface
2. Navigate through different system components
3. Monitor approval queues and execution logs
4. Review system analytics and workflows

This system represents a complete solution for modern workflow management and automation.
EOF

# app.pyを作成
cat > app.py << 'EOF'
import gradio as gr
import os
import sys
import sqlite3
import pandas as pd
from datetime import datetime
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_approval_queue_data():
    """Get approval queue data from database."""
    try:
        # Check if database exists
        if not os.path.exists('prompts.db'):
            return pd.DataFrame({'Message': ['Database not found']})
        
        conn = sqlite3.connect('prompts.db')
        query = "SELECT * FROM approval_queue ORDER BY created_at DESC LIMIT 10"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame({'Error': [str(e)]})

def get_execution_logs():
    """Get execution logs from database."""
    try:
        if not os.path.exists('prompts.db'):
            return pd.DataFrame({'Message': ['Database not found']})
        
        conn = sqlite3.connect('prompts.db')
        query = "SELECT * FROM execution_log ORDER BY executed_at DESC LIMIT 10"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame({'Error': [str(e)]})

def get_system_status():
    """Get overall system status."""
    status_info = []
    
    # Check database
    if os.path.exists('prompts.db'):
        status_info.append("✅ Database: Connected")
        try:
            conn = sqlite3.connect('prompts.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM approval_queue")
            queue_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM execution_log")
            log_count = cursor.fetchone()[0]
            conn.close()
            status_info.append(f"📋 Approval Queue: {queue_count} items")
            status_info.append(f"📊 Execution Logs: {log_count} entries")
        except Exception as e:
            status_info.append(f"⚠️ Database Error: {str(e)}")
    else:
        status_info.append("❌ Database: Not found")
    
    # Check key files
    key_files = [
        ('system_workflow_analysis.ipynb', 'Jupyter Notebook'),
        ('controllers/gra_03_programfromdocs/approved_item_executor.py', 'Item Executor'),
        ('controllers/gra_03_programfromdocs/integrated_dashboard.py', 'Dashboard')
    ]
    
    for file_path, description in key_files:
        if os.path.exists(file_path):
            status_info.append(f"✅ {description}: Available")
        else:
            status_info.append(f"❌ {description}: Missing")
    
    return "\n".join(status_info)

def main_interface():
    """Main Gradio interface for the system workflow analysis."""
    
    with gr.Blocks(title="System Workflow Analysis", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🔄 Advanced Prompt Management System")
        gr.Markdown("Welcome to the comprehensive workflow analysis and management system.")
        
        with gr.Tab("📊 System Dashboard"):
            gr.Markdown("## System Status")
            
            with gr.Row():
                with gr.Column():
                    status_output = gr.Textbox(
                        label="System Status",
                        lines=10,
                        interactive=False,
                        value=get_system_status()
                    )
                    refresh_btn = gr.Button("🔄 Refresh Status", variant="primary")
                    refresh_btn.click(get_system_status, outputs=status_output)
        
        with gr.Tab("📋 Approval Queue"):
            gr.Markdown("## Approval Queue Management")
            
            with gr.Row():
                queue_data = gr.Dataframe(
                    value=get_approval_queue_data(),
                    label="Current Approval Queue",
                    interactive=False
                )
                refresh_queue_btn = gr.Button("🔄 Refresh Queue")
                refresh_queue_btn.click(get_approval_queue_data, outputs=queue_data)
        
        with gr.Tab("📈 Execution Logs"):
            gr.Markdown("## System Execution History")
            
            with gr.Row():
                log_data = gr.Dataframe(
                    value=get_execution_logs(),
                    label="Recent Execution Logs",
                    interactive=False
                )
                refresh_logs_btn = gr.Button("🔄 Refresh Logs")
                refresh_logs_btn.click(get_execution_logs, outputs=log_data)
        
        with gr.Tab("📖 Documentation"):
            gr.Markdown("## System Documentation")
            
            gr.Markdown("""
            ### 🔧 Core Components
            
            1. **ApprovedItemExecutor**: Handles execution of approved workflow items
            2. **Integrated Dashboard**: Provides real-time system monitoring
            3. **GitHub Integration**: Automates repository creation and management
            4. **Google Chat Notifications**: Sends rich card notifications
            
            ### 📊 Database Schema
            
            - **approval_queue**: Stores items pending approval
            - **execution_log**: Tracks executed workflows and results
            
            ### 🔗 External Integrations
            
            - GitHub API for repository management
            - Google Chat Webhooks for notifications
            - Mermaid.js for workflow visualization
            
            ### 🚀 Quick Start
            
            1. Monitor system status in the Dashboard tab
            2. Review approval queue items
            3. Check execution logs for completed workflows
            4. Access the Jupyter notebook for detailed analysis
            """)
        
        with gr.Tab("⚙️ Configuration"):
            gr.Markdown("## System Configuration")
            
            gr.Markdown("""
            ### Environment Variables
            
            Configure the following environment variables for full functionality:
            
            - `GITHUB_TOKEN`: GitHub Personal Access Token
            - `GOOGLE_CHAT_WEBHOOK_URL`: Google Chat webhook URL
            - `HF_TOKEN`: Hugging Face token (for deployment)
            
            ### File Structure
            
            ```
            /
            ├── app.py                          # Main Gradio application
            ├── system_workflow_analysis.ipynb  # Comprehensive notebook
            ├── prompts.db                      # SQLite database
            ├── controllers/
            │   └── gra_03_programfromdocs/
            │       ├── approved_item_executor.py
            │       └── integrated_dashboard.py
            └── requirements.txt                # Python dependencies
            ```
            """)
    
    return demo

if __name__ == "__main__":
    demo = main_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
EOF

# requirements.txtを作成
cat > requirements.txt << 'EOF'
gradio>=4.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
python-multipart>=0.0.6
jinja2>=3.1.2
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
streamlit>=1.28.0
sqlite3
EOF

# .gitignoreを作成
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
*.tmp
*.temp
cache/
chroma/
flagged/
.env
.env.*
node_modules/
EOF

# ワークスペースファイルをコピー
echo -e "\n📋 ワークスペースファイルをコピー中..."

# 重要なファイルとディレクトリをコピー
if [ -d "$WORKSPACE_DIR" ]; then
    # controllers ディレクトリをコピー
    if [ -d "$WORKSPACE_DIR/controllers" ]; then
        cp -r "$WORKSPACE_DIR/controllers" ./
        echo "✅ controllers/ ディレクトリをコピーしました"
    fi
    
    # Jupyter notebookをコピー
    if [ -f "$WORKSPACE_DIR/system_workflow_analysis.ipynb" ]; then
        cp "$WORKSPACE_DIR/system_workflow_analysis.ipynb" ./
        echo "✅ system_workflow_analysis.ipynb をコピーしました"
    fi
    
    # データベースをコピー
    if [ -f "$WORKSPACE_DIR/prompts.db" ]; then
        cp "$WORKSPACE_DIR/prompts.db" ./
        echo "✅ prompts.db をコピーしました"
    fi
    
    # その他の重要なファイル
    for file in "*.py" "*.json" "*.yaml" "*.yml"; do
        if ls "$WORKSPACE_DIR"/$file 1> /dev/null 2>&1; then
            cp "$WORKSPACE_DIR"/$file ./ 2>/dev/null || true
        fi
    done
else
    echo "⚠️ ワークスペースディレクトリが見つかりません"
fi

# 最初のコミット
echo -e "\n💾 最初のコミットを作成中..."
git add .
git commit -m "🚀 Initial commit: Advanced Prompt Management System

- Complete Gradio interface for workflow management
- Approval queue and execution log monitoring
- System status dashboard
- Integration with GitHub API and Google Chat
- Comprehensive documentation and configuration

Features:
- Real-time system monitoring
- Interactive data visualization
- Database-driven workflow management
- Multi-tab interface for different system aspects"

# Hugging Face Spacesリモートを追加してプッシュ
echo -e "\n🔗 Hugging Face Spacesリモートを設定中..."
git remote add origin "https://oauth2:$HF_TOKEN@huggingface.co/spaces/$USERNAME/$SPACE_NAME"

echo -e "\n🚀 Hugging Face Spacesにプッシュ中..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "\n✅ Hugging Face Spacesの作成とデプロイが成功しました！"
    echo "🔗 スペースURL: https://huggingface.co/spaces/$USERNAME/$SPACE_NAME"
    echo -e "\n📊 デプロイされた機能："
    echo "- 📱 Gradioインターフェース"
    echo "- 📊 システムダッシュボード"
    echo "- 📋 承認キュー管理"
    echo "- 📈 実行ログ表示"
    echo "- 📖 包括的なドキュメント"
    echo "- ⚙️ システム設定"
    echo -e "\n⏳ スペースのビルドには数分かかる場合があります"
    echo "🌐 ビルド完了後、上記URLからアクセスできます"
else
    echo -e "\n❌ デプロイに失敗しました"
    echo "エラーログを確認してください"
fi

# クリーンアップ
echo -e "\n🧹 一時ファイルをクリーンアップ中..."
cd "$WORKSPACE_DIR"
rm -rf "$TEMP_DIR"

echo -e "\n🎉 デプロイ完了！"
