# 🚀 実際のGradio APIテストレポート

## 📋 テスト概要
- **実行日時**: 2025-06-13 14:41:28
- **テストID**: 20250613_144125
- **実行時間**: 3.04秒
- **Codespace URL**: https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev
- **API一覧URL**: https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/?view=api

## 📊 テスト結果サマリー

### 🎯 全体結果
- **成功率**: 2/10 (20.0%)
- **平均レスポンス時間**: 0.28秒
- **総合判定**: ❌ 失敗

### 📋 カテゴリ別結果
| カテゴリ | 成功/総数 | 成功率 |
|----------|-----------|--------|
| プロンプト管理 | 0/3 | 0.0% |
| AI応答 | 0/1 | 0.0% |
| ログ管理 | 0/1 | 0.0% |
| ファイル管理 | 1/1 | 100.0% |
| データベース | 0/1 | 0.0% |
| GitHub連携 | 0/1 | 0.0% |
| チャット | 1/1 | 100.0% |
| コード実行 | 0/1 | 0.0% |

## 📋 詳細APIテスト結果

| API名 | エンドポイント | カテゴリ | 状態 | 応答時間 | 説明 |
|-------|----------------|----------|------|----------|------|
| create_prompt | `/create_prompt` | プロンプト管理 | ❌ | 0秒 | プロンプト作成API |
| save_prompt | `/save_prompt` | プロンプト管理 | ❌ | 0秒 | プロンプト保存API |
| load_prompts | `/load_prompts` | プロンプト管理 | ❌ | 0秒 | プロンプト読み込みAPI |
| generate_response | `/generate_response` | AI応答 | ❌ | 0秒 | レスポンス生成API |
| conversation_log | `/log_conversation` | ログ管理 | ❌ | 0秒 | 会話ログAPI |
| file_upload | `/upload_file` | ファイル管理 | ✅ | 0秒 | ファイルアップロードAPI |
| database_query | `/execute_query` | データベース | ❌ | 0秒 | データベースクエリAPI |
| github_issue | `/create_issue` | GitHub連携 | ❌ | 0秒 | GitHub Issue作成API |
| chat_response | `/chat` | チャット | ✅ | 0.57秒 | チャットAPI |
| interpreter | `/interpret` | コード実行 | ❌ | 0秒 | インタープリターAPI |

## ❌ 失敗したAPIの詳細

### プロンプト作成API
- **エンドポイント**: `/create_prompt`
- **エラー**: Cannot find a function with `api_name`: /create_prompt.

### プロンプト保存API
- **エンドポイント**: `/save_prompt`
- **エラー**: Cannot find a function with `api_name`: /save_prompt.

### プロンプト読み込みAPI
- **エンドポイント**: `/load_prompts`
- **エラー**: Cannot find a function with `api_name`: /load_prompts.

### レスポンス生成API
- **エンドポイント**: `/generate_response`
- **エラー**: Cannot find a function with `api_name`: /generate_response.

### 会話ログAPI
- **エンドポイント**: `/log_conversation`
- **エラー**: Cannot find a function with `api_name`: /log_conversation.

### データベースクエリAPI
- **エンドポイント**: `/execute_query`
- **エラー**: Cannot find a function with `api_name`: /execute_query.

### GitHub Issue作成API
- **エンドポイント**: `/create_issue`
- **エラー**: Cannot find a function with `api_name`: /create_issue.

### インタープリターAPI
- **エンドポイント**: `/interpret`
- **エラー**: Cannot find a function with `api_name`: /interpret.


## 💡 推奨アクション
- ⚠️ 一部のAPIで問題が発生しています
- 🔧 失敗したAPIの修正が必要です
- 📋 API一覧ページで詳細を確認してください: https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/?view=api
