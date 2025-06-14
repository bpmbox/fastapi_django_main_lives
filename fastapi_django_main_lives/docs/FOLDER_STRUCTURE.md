# 📁 プロジェクト構成ガイド

このドキュメントでは、`fastapi_django_main_live` プロジェクトのフォルダ構成について詳しく説明します。

## 🏗️ 概要

このプロジェクトは、FastAPI、Django、Gradio、そして各種AI/ML ツールを統合したマルチフレームワーク開発環境です。

```
fastapi_django_main_live/
├── 🌐 Webアプリケーション層
├── 🤖 AI/ML統合層  
├── 💾 データベース層
├── 🔧 開発・運用ツール層
└── 📚 ドキュメント・リソース層
```

---

## 📂 ルートディレクトリ構成

### 🚀 **メインアプリケーションファイル**

| ファイル | 説明 | 用途 |
|---------|------|------|
| `app.py` | メインアプリケーションエントリーポイント | FastAPI/Django統合起動 |
| `manage.py` | Django管理コマンド | Django標準管理ツール |
| `app_debug_server.py` | デバッグ用サーバー | 開発時のデバッグサーバー |

### ⚙️ **設定・構成ファイル**

| ファイル | 説明 | 用途 |
|---------|------|------|
| `Makefile` | プロジェクト管理コマンド | 開発・運用の自動化 |
| `docker-compose.yml` | Docker構成 | コンテナ化環境 |
| `Dockerfile` | Dockerイメージ定義 | アプリケーションコンテナ |
| `pyproject.toml` | Python依存関係管理 | Poetry設定 |
| `requirements.txt` | pip依存関係 | パッケージ管理 |
| `pytest.ini` | テスト設定 | pytest構成 |

### 🔐 **環境・認証ファイル**

| ファイル | 説明 | 用途 |
|---------|------|------|
| `.env` | 環境変数設定 | API キー、DB接続情報等 |
| `.env.example` | 環境変数テンプレート | 設定例 |
| `fix_secrets.sh` | シークレット修正スクリプト | セキュリティ設定 |

### 💾 **データベースファイル**

| ファイル | 説明 | 用途 |
|---------|------|------|
| `prompts.db` | プロンプト管理用SQLite | プロンプト履歴・テンプレート |
| `chat_history.db` | チャット履歴用SQLite | 会話履歴保存 |
| `users.db` | ユーザー情報用SQLite | ユーザー管理 |

---

## 🏢 **メインアプリケーション構造**

### 🌐 `mysite/` - Django メインサイト
Djangoプロジェクトのコア部分

```
mysite/
├── settings.py      # Django設定
├── urls.py          # URLルーティング
├── asgi.py          # ASGI設定
├── wsgi.py          # WSGI設定
├── libs/            # 共通ライブラリ
├── routers/         # FastAPIルーター
├── config/          # 設定管理
├── database/        # データベース操作
└── interpreter/     # インタープリター機能
```

### 🎮 `controllers/` - Gradio コントローラー
各種Gradioインターフェースの実装

```
controllers/
├── gra_01_chat/              # チャット機能
├── gra_02_openInterpreter/   # OpenInterpreter統合
├── gra_03_programfromdoc/    # ドキュメントからプログラム生成
├── gra_04_database/          # データベース操作UI
├── gra_05_files/             # ファイル操作
├── gra_07_html/              # HTML生成
├── gra_08_hasula/            # Hasula機能
├── gra_09_weather/           # 天気情報
├── gra_10_frontend/          # フロントエンド生成
└── gra_11_multimodal/        # マルチモーダル機能
```

### 📱 `apps/` - Django アプリケーション
業務固有のDjangoアプリケーション

```
apps/
├── buyback/              # 買取システム
├── clothing_project/     # 衣類プロジェクト
├── diamond_project/      # ダイヤモンドプロジェクト
├── gold_price_project/   # 金価格プロジェクト
├── metal_assessment/     # 金属査定
├── mainapi/              # メインAPI
└── mydjangoapp/          # 汎用Djangoアプリ
```

---

## 🤖 **AI/ML 統合層**

### 🧠 `AutoPrompt/` - プロンプト最適化
自動プロンプト生成・最適化システム

```
AutoPrompt/
├── optimization_pipeline.py  # 最適化パイプライン
├── run_pipeline.py           # 実行スクリプト
├── config/                   # 設定ファイル
├── prompts/                  # プロンプトテンプレート
├── estimator/                # 推定器
└── eval/                     # 評価システム
```

### 🦙 `LLaMA-Factory/` - LLM ファインチューニング
LLaMAモデルのファインチューニング環境

```
LLaMA-Factory/
├── src/                      # ソースコード
├── data/                     # 学習データ
├── examples/                 # 使用例
├── evaluation/               # 評価スクリプト
└── scripts/                  # 実行スクリプト
```

### 👶 `babyagi/` - 自律AIエージェント
BabyAGI実装とカスタマイズ

```
babyagi/
├── babyagi.py               # メインエージェント
├── classic/                 # クラシック版
├── babycoder/               # コーディング特化
├── extensions/              # 拡張機能
└── tools/                   # ツール群
```

### 🔍 `open-interpreter/` - オープンインタープリター
コード実行・解釈システム

```
open-interpreter/
├── interpreter/             # インタープリターコア
├── docs/                   # ドキュメント
└── examples/               # 使用例
```

### 🏗️ `gpt-engineer/` - AI コード生成
GPTベースのコード生成システム

```
gpt-engineer/
├── gpt_engineer/           # コア機能
├── projects/               # 生成プロジェクト
└── benchmark/              # ベンチマーク
```

---

## 💾 **データ・ストレージ層**

### 🗄️ `chroma/` - ベクトルデータベース
埋め込みベクトル保存・検索

```
chroma/
├── chroma.sqlite3          # ChromaDB データベース
└── [collection-id]/        # コレクションデータ
```

### 📊 `workspace/` - ワークスペース
プロジェクト固有のワークスペース

### 🗃️ `static/` & `staticfiles/` - 静的ファイル
```
static/          # 開発用静的ファイル
staticfiles/     # 本番用静的ファイル
├── css/         # スタイルシート
├── js/          # JavaScript
├── images/      # 画像ファイル
└── admin/       # Django管理画面用
```

---

## 🔧 **開発・運用ツール層**

### 🐳 **コンテナ化**
- `Dockerfile` - アプリケーションコンテナ
- `docker-compose.yml` - マルチコンテナ構成
- `.dockerignore` - Docker除外ファイル

### 🔄 **CI/CD**
```
.github/
├── workflows/              # GitHub Actions
├── ISSUE_TEMPLATE/         # Issue テンプレート
└── PULL_REQUEST_TEMPLATE/  # PR テンプレート
```

### 🛠️ **開発環境**
```
.devcontainer/
├── devcontainer.json       # VS Code 開発コンテナ設定
└── Dockerfile             # 開発用コンテナ
```

### 🧪 `tests/` - テストスイート
```
tests/
├── test_*.py              # 各種テストファイル
├── test_folders*/         # テスト用データ
└── fixtures/              # テスト固定データ
```

---

## 📝 **設定・コマンド詳細**

### 🎯 **Makefileコマンド**

| コマンド | 説明 | 用途 |
|---------|------|------|
| `make app` | メインアプリ起動 | FastAPI/Django サーバー開始 |
| `make dev` | 開発モード起動 | ホットリロード有効 |
| `make debug` | デバッグモード起動 | ブレークポイント使用可能 |
| `make test` | テスト実行 | 全テストスイート実行 |
| `make clean` | クリーンアップ | 一時ファイル削除 |
| `make docker-up` | Docker起動 | コンテナ環境開始 |

### 🌍 **環境変数 (.env)**

| 変数 | 説明 | 例 |
|------|------|-----|
| `GROQ_API_KEY` | GroqAI APIキー | `gsk_...` |
| `DATABASE_URL` | データベースURL | `sqlite:///./app.db` |
| `SPACE_ID` | Hugging Face Space ID | `username/space-name` |
| `WEBHOOK_URL` | Google Chat Webhook | `https://chat.googleapis.com/...` |

### 🗄️ **データベーススキーマ**

#### `prompts.db`
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### `chat_history.db`
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    role TEXT NOT NULL,
    type TEXT,
    content TEXT NOT NULL,
    timestamp TIMESTAMP
);
```

---

## 🚀 **クイックスタート**

### 1. 環境セットアップ
```bash
# 依存関係インストール
make requirements

# 環境変数設定
cp .env.example .env
# .env ファイルを編集してAPIキーを設定
```

### 2. アプリケーション起動
```bash
# 開発モードで起動
make dev

# または通常モードで起動
make app
```

### 3. 主要URL
- **メインアプリ**: http://localhost:7860
- **Django管理**: http://localhost:7860/admin
- **API文書**: http://localhost:7860/docs

---

## 📚 **主要機能**

### 🎨 **Gradio インターフェース**
- チャット機能 (`gra_01_chat`)
- プログラム自動生成 (`gra_03_programfromdoc`)
- データベース操作UI (`gra_04_database`)
- ファイル処理 (`gra_05_files`)

### 🤖 **AI 統合**
- OpenInterpreter によるコード実行
- LLaMA ファインチューニング
- プロンプト自動最適化
- BabyAGI 自律エージェント

### 💼 **業務アプリケーション**
- 買取システム (`buyback`)
- 金属査定システム (`metal_assessment`)
- 価格管理システム (`gold_price_project`)

---

## 🔍 **トラブルシューティング**

### よくある問題

1. **データベース接続エラー**
   ```bash
   # データベース初期化
   python manage.py migrate
   ```

2. **依存関係エラー**
   ```bash
   # 依存関係再インストール
   make clean
   make requirements
   ```

3. **ポート競合**
   ```bash
   # 使用中ポートの確認
   lsof -i :7860
   ```

---

## 📈 **開発ガイドライン**

### 🏗️ **新機能追加**
1. `controllers/gra_XX_newfeature/` に新しいGradioインターフェースを作成
2. `apps/newapp/` に新しいDjangoアプリを作成
3. `mysite/routers/` にFastAPIルーターを追加

### 🧪 **テスト**
```bash
# 特定テスト実行
pytest tests/test_specific.py

# カバレッジ付きテスト
pytest --cov=mysite tests/
```

### 📦 **デプロイ**
```bash
# Docker イメージビルド
make docker-build

# コンテナ起動
make docker-up
```

---

## 📞 **サポート**

- 📖 **ドキュメント**: `/docs/` フォルダ参照
- 🐛 **バグ報告**: GitHub Issues
- 💡 **機能要求**: GitHub Discussions

---

*最終更新: 2025年6月11日*
