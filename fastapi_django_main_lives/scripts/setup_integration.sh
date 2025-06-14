#!/bin/bash
# GitHub + GPT-ENGINEER 統合システム セットアップスクリプト

echo "🚀 GitHub + GPT-ENGINEER 統合システム セットアップ"
echo "=================================================="

# 1. GitHub Personal Access Token設定
echo ""
echo "1️⃣ GitHub Personal Access Token設定"
echo "以下のURLでTokenを生成してください:"
echo "https://github.com/settings/tokens/new"
echo ""
echo "必要な権限:"
echo "- repo (フルアクセス)"
echo "- admin:org (リポジトリ作成用)"
echo ""
read -p "GitHub Token を入力してください: " github_token
export GITHUB_TOKEN="$github_token"
echo "export GITHUB_TOKEN='$github_token'" >> ~/.bashrc

# 2. OpenAI API Key設定
echo ""
echo "2️⃣ OpenAI API Key設定"
echo "https://platform.openai.com/api-keys でAPIキーを生成してください"
echo ""
read -p "OpenAI API Key を入力してください: " openai_key
export OPENAI_API_KEY="$openai_key"
echo "export OPENAI_API_KEY='$openai_key'" >> ~/.bashrc

# 3. GPT-ENGINEER インストール確認
echo ""
echo "3️⃣ GPT-ENGINEER インストール確認"
if command -v gpt-engineer &> /dev/null; then
    echo "✅ gpt-engineer は既にインストール済みです"
else
    echo "📦 gpt-engineer をインストール中..."
    pip install gpt-engineer
fi

# 4. 統合システム動作確認
echo ""
echo "4️⃣ 統合システム動作確認"
cd /workspaces/fastapi_django_main_live/controllers/gra_03_programfromdocs
python3 github_api_test.py

echo ""
echo "✅ セットアップ完了！"
echo "🌐 統合システムにアクセス: http://localhost:7861"
