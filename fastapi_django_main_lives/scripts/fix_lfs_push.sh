#!/bin/bash

echo "🔧 Git LFS プッシュ問題の修復スクリプト"
echo "================================================"

# Git LFS設定の確認
echo "📊 現在のGit LFS設定:"
git lfs track

# LFSオブジェクトの状態確認
echo -e "\n📋 LFS オブジェクトの状態:"
git lfs status

# 問題のファイルを一時的にGit管理から除外
echo -e "\n🔧 問題のファイルを一時的に除外:"

# 問題のファイルをバックアップ
mkdir -p /tmp/lfs_backup
cp "docs/images/collected/test_2/118224532-3842c400-b438-11eb-923d-a5f66fa6785a.png" /tmp/lfs_backup/ 2>/dev/null || echo "ファイル1のバックアップに失敗"
cp "docs/images/screenshots/contbk_dashboard.png" /tmp/lfs_backup/ 2>/dev/null || echo "ファイル2のバックアップに失敗"

# .gitignoreに一時的に追加
echo "# 一時的にLFS問題のあるファイルを除外" >> .gitignore
echo "docs/images/collected/test_2/118224532-3842c400-b438-11eb-923d-a5f66fa6785a.png" >> .gitignore
echo "docs/images/screenshots/contbk_dashboard.png" >> .gitignore

# Gitから削除（ファイルは保持）
git rm --cached "docs/images/collected/test_2/118224532-3842c400-b438-11eb-923d-a5f66fa6785a.png" 2>/dev/null || echo "ファイル1は既にキャッシュにありません"
git rm --cached "docs/images/screenshots/contbk_dashboard.png" 2>/dev/null || echo "ファイル2は既にキャッシュにありません"

# 変更をコミット
git add .gitignore
git commit -m "🔧 Temporarily exclude problematic LFS files for push fix"

echo -e "\n✅ LFS問題修復準備完了"
echo "次のステップ:"
echo "1. git push でプッシュを試行"
echo "2. 成功後、バックアップからファイルを復元"
echo "3. .gitignore から除外設定を削除"
