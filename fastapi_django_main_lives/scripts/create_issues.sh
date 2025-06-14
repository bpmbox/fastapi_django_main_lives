#!/bin/bash
# GitHub Issues作成スクリプト

echo '🚀 GitHub Issuesを作成しています...'

echo 'Issue 1: 作成中...'
gh issue create \
  --title "🏗️ 階層化インターフェースシステムの検証依頼 - UIユーザビリティ改善" \
  --body-file "issue_1_body.md" \
  --label "enhancement,ui-ux,verification-needed"
echo 'Issue 1: 完了'

echo 'Issue 2: 作成中...'
gh issue create \
  --title "🤖 Gradio API自動テストシステムの実証 - GUI操作完全自動化" \
  --body-file "issue_2_body.md" \
  --label "automation,testing,innovation,verification-needed"
echo 'Issue 2: 完了'

echo 'Issue 3: 作成中...'
gh issue create \
  --title "🎓 初心者ガイドシステムのユーザビリティ検証 - オンボーディング改善" \
  --body-file "issue_3_body.md" \
  --label "documentation,user-experience,onboarding,verification-needed"
echo 'Issue 3: 完了'

echo 'Issue 4: 作成中...'
gh issue create \
  --title "🤝 AI-Human協働ワークフローの実証検証 - 24時間高速開発システム" \
  --body-file "issue_4_body.md" \
  --label "ai-collaboration,workflow,productivity,verification-needed"
echo 'Issue 4: 完了'

echo 'Issue 5: 作成中...'
gh issue create \
  --title "⚡ システム全体のパフォーマンス・安定性検証 - 本番運用可能性評価" \
  --body-file "issue_5_body.md" \
  --label "performance,stability,production-ready,verification-needed"
echo 'Issue 5: 完了'

echo '✅ 全てのIssuesが作成されました！'
