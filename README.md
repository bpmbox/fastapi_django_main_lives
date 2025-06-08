---
title: FastAPI Django Main Live
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 8004
---

# FastAPI Debug Toolbar - Hugging Face Spaces

🚀 **Laravel風デバッグツールバー for FastAPI**

## 🌟 特徴

- ✅ **GitHub Actions自動デプロイ**
- 🔧 **Content-Length問題修正済み**
- 📊 **SQLAlchemy クエリ監視**
- ⚡ **リアルタイムパフォーマンス測定**
- 🎨 **Laravel風美しいUI**
- 🌐 **Hugging Face Spaces完全対応**

## 🚀 アクセス

デバッグツールバー付きのページにアクセスして、画面下部のバーをクリックしてください：

- `/demo` - 完全デモページ
- `/simple` - シンプルテスト
- `/users` - データベースクエリテスト

## 🔄 自動デプロイ

このスペースはGitHub Actionsで自動更新されます：
- `main`ブランチへのプッシュで自動デプロイ
- 手動実行も可能
- デバッグツールバーの最新版を常に反映

## 📡 最終更新

Last deployed: 2025-06-08 13:50:00 UTC

## 🛠️ GitHub Actions設定手順

1. **GitHubリポジトリを作成**
   ```
   リポジトリ名: fastapi_django_main_live
   公開設定: Public
   説明: FastAPI Debug Toolbar with auto-deployment
   ```

2. **HF_TOKENシークレットを設定**
   - GitHubリポジトリ → Settings → Secrets and variables → Actions
   - New repository secret で `HF_TOKEN` を追加
   - Hugging Face token を値として設定

3. **自動デプロイの実行**
   - mainブランチにプッシュすると自動デプロイ開始
   - Actions タブで進行状況を確認

## 📊 デバッグツールバー機能

- ✅ Laravel-style UI with gradients
- ✅ SQLAlchemy query monitoring  
- ✅ Real-time performance tracking
- ✅ Streaming response (Content-Length fixed)
- ✅ Interactive toolbar (click to expand)
- ✅ Request/Response analysis
- ✅ Database query profiling
- ✅ Memory and CPU usage tracking