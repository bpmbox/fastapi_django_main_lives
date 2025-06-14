# 🚀 FastAPI Laravel - Laravel風Python Webフレームワーク

## 📖 概要

LaravelのArtisanコマンドとMVC構造をPythonのFastAPIで再現したWebフレームワークです。
PHPのLaravelと同様の開発体験を提供し、迅速なWeb開発を可能にします。

## 🏗️ プロジェクト構造

```
fastapi_laravel/
├── app/                          # アプリケーションコア
│   ├── Console/                  # コンソールコマンド
│   │   └── Commands/            # カスタムコマンド
│   ├── Http/                    # HTTP関連
│   │   ├── Controllers/         # コントローラー
│   │   └── Middleware/          # ミドルウェア
│   ├── Models/                  # データモデル
│   └── Services/                # ビジネスロジック
├── bootstrap/                   # アプリケーション初期化
├── config/                      # 設定ファイル
├── public/                      # 静的ファイル
├── resources/                   # リソース
│   └── views/                   # テンプレート
├── routes/                      # ルーティング
│   ├── web.py                   # Web routes
│   └── api.py                   # API routes
├── artisan                      # Artisanコマンド
└── main.py                      # アプリケーションエントリーポイント
```

## 🎨 Artisanコマンド

Laravel風のコマンドラインツールを提供：

### 基本コマンド

```bash
# ヘルプ表示
./artisan --help

# 開発サーバー起動
./artisan serve
./artisan serve --port 8080 --host 127.0.0.1

# ルート一覧表示
./artisan route:list
```

### make コマンド

```bash
# コントローラー作成
./artisan make:controller UserController
./artisan make:controller PostController

# モデル作成
./artisan make:model User
./artisan make:model Post

# サービス作成
./artisan make:service UserService
./artisan make:service PostService
```

## 🚀 クイックスタート

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
pip install jinja2 python-multipart
```

### 2. 環境設定

```bash
cp .env.example .env
# .envファイルを編集
```

### 3. アプリケーション起動

```bash
# Artisanコマンドで起動
./artisan serve

# または直接起動
python main.py

# またはUvicornで起動
uvicorn main:app --reload
```

### 4. ブラウザでアクセス

- メインアプリ: http://localhost:8000
- API: http://localhost:8000/api
- API文書: http://localhost:8000/docs

## 📚 使用例

### コントローラーの作成

```bash
./artisan make:controller BlogController
```

生成されるファイル: `app/Http/Controllers/BlogController.py`

```python
class BlogController:
    def __init__(self):
        self.router = router
    
    @router.get("/")
    async def index(self) -> Dict[str, Any]:
        return {"message": "Hello from BlogController!"}
    
    @router.post("/")
    async def store(self, request: Request) -> Dict[str, Any]:
        return {"message": "Resource created successfully"}
```

### モデルの作成

```bash
./artisan make:model Post
```

生成されるファイル: `app/Models/Post.py`

```python
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### サービスの作成

```bash
./artisan make:service PostService
```

生成されるファイル: `app/Services/PostService.py`

```python
class PostService:
    async def get_all(self) -> List[Dict[str, Any]]:
        # ビジネスロジックの実装
        return []
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 作成ロジックの実装
        return {"message": "Post created successfully"}
```

## 🔧 設定

### 環境変数 (.env)

```env
APP_NAME="FastAPI Laravel"
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=sqlite
DB_DATABASE=database.sqlite

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

### 設定の取得

```python
from config.app import get_config

app_name = get_config('app.name')
debug_mode = get_config('app.debug')
db_connection = get_config('database.default')
```

## 🛣️ ルーティング

### Web Routes (`routes/web.py`)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Welcome to FastAPI Laravel"}
```

### API Routes (`routes/api.py`)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "John"}]
```

## 📦 主要機能

### ✅ 実装済み
- 🎨 Artisanコマンドライン
- 🏗️ MVC アーキテクチャ
- 🛣️ ルーティング (Web/API)
- 📄 テンプレートエンジン (Jinja2)
- ⚙️ 設定管理
- 🔧 開発サーバー
- 📚 自動API文書

### 🚧 今後の実装予定
- 🗃️ データベースマイグレーション
- 🔐 認証・認可システム
- 📧 メール送信
- 📁 ファイルストレージ
- 🧪 テストフレームワーク
- 📊 ロギングシステム

## 🤝 貢献

このプロジェクトは Laravel の素晴らしい開発体験を Python に持ち込むことを目指しています。
バグ報告、機能要求、プルリクエストを歓迎します！

## 📄 ライセンス

MIT License

---

**FastAPI Laravel** - Laravel風の開発体験をPythonで 🚀
