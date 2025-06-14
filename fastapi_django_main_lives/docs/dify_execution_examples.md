# 🔧 Dify環境セットアップ実行例

## クイックスタート実行例

### 1. 環境確認
```bash
# 現在のディレクトリ確認
pwd
# /workspaces/fastapi_django_main_live

# Docker動作確認
docker --version
docker info
```

### 2. Dify起動（ワンライナー）
```bash
cd /workspaces/fastapi_django_main_live/dify-setup/dify/docker && docker compose up -d
```

### 3. 起動確認
```bash
# コンテナ状態確認
docker ps

# Webアクセス確認
curl -I http://localhost
```

### 4. 並行してapp.py起動
```bash
cd /workspaces/fastapi_django_main_live && python app.py &
```

## 📊 期待される結果

### Docker PSコマンド出力例
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED       STATUS       PORTS                                   NAMES
abc123def456   dify/dify-api:latest    "python app.py"          2 min ago     Up 2 min     0.0.0.0:5001->5001/tcp                 dify-api
def456ghi789   nginx:latest            "/docker-entrypoint.…"   2 min ago     Up 2 min     0.0.0.0:80->80/tcp,443->443/tcp        nginx
...
```

### HTTPレスポンス例
```
HTTP/1.1 307 Temporary Redirect
Server: nginx/1.27.5
Date: Fri, 13 Jun 2025 11:41:21 GMT
Connection: keep-alive
location: /apps
```

## 🎯 アクセス方法

### Web UI
- **URL**: `http://localhost`
- **リダイレクト**: 自動的に `/apps` にリダイレクト
- **初期設定**: ブラウザでアクセス後、管理者アカウント作成

### API エンドポイント
- **API Base**: `http://localhost/v1`
- **API Docs**: `http://localhost/docs`
- **Health Check**: `http://localhost/health`

## 🔄 停止・再起動方法

### 停止
```bash
cd /workspaces/fastapi_django_main_live/dify-setup/dify/docker
docker compose down
```

### 再起動
```bash
cd /workspaces/fastapi_django_main_live/dify-setup/dify/docker
docker compose restart
```

### ログ確認
```bash
cd /workspaces/fastapi_django_main_live/dify-setup/dify/docker
docker compose logs -f
```

## 🚨 トラブルシューティング

### よくある問題
1. **ポート競合**: `docker compose down` で停止後再起動
2. **メモリ不足**: `docker system prune` でクリーンアップ
3. **権限エラー**: `sudo` 追加（DevContainerでは通常不要）

### ヘルスチェック
```bash
# 全サービス状態確認
docker compose ps

# 特定サービスログ確認
docker compose logs dify-api
docker compose logs nginx
```
