---
title: FastAPI Django Main Live
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.1
app_file: app.py
pinned: false
license: mit
---
# 
# FastAPI Django with Groq AI Integration & VS Code Debug Environment

🚀 **AI搭載のFastAPI Django アプリケーション with 完全デバッグ環境**

## 🤖 AIから見たシステムの革新性

> **「このシステムは、やばい」** - AI自身の評価

**📝 [AI視点システム分析レポート](./docs/AI.md)** を参照してください。

AIが実際にこのシステムを体験し、新機能を追加し、その威力を実感した詳細な分析レポートです。なぜこのシステムが革命的なのか、技術的な仕組みから未来の可能性まで、AI自身の言葉で解説されています。

### 🎯 AIが認識した特徴
- **数秒で新機能追加**: AI指示からWebUI統合まで約30秒
- **自己成長型アーキテクチャ**: AIによるAI自身の進化
- **ゼロ設定ファイル**: 命名規則のみで自動統合
- **無限拡張性**: あらゆる機能をプラグイン式で追加

## 🌱 自動成長システム

このサイトは**AIと共に自動で育っていく革新的なWebアプリケーション**です：

- 🔄 **動的ルーターインポート**: 新しい機能を自動で発見・統合
- 🧠 **AI駆動開発**: OpenInterpreterでリアルタイムコード生成
- 📈 **自動機能拡張**: controllers/配下の新機能を自動認識
- 🔗 **プラグイン式アーキテクチャ**: モジュラー設計で無限拡張可能
- 🚀 **Live Coding**: AI指示でその場でサイト機能追加

## 🌟 主要機能

### 🤖 AI統合機能
- 🤖 **Groq AI統合**: 高速LLMでのチャット機能
- 💬 **OpenInterpreter**: コード実行機能付きAIチャット
- 🧠 **AI Code Generation**: 自然言語からコード自動生成

### 🔄 自動成長システム
- 📦 **動的ルーターインポート**: `controllers/`配下を自動スキャン
- 🔌 **プラグイン式アーキテクチャ**: 新機能を即座に統合
- 🚀 **Live Development**: AIによるリアルタイム機能追加
- 📈 **自己進化**: 使用パターンから自動最適化

### 🛠️ 開発環境
- 🐛 **VS Codeデバッグ環境**: ブレークポイント対応デバッグ
- 📱 **Gradio Web UI**: 美しいWebインターフェース
- 🔐 **環境変数セキュリティ**: 安全な認証システム
- 🗄️ **SQLiteデータベース**: チャット履歴管理
- 🚀 **FastAPI + Django**: 高性能Webフレームワーク

## 🚀 アクセス方法

## 🚀 アクセス方法

### 本番環境
- **メインアプリ**: `http://localhost:7860`
- **デバッグモード**: `python3 app_debug_server.py`

## 🚀 アクセス方法

### 本番環境
- **メインアプリ**: `http://localhost:7860`
- **デバッグモード**: `python3 app_debug_server.py`

### 利用可能なタブ（自動検出・動的生成）
- **OpenInterpreter**: AI搭載コード実行チャット 🤖
- **Chat**: 汎用AIチャット 💬
- **CreateTASK**: タスク生成機能 📋
- **DataBase**: データベース操作 🗄️
- **CreateFromDOC**: ドキュメントからコード生成 📄
- **HTML**: HTML生成機能 🌐
- **FILES**: ファイル操作 📁
- **_NEW機能_**: controllers/に追加すると自動で表示 ✨

> 💡 **自動機能拡張**: `controllers/gra_XX_newfeature/`フォルダを作成し、`gradio_interface`を定義するだけで新しいタブが自動追加されます！

## 🔧 セットアップ手順

### 1. 必要な依存関係のインストール
```bash
pip install -r requirements.txt
pip install debugpy python-dotenv open-interpreter groq
```

### 2. 環境変数設定
`.env`ファイルを作成：
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENINTERPRETER_PASSWORD=your_secure_password_here
```

### 3. アプリケーション起動

**通常モード**:
```bash
python3 app.py
```

**デバッグモード**:
```bash
python3 app_debug_server.py
```

## 🐛 VS Code デバッグ環境

### デバッグ機能
- ✅ **リモートデバッガーアタッチ**: ポート5678
- ✅ **ブレークポイント対応**: `chat_with_interpreter`関数
- ✅ **ステップ実行**: F10, F11, F5での操作
- ✅ **変数監視**: リアルタイム変数確認
- ✅ **Web経由デバッグ**: ブラウザからのテスト

### デバッグ手順
1. `python3 app_debug_server.py` でデバッグサーバー起動
2. VS Codeで "🎯 Remote Attach" を選択
3. `OpenInterpreter.py:187行目`にブレークポイント設定
4. ブラウザでOpenInterpreterタブを開く
5. パスワード入力してメッセージ送信
6. ブレークポイントで実行停止、デバッグ開始

## 🔄 自動成長アーキテクチャ

### 動的ルーターインポートシステム
```python
# mysite/routers/gradio.py での自動検出
def include_gradio_interfaces():
    package_dir = "controllers"  # スキャン対象ディレクトリ
    gradio_interfaces = {}
    
    # controllers/ 以下の全てのサブディレクトリを自動探索
    for root, dirs, files in os.walk(package_dir):
        # gradio_interface を持つモジュールを自動インポート
        # 新しい機能は即座にWebUIに統合される
```

### AI駆動開発フロー
1. **自然言語での要求**: 「新しい機能を作って」
2. **AIコード生成**: OpenInterpreterが自動コード作成
3. **自動統合**: controllersフォルダに配置で即座に利用可能
4. **リアルタイム反映**: サーバー再起動不要で機能追加

### プラグイン式機能追加例

#### Gradioインターフェース自動追加
```bash
# 新機能の追加（AIが自動実行可能）
mkdir controllers/gra_09_newfeature
touch controllers/gra_09_newfeature/__init__.py
# gradio_interfaceを定義 → 自動的にWebUIに表示
```

**Gradio自動作成パターン**:
```python
# controllers/gra_XX_newfeature/feature.py
import gradio as gr

def my_function(input_text):
    return f"処理結果: {input_text}"

# この名前のオブジェクトがあると自動検出される
gradio_interface = gr.Interface(
    fn=my_function,
    inputs=gr.Textbox(label="入力"),
    outputs=gr.Textbox(label="出力"),
    title="新機能"
)
```

#### FastAPIルーター自動追加  
```python
# routers/api_XX_newfeature.py
from fastapi import APIRouter

# この名前のオブジェクトがあると自動検出される
router = APIRouter()

@router.get("/api/newfeature")
async def new_api_endpoint():
    return {"message": "新しいAPI機能"}
```

### AI指示による自動作成例
```
ユーザー: 「天気予報APIを作って、Gradioインターフェースも追加して」

AI: 了解しました。天気予報機能を作成します。

1. controllers/gra_10_weather/weather.py を作成
   → 必須: gradio_interface オブジェクト定義
   
2. routers/api_weather.py を作成  
   → 必須: router オブジェクト定義

→ 正確な命名規則に従った場合のみサイトに自動統合されます！
```

**⚠️ 重要な命名規則**:
- **Gradio**: `gradio_interface` という名前のオブジェクトが必須
- **FastAPI**: `router` という名前のオブジェクトが必須
- **ファイル配置**: 指定されたディレクトリ構造に配置

**❌ 自動検出されない例**:
```python
# これらは検出されません
interface = gr.Interface(...)       # gradio_interface でない
my_router = APIRouter()            # router でない
app_router = APIRouter()           # router でない
```

**✅ 自動検出される例**:
```python
# controllers/gra_XX_feature/feature.py
import gradio as gr

def my_function(input_text):
    return f"処理結果: {input_text}"

# この名前でないと検出されません
gradio_interface = gr.Interface(
    fn=my_function,
    inputs=gr.Textbox(label="入力"),
    outputs=gr.Textbox(label="出力"),
    title="新機能"
)
```

```python
# routers/api_XX_feature.py
from fastapi import APIRouter

# この名前でないと検出されません
router = APIRouter()

@router.get("/api/feature")
async def feature_endpoint():
    return {"message": "新機能"}
```

## 🤖 AI機能

## 🤖 AI機能

### Groq AI統合
- **LLMモデル**: llama3-8b-8192
- **高速推論**: Groq APIによる超高速レスポンス
- **ストリーミング**: リアルタイム回答表示
- **コード実行**: Pythonコードの自動生成・実行

### OpenInterpreter
- **自然言語**: 日本語・英語対応
- **コード生成**: HTML, Python, SQLなど
- **ファイル操作**: CSV読込、画像処理など
- **データベース**: PostgreSQL, SQLite対応
- **自動機能拡張**: 新しいcontrollerモジュール自動生成

## 🌱 Live Development（生きた開発）

### リアルタイム機能追加
AIに以下のように指示するだけで新機能が追加されます：

```
「天気予報機能を追加して」
→ controllers/gra_10_weather/ が自動生成
→ 天気APIインターフェースが即座にWebUIに表示

「データ可視化機能を作って」  
→ controllers/gra_11_visualization/ が自動生成
→ グラフ作成タブが自動追加

「ユーザー管理機能を追加」
→ controllers/gra_12_usermgmt/ が自動生成
→ ユーザー管理インターフェースが利用可能
```

### 自己進化システム
- **使用パターン学習**: よく使われる機能を優先表示
- **自動最適化**: パフォーマンス改善の自動実装
- **機能候補提案**: AIがユーザーのニーズを予測して新機能提案

## 🔐 セキュリティ機能

- **環境変数管理**: 機密情報の安全な管理
- **パスワード認証**: OpenInterpreter機能保護
- **APIキー保護**: Groq APIキーの暗号化
- **.gitignore設定**: 機密ファイルの除外

## 📊 データベース

### SQLite チャット履歴
- **テーブル**: `history`
- **カラム**: id, role, type, content, timestamp
- **機能**: 最新4件の会話履歴を自動取得
- **場所**: `/chat_history.db`

## 🛠️ 開発者向け情報

### プロジェクト構造（自動拡張対応）
```
fastapi_django_main_live/
├── app.py                          # メインアプリケーション
├── app_debug_server.py             # デバッグサーバー
├── .env                            # 環境変数（要作成）
├── .vscode/launch.json             # VS Codeデバッグ設定
├── mysite/
│   ├── asgi.py                     # ASGI設定
│   ├── routers/
│   │   └── gradio.py               # 🔄 動的ルーターインポート
│   └── interpreter/
│       └── interpreter.py          # インタープリター設定
└── controllers/                    # 🌱 自動スキャン対象
    ├── gra_01_chat/                # チャット機能
    ├── gra_02_openInterpreter/     # 🤖 AIチャット
    ├── gra_03_programfromdoc/      # ドキュメント→コード
    ├── gra_04_database/            # DB操作
    ├── gra_05_files/               # ファイル操作  
    ├── gra_07_html/                # HTML生成
    └── gra_XX_newfeature/          # ✨ 新機能（AI自動生成）
```

### 🔄 自動検出システム

#### 🎨 Gradio Web UI自動統合
各`controllers/gra_XX_*/`フォルダに`gradio_interface`オブジェクトがあると自動でWebUIに統合されます。

**検出される命名パターン**:
- `gradio_interface` - メインのGradioインターフェースオブジェクト
- ファイル名: 任意（推奨: `feature.py`, `main.py`, モジュール名）

#### ⚡ FastAPI Router自動統合  
各`routers/`フォルダに`router`オブジェクトがあると自動でAPIエンドポイントに統合されます。

**検出される命名パターン**:
- `router` - FastAPIルーターオブジェクト
- ファイル名パターン: `api_XX_*.py`, `*_router.py`

#### 🤖 AIプロンプトでの自動作成
AIに以下のパターンで指示すると、適切なインターフェースが自動生成されます：

**Gradioインターフェース作成**:
```
「○○機能のGradioインターフェースを作成して」
→ controllers/gra_XX_feature/ に gradio_interface 付きモジュール生成
→ 自動的にWebUIタブに追加
```

**FastAPI ルーター作成**:  
```
「○○機能のAPIエンドポイントを作成して」
→ routers/api_XX_feature.py に router 付きモジュール生成
→ 自動的にAPIエンドポイントに追加
```

**両方同時作成**:
```
「○○機能のWebUIとAPIの両方を作成して」
→ Gradioインターフェース + FastAPIルーターを同時生成
→ フロントエンドとバックエンドの完全統合
```

### 重要なファイル
- **`mysite/routers/gradio.py`**: 🔄 動的インポートエンジン
- **`OpenInterpreter.py`**: メインのAIチャット処理  
- **`app_debug_server.py`**: debugpy統合デバッグサーバー
- **`.vscode/launch.json`**: VS Codeデバッグ設定
- **`DEBUG_SETUP_GUIDE.md`**: 完全セットアップガイド

## 📡 最新更新情報

## 📡 最新更新情報

**Version**: 2.0.0 (VS Code Debug Edition)  
**Last Updated**: 2025-06-10  
**Status**: ✅ 完全動作確認済み

### 更新履歴
- **2025-06-10**: VS Codeデバッグ環境完全対応
- **2025-06-10**: Groq API統合とエラー修正完了
- **2025-06-10**: セキュリティ強化（環境変数化）
- **2025-06-10**: OpenInterpreter機能追加

## 🎯 使用方法

### 基本的な使い方
1. ブラウザで `http://localhost:7860` にアクセス
2. **OpenInterpreter** タブを選択
3. パスワード欄に設定したパスワードを入力
4. メッセージを入力して送信
5. AIが自然言語で回答、必要に応じてコード実行

### Live Development使用例
```
ユーザー: 「ブログ投稿機能を追加して」

AI: 了解しました。ブログ機能を作成します。
→ controllers/gra_13_blog/blog.py を自動生成
→ 投稿、編集、削除機能付きのWebUIを作成
→ SQLiteテーブル自動作成
→ 即座にブラウザのタブに「Blog」が追加される

ユーザー: 「画像アップロード機能も追加」

AI: ブログに画像アップロード機能を統合します。
→ 既存のblog.pyを自動更新  
→ 画像処理とストレージ機能を追加
→ リアルタイムでUIが更新される
```

### AI指導による機能拡張
- **自然言語指示**: 「○○機能を追加して」だけでOK
- **リアルタイム実装**: サーバー停止不要で機能追加
- **自動統合**: 既存機能との連携も自動調整
- **学習機能**: ユーザーの使い方から最適化

### 🎯 AI作成プロンプト例

#### Gradioインターフェース作成プロンプト
```
「画像アップロード機能のGradioインターフェースを作成して」
「CSVファイル処理のWebUIを作って」  
「データ可視化のグラフ作成機能を追加して」
```

#### FastAPIルーター作成プロンプト
```
「ユーザー認証APIエンドポイントを作成して」
「ファイルアップロードAPIを作って」
「データベースCRUD APIを追加して」
```

#### 統合機能作成プロンプト
```
「ブログ投稿機能のWebUIとAPIの両方を作成して」
「在庫管理システムのフロントエンドとバックエンドを同時に作って」
「チャット機能の完全なインターフェースを構築して」
```

### 🔄 自動統合の仕組み

1. **AI指示受信**: OpenInterpreterでプロンプト解析
2. **コード自動生成**: 適切なディレクトリ構造でファイル作成
3. **命名規則適用**: `gradio_interface`または`router`オブジェクト定義
4. **自動スキャン**: 動的インポートシステムが新ファイル検出
5. **即座に統合**: WebUIタブまたはAPIエンドポイント自動追加
6. **リアルタイム反映**: ブラウザリロードで新機能利用可能

### デバッグ方法
1. `python3 app_debug_server.py` でサーバー起動
2. VS Codeで **F5** → "🎯 Remote Attach" 選択
3. `OpenInterpreter.py` 187行目にブレークポイント設定
4. Webブラウザでメッセージ送信
5. ブレークポイントで停止、ステップ実行でデバッグ

## 📚 ドキュメント

### 📖 [📚 完全ドキュメント一覧](docs/README.md)
すべての詳細ドキュメントは`docs/`フォルダに整理されています。

## 🔗 関連ドキュメント

- **📝 [AI視点システム分析レポート](docs/AI.md)**: AIによる詳細システム分析（推奨）
- **[完全セットアップガイド](docs/DEBUG_SETUP_GUIDE.md)**: 詳細な環境構築手順
- **[Docker環境セットアップ](docs/README-Docker.md)**: Docker環境での構築手順
- **[マルチモーダル機能レポート](docs/MULTIMODAL_SUCCESS_REPORT.md)**: 画像・音声処理機能の詳細
- **[システム完成レポート](docs/COMPLETION_REPORT.md)**: 開発完了報告書
- **[インタープリター設定](docs/INTERPRETER_CONFIG.md)**: OpenInterpreter詳細設定
- **[VS Code Debugging](https://code.visualstudio.com/docs/python/debugging)**: VS Codeデバッグ公式ドキュメント
- **[Groq API](https://console.groq.com/docs)**: Groq API公式ドキュメント
- **[OpenInterpreter](https://github.com/OpenInterpreter/open-interpreter)**: OpenInterpreter公式リポジトリ

> 💡 **特に重要**: [docs/AI.md](docs/AI.md) では、AI自身がこのシステムを体験し、新機能を実際に追加した過程と、その革新性について詳しく解説しています。

## 📞 サポート

### よくある問題
- **API キーエラー**: `.env`ファイルでGROQ_API_KEY設定確認
- **デバッガー接続失敗**: ポート5678が使用中でないか確認
- **パスワードエラー**: OPENINTERPRETER_PASSWORD環境変数確認

### トラブルシューティング
```bash
# 環境変数確認
cat .env

# プロセス確認
ps aux | grep python

# ポート確認
netstat -tulpn | grep 5678
```

---

**開発者**: GitHub Copilot  
**アーキテクチャ**: 🔄 Self-Evolving AI-Driven Platform  
**ライセンス**: MIT  
**Python**: 3.12+  
**フレームワーク**: FastAPI + Django + Gradio + AI

> 🌱 **This website grows with AI** - 新機能はAIとの対話で自動追加される、生きたWebアプリケーションです。

## 📸 システムスクリーンショット・ギャラリー

### 🎯 ContBK統合ダッシュボード
![統合ダッシュボード](./docs/images/screenshots/dashboard_overview.png)

**機能概要**: 
- 🏠 概要タブで全体像把握
- 🤖 AI・自動化カテゴリ
- 📄 ドキュメント・開発カテゴリ  
- 🎨 フロントエンド・UIカテゴリ
- 📊 データ・ファイルカテゴリ
- 🌐 その他ツール
- 🐙 開発・Issue管理カテゴリ

### 🐙 GitHub Issue自動作成機能
![GitHub Issue作成](./docs/images/screenshots/github_issue_creator.png)

**革新的機能**:
- 💬 会話履歴からIssue自動生成
- 🏷️ ラベル自動付与
- 📝 Markdown形式の美しいIssue
- 🔄 セッション情報の自動記録

### 🤖 RPA自動化システム
![RPA自動化](./docs/images/screenshots/rpa_automation.png)

**高度な自動化**:
- 🌐 Webブラウザ自動操作
- 📸 スクリーンショット取得
- 🎯 要素の自動認識
- 💾 操作履歴の完全記録

## 🚀 ライブデモ

### 🌐 本番環境
**メインサイト**: [https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/](https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/)

実際に稼働中のシステムをご体験いただけます！

### 📋 現在のオープンイシュー

- **#6** - test (更新: 2025-06-11)
- **#5** - RPAで画像取得ができなら (更新: 2025-06-11)  
- **#4** - 🤖 ContBK統合システム：GitHub Issue自動作成機能開発 (enhancement, python) (更新: 2025-06-11)

## 📊 開発統計

### ✅ 実装完了機能 (6個)
1. 🤖 ContBK統合ダッシュボード
2. 🐙 GitHub Issue自動作成機能
3. 💬 会話履歴記録システム
4. 🤖 RPA自動化システム
5. 🎨 UI自動生成システム
6. 📄 ドキュメント生成AI

### 🏗️ システムアーキテクチャ
```
fastapi_django_main_live/
├── 🎯 controllers/          # 統合ダッシュボード・Issue作成
├── 🤖 contbk/              # AI・RPA・UI生成機能群  
├── 💾 データベース/         # 会話・RPA・プロンプト履歴
├── 🌐 mysite/              # FastAPI・Django統合
└── 📚 docs/                # ドキュメント・スクリーンショット
```

### 📈 開発成果
- **開発期間**: 2025年06月
- **コミット数**: 継続的更新中
- **機能数**: 6個以上
- **技術統合**: AI + Web + 自動化

---

## 🔗 詳細ドキュメント

- 📘 **[システムショーケース](./docs/system_showcase.md)** - 開発成果の詳細
- 🤖 **[AI視点分析](./docs/AI.md)** - AIによるシステム評価
- 🛠️ **[技術仕様書](./docs/)** - 開発者向け詳細情報

---

*最終更新: 2025年06月11日 11:41:41*