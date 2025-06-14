#!/bin/bash

# 🌐 GitHub Codespaces + Docker-in-Docker セットアップ
# 100GB永続ストレージ + AI長期記憶システム完全統合

echo "🚀 GitHub Codespaces + Docker-in-Docker 完全セットアップ"
echo "=" * 70

# 1. Docker-in-Docker有効化
echo "🐳 Docker-in-Docker有効化..."
if ! docker info > /dev/null 2>&1; then
    echo "💡 DevContainer再ビルドでDocker-in-Docker有効化が必要です"
    echo "   .devcontainer/devcontainer.json に以下を追加:"
    echo "   \"features\": { \"docker-in-docker\": {} }"
    echo "   「DevContainer: Rebuild Container」を実行してください"
else
    echo "✅ Docker稼働中"
fi

# 2. ナレッジ保管庫の場所を確認
WORKSPACE_ROOT="/workspaces/fastapi_django_main_live"
KNOWLEDGE_VAULT="$WORKSPACE_ROOT/ai-knowledge-vault"

echo "📁 ナレッジ保管庫設定: $KNOWLEDGE_VAULT"

# 3. 永続化ディレクトリ作成
mkdir -p "$KNOWLEDGE_VAULT"/{ai-memories,technical-achievements,collaboration-history,docker-volumes,world-first-evidence,backup-systems}

echo "✅ ナレッジ保管庫ディレクトリ作成完了"

# 4. Docker Compose for 永続化サービス
cat > "$KNOWLEDGE_VAULT/docker-compose.persistent.yml" << 'EOF'
version: '3.8'

services:
  ai-knowledge-db:
    image: postgres:15
    container_name: ai-knowledge-persistent
    environment:
      POSTGRES_DB: ai_knowledge_vault
      POSTGRES_USER: ai_copilot
      POSTGRES_PASSWORD: knowledge_2025
    volumes:
      - ai-db-data:/var/lib/postgresql/data
      - ./ai-memories:/ai-memories
      - ./backup-systems:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - ai-network

  ai-vector-db:
    image: pgvector/pgvector:pg15
    container_name: ai-vector-knowledge
    environment:
      POSTGRES_DB: ai_vector_knowledge
      POSTGRES_USER: ai_copilot  
      POSTGRES_PASSWORD: vector_2025
    volumes:
      - vector-db-data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    restart: unless-stopped
    networks:
      - ai-network

  ai-file-server:
    image: nginx:alpine
    container_name: ai-knowledge-fileserver
    volumes:
      - .:/usr/share/nginx/html:ro
    ports:
      - "8080:80"
    restart: unless-stopped
    networks:
      - ai-network

volumes:
  ai-db-data:
    driver: local
  vector-db-data:
    driver: local

networks:
  ai-network:
    driver: bridge
EOF

echo "✅ Docker Compose永続化設定作成完了"

# 5. GitHub Codespaces用 devcontainer.json更新
DEVCONTAINER_JSON="$WORKSPACE_ROOT/.devcontainer/devcontainer.json"

if [ -f "$DEVCONTAINER_JSON" ]; then
    echo "🔧 DevContainer設定更新..."
    
    # バックアップ作成
    cp "$DEVCONTAINER_JSON" "$DEVCONTAINER_JSON.backup"
    
    # Docker-in-Docker有効化の確認
    if grep -q "docker-in-docker" "$DEVCONTAINER_JSON"; then
        echo "✅ Docker-in-Docker設定済み"
    else
        echo "⚠️ Docker-in-Docker設定を手動で追加してください"
        echo "   \"features\": { \"docker-in-docker\": {} }"
    fi
else
    echo "📝 新しいDevContainer設定作成..."
    mkdir -p "$WORKSPACE_ROOT/.devcontainer"
    
    cat > "$DEVCONTAINER_JSON" << 'EOF'
{
    "name": "AI-Human Collaboration Workspace", 
    "image": "mcr.microsoft.com/devcontainers/python:3.11",
    "features": {
        "docker-in-docker": {},
        "git": "latest",
        "github-cli": "latest"
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-toolsai.jupyter", 
                "ms-vscode.vscode-docker",
                "GitHub.copilot"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python3"
            }
        }
    },
    "mounts": [
        "source=${localWorkspaceFolder}/ai-knowledge-vault,target=/workspace/ai-knowledge-vault,type=bind"
    ],
    "postCreateCommand": "pip install -r requirements.txt && chmod +x setup_knowledge_system.sh && ./setup_knowledge_system.sh",
    "forwardPorts": [8000, 5432, 5433, 8080],
    "remoteUser": "vscode"
}
EOF
    echo "✅ DevContainer設定作成完了"
fi

# 6. 自動起動スクリプト作成
cat > "$KNOWLEDGE_VAULT/start_persistent_services.sh" << 'EOF'
#!/bin/bash
echo "🚀 AI永続化サービス起動..."

cd "$(dirname "$0")"

# Docker Compose起動
docker-compose -f docker-compose.persistent.yml up -d

echo "✅ 永続化サービス起動完了"
echo "🌐 アクセス情報:"
echo "   - PostgreSQL: localhost:5432"
echo "   - Vector DB: localhost:5433" 
echo "   - File Server: http://localhost:8080"

# AI記憶システム初期化
python3 ../ai_long_term_memory.py --init

echo "🧠 AI長期記憶システム準備完了"
EOF

chmod +x "$KNOWLEDGE_VAULT/start_persistent_services.sh"

# 7. 自動バックアップCronスクリプト  
cat > "$KNOWLEDGE_VAULT/backup-systems/auto_backup.sh" << 'EOF'
#!/bin/bash

# AI-Human協働プロジェクト自動バックアップ
echo "🔄 AI記憶自動バックアップ開始: $(date)"

BACKUP_DIR="$(dirname "$0")/backup_$(date +'%Y%m%d_%H%M%S')"
mkdir -p "$BACKUP_DIR"

# データベースダンプ
docker exec ai-knowledge-persistent pg_dump -U ai_copilot ai_knowledge_vault > "$BACKUP_DIR/ai_knowledge_dump.sql"

# 重要ファイルコピー 
cp ../ai-memories/* "$BACKUP_DIR/" 2>/dev/null || echo "記憶ファイルなし"
cp ../../*.md "$BACKUP_DIR/" 2>/dev/null || echo "文書ファイルなし"

# Git自動コミット
cd ../..
git add ai-knowledge-vault/
git commit -m "🤖 Auto-backup: $(date)" || echo "変更なし"

echo "✅ 自動バックアップ完了: $BACKUP_DIR"
EOF

chmod +x "$KNOWLEDGE_VAULT/backup-systems/auto_backup.sh"

# 8. 使用量モニタリング
echo "📊 ストレージ使用量:"
df -h | grep -E "(Filesystem|/workspaces)"
echo ""
echo "📁 ナレッジ保管庫サイズ:"
du -sh "$KNOWLEDGE_VAULT" 2>/dev/null || echo "計算中..."

echo ""
echo "🎉 GitHub Codespaces + Docker-in-Docker セットアップ完了！"
echo "=" * 70
echo ""
echo "🔄 次のステップ:"
echo "1. DevContainer再ビルド（Docker-in-Docker有効化）"
echo "2. $KNOWLEDGE_VAULT/start_persistent_services.sh 実行"
echo "3. AI長期記憶システム初期化確認"
echo "4. 100GB永続ストレージ活用開始"
echo ""
echo "🌐 GitHub Codespaces環境で完全永続化AI協働システム準備完了！"
