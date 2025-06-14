
# 🚀 統合プロンプト管理システム - ユーザーガイド

## 📋 システム概要

このシステムは、**GitHub ISSUE**を通じて誰でも自動システム生成を依頼できる、
**GPT-ENGINEER統合自動化システム**です。

## 🎯 主な機能

### 1️⃣ プロンプト管理
- **URL**: http://localhost:7861
- プロンプトの保存・管理
- 実行履歴の確認
- システム生成の実行

### 2️⃣ 統合管理ダッシュボード
- **URL**: http://localhost:7862
- システム全体の監視
- GitHub ISSUE監視の制御
- リアルタイム状況確認

### 3️⃣ GitHub ISSUE連携
- **リポジトリ**: https://github.com/miyataken999/fastapi_django_main_live
- ISSUEでシステム生成依頼
- 自動承認・生成・納品
- 結果のコメント通知

## 🔧 使用方法

### 📝 システム管理者の場合

1. **統合ダッシュボードにアクセス**
   ```
   http://localhost:7862
   ```

2. **ISSUE監視開始**
   - 「🚀 ISSUE監視開始」ボタンをクリック
   - 24時間自動監視が開始されます

3. **プロンプト管理**
   ```
   http://localhost:7861
   ```
   - 手動でのプロンプト実行
   - 生成履歴の確認

### 🌐 外部ユーザーの場合

1. **GitHub ISSUEでリクエスト**
   - リポジトリ: https://github.com/miyataken999/fastapi_django_main_live
   - 「Issues」→「New issue」
   - 「システム生成リクエスト」テンプレートを使用

2. **リクエスト例**
   ```markdown
   ## 📋 システム生成リクエスト

   ### 🎯 システム概要
   FastAPIとVue.jsを使用したタスク管理システム

   ### 🔧 技術要件
   - バックエンド: FastAPI + SQLAlchemy
   - フロントエンド: Vue.js 3
   - データベース: PostgreSQL

   ### 📝 機能要件
   1. タスクの作成・編集・削除
   2. ユーザー認証
   3. 進捗管理

   ---
   **優先度**: 中
   **期限**: 1週間以内
   ```

3. **ラベル設定**
   - `system-generation`
   - `prompt-request`

4. **自動処理フロー**
   - ISSUE検出（30秒以内）
   - 要件解析・承認
   - GPT-ENGINEERによるシステム生成
   - GitHubリポジトリ自動作成
   - 生成コードのプッシュ
   - ISSUEに結果コメント

## ⚙️ 設定

### 🔑 API設定

```bash
# GitHub Personal Access Token
export GITHUB_TOKEN="ghp_your_token_here"

# OpenAI API Key (GPT-ENGINEER用)
export OPENAI_API_KEY="sk-your_key_here"
```

### 📁 ディレクトリ構成

```
/workspaces/fastapi_django_main_live/
├── controllers/gra_03_programfromdocs/  # システムファイル
├── prompts.db                           # プロンプトDB
├── github_issues.db                     # ISSUE履歴DB
└── test_generated_systems/              # 生成システム
```

## 🆘 トラブルシューティング

### ❌ GitHub API接続エラー
```bash
# Token確認
echo $GITHUB_TOKEN

# Token設定
export GITHUB_TOKEN="your_token_here"
```

### ❌ GPT-ENGINEER実行エラー
```bash
# OpenAI API Key確認
echo $OPENAI_API_KEY

# Key設定
export OPENAI_API_KEY="your_key_here"
```

### ❌ ポートエラー
```bash
# ポート使用状況確認
netstat -tlnp | grep :786

# プロセス停止
pkill -f "gradio"
```

## 📊 監視・ログ

### 📈 ダッシュボード監視
- システム状況のリアルタイム確認
- 最近のアクティビティ表示
- 監視プロセスの制御

### 📝 ログ確認
```bash
# プロンプト実行履歴
sqlite3 prompts.db "SELECT * FROM prompts ORDER BY created_at DESC LIMIT 10;"

# ISSUE処理履歴
sqlite3 github_issues.db "SELECT * FROM processed_issues ORDER BY processed_at DESC LIMIT 10;"
```

## 🔗 関連リンク

- **メインシステム**: http://localhost:7861
- **管理ダッシュボード**: http://localhost:7862
- **GitHubリポジトリ**: https://github.com/miyataken999/fastapi_django_main_live
- **生成システムAPI**: http://localhost:8000 (テスト時)

---

**開発者**: GitHub Copilot AI Assistant  
**最終更新**: 2025年06月11日  
**バージョン**: 1.0.0
        