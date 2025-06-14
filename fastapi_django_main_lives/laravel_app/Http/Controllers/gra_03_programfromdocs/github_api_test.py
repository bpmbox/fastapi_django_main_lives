#!/usr/bin/env python3
"""
GitHub API設定とGPT-ENGINEER統合のセットアップガイド
"""

import os
import requests
import subprocess
from pathlib import Path

def check_github_api_setup():
    """GitHub API設定の確認"""
    print("🔑 GitHub API設定確認")
    print("-" * 40)
    
    # 環境変数確認
    github_token = os.environ.get('GITHUB_TOKEN', '')
    if github_token:
        print(f"✅ GITHUB_TOKEN: 設定済み (長さ: {len(github_token)}文字)")
        
        # API接続テスト
        try:
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get('https://api.github.com/user', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ GitHub API接続: 成功")
                print(f"   ユーザー: {user_data.get('login', 'Unknown')}")
                print(f"   アカウント: {user_data.get('name', 'N/A')}")
                return True
            else:
                print(f"❌ GitHub API接続失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ GitHub API接続エラー: {e}")
            return False
    else:
        print("❌ GITHUB_TOKEN: 未設定")
        print("\n📋 設定方法:")
        print("export GITHUB_TOKEN='ghp_your_token_here'")
        return False

def check_gpt_engineer_setup():
    """GPT-ENGINEER設定の確認"""
    print("\n🤖 GPT-ENGINEER設定確認") 
    print("-" * 40)
    
    # OpenAI APIキー確認
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    if openai_key:
        print(f"✅ OPENAI_API_KEY: 設定済み (長さ: {len(openai_key)}文字)")
    else:
        print("❌ OPENAI_API_KEY: 未設定")
        print("\n📋 設定方法:")
        print("export OPENAI_API_KEY='sk-your_key_here'")
        return False
    
    # GPT-ENGINEERコマンド確認
    try:
        result = subprocess.run(['gpt-engineer', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ gpt-engineer コマンド: 利用可能")
            return True
        else:
            print("❌ gpt-engineer コマンド: エラー")
            return False
    except FileNotFoundError:
        print("❌ gpt-engineer コマンド: 見つかりません")
        print("\n📋 インストール方法:")
        print("pip install gpt-engineer")
        return False
    except Exception as e:
        print(f"❌ gpt-engineer コマンドエラー: {e}")
        return False

def create_setup_script():
    """セットアップスクリプトの生成"""
    setup_script = '''#!/bin/bash
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
'''
    
    with open('/workspaces/fastapi_django_main_live/setup_integration.sh', 'w') as f:
        f.write(setup_script)
    
    # 実行権限を付与
    subprocess.run(['chmod', '+x', '/workspaces/fastapi_django_main_live/setup_integration.sh'])
    print("📄 セットアップスクリプト作成: setup_integration.sh")

def test_integration():
    """統合機能のテスト"""
    print("\n🧪 統合機能テスト")
    print("-" * 40)
    
    # データベース接続テスト
    try:
        import sqlite3
        conn = sqlite3.connect('/workspaces/fastapi_django_main_live/prompts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM prompts')
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ データベース接続: 成功 ({count} プロンプト)")
    except Exception as e:
        print(f"❌ データベース接続エラー: {e}")
        return False
    
    # システム自動化クラステスト
    try:
        from system_automation import SystemAutomation
        print("✅ SystemAutomation: インポート成功")
    except Exception as e:
        print(f"❌ SystemAutomation インポートエラー: {e}")
        return False
    
    return True

def generate_demo_issue_template():
    """GitHub ISSUE テンプレートの生成"""
    issue_template = '''---
name: システム生成リクエスト
about: 自動システム生成を依頼する
title: '[SYSTEM-GEN] '
labels: system-generation, prompt-request
assignees: ''
---

## 📋 システム生成リクエスト

### 🎯 システム概要
<!-- 生成したいシステムの概要を記述してください -->

### 🔧 技術要件
- **バックエンド**: 
- **フロントエンド**: 
- **データベース**: 
- **その他**: 

### 📝 機能要件
1. 
2. 
3. 

### 🎨 デザイン要件
<!-- デザインに関する要求があれば記述してください -->

### 📊 その他の要求
<!-- その他の特別な要求があれば記述してください -->

---
**優先度**: [高/中/低]
**期限**: [期限があれば記載]

<!-- この ISSUE が作成されると、自動的にシステム生成が開始されます -->
'''
    
    # .github/ISSUE_TEMPLATE ディレクトリを作成
    template_dir = Path('/workspaces/fastapi_django_main_live/.github/ISSUE_TEMPLATE')
    template_dir.mkdir(parents=True, exist_ok=True)
    
    with open(template_dir / 'system-generation.md', 'w') as f:
        f.write(issue_template)
    
    print("📋 GitHub ISSUE テンプレート作成: .github/ISSUE_TEMPLATE/system-generation.md")

def main():
    """メイン実行"""
    print("🚀 GitHub + GPT-ENGINEER 統合システム設定確認")
    print("=" * 60)
    
    # 各種設定確認
    github_ok = check_github_api_setup()
    gpteng_ok = check_gpt_engineer_setup()
    integration_ok = test_integration()
    
    # セットアップスクリプト生成
    create_setup_script()
    
    # ISSUE テンプレート生成
    generate_demo_issue_template()
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 設定状況サマリー")
    print("-" * 40)
    
    status_items = [
        ("GitHub API設定", "✅ 完了" if github_ok else "❌ 要設定"),
        ("GPT-ENGINEER設定", "✅ 完了" if gpteng_ok else "❌ 要設定"),
        ("統合システム", "✅ 正常" if integration_ok else "❌ エラー"),
        ("セットアップスクリプト", "✅ 生成済み"),
        ("ISSUE テンプレート", "✅ 生成済み")
    ]
    
    for item, status in status_items:
        print(f"{status} {item}")
    
    # 次のステップ
    print(f"\n📋 次のステップ:")
    if not (github_ok and gpteng_ok):
        print("1. ./setup_integration.sh を実行してAPIキーを設定")
    print("2. GitHub リポジトリでISSUE monitoring を有効化")
    print("3. 統合システムで実際のテスト実行")
    
    # 統合完了度
    completion = sum([github_ok, gpteng_ok, integration_ok]) / 3 * 100
    print(f"\n🎯 統合完了度: {completion:.1f}%")
    
    if completion >= 80:
        print("🎉 本番運用準備完了！")
    elif completion >= 60:
        print("👍 あと少しで完成です")
    else:
        print("⚠️ 追加設定が必要です")

if __name__ == "__main__":
    main()
