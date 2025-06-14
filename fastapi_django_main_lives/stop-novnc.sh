#!/bin/bash

echo "⏹️  noVNCデスクトップ環境を停止します"

# コンテナを停止
docker compose -f docker-compose-novnc.yml down

echo "🧹 リソースをクリーンアップしています..."

# 不要なボリュームを削除（オプション）
read -p "ボリュームも削除しますか? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker compose -f docker-compose-novnc.yml down -v
    echo "💾 ボリュームも削除しました"
fi

# 未使用のDockerリソースをクリーンアップ（オプション）
read -p "未使用のDockerイメージ・ネットワークを削除しますか? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker system prune -f
    echo "🗑️  未使用リソースを削除しました"
fi

echo "✅ noVNC環境の停止が完了しました"
