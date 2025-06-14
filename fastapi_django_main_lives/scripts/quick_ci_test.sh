#!/bin/bash
# 🚀 CI/CD自動テストシステム - クイック実行スクリプト

echo "🚀 AI-Human協働システム CI/CD自動テスト開始"
echo "=================================================="

# 環境チェック
echo "🔍 環境チェック中..."

# Python環境確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    exit 1
fi

# 必要なPythonパッケージ確認
python3 -c "import gradio_client" 2>/dev/null || {
    echo "⚠️ gradio-clientがインストールされていません。インストール中..."
    pip install gradio-client
}

# GitHub CLI確認
if ! command -v gh &> /dev/null; then
    echo "⚠️ GitHub CLIが見つかりません。GitHub Issue作成をスキップします"
    SKIP_GITHUB="--no-github-issue"
else
    echo "✅ GitHub CLI確認完了"
    SKIP_GITHUB=""
fi

# Gradioサーバー起動確認
echo "🔍 Gradioサーバー状態確認中..."
if curl -s http://localhost:7860 > /dev/null; then
    echo "✅ Gradioサーバー起動中"
else
    echo "⚠️ Gradioサーバーが起動していません"
    echo "   以下のコマンドでサーバーを起動してください:"
    echo "   python app.py"
    echo ""
    echo "🔄 サーバー起動なしでテスト続行..."
fi

# ディレクトリ作成
mkdir -p ci_reports
mkdir -p docs/images/screenshots
mkdir -p ci_issue_templates

# 実行権限付与
chmod +x run_complete_ci_pipeline.py
chmod +x ci_auto_test_system.py
chmod +x github_issue_ci_system.py

echo ""
echo "🚀 CI/CDパイプライン実行開始..."
echo "=================================================="

# CI/CDパイプライン実行
python3 run_complete_ci_pipeline.py $SKIP_GITHUB "$@"

RESULT=$?

echo ""
echo "=================================================="
if [ $RESULT -eq 0 ]; then
    echo "🎉 CI/CD自動テスト完了: 成功"
    echo "📊 詳細レポート: ci_reports/ フォルダを確認"
    echo "📸 スクリーンショット: docs/images/screenshots/ フォルダを確認"
    if [ -z "$SKIP_GITHUB" ]; then
        echo "📋 GitHub Issue: 自動作成されました"
    fi
else
    echo "❌ CI/CD自動テスト完了: 失敗"
    echo "🔧 修正が必要です。詳細はログを確認してください"
fi

echo "=================================================="
