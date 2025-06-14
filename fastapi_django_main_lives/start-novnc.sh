#!/bin/bash

echo "=== noVNCデスクトップ環境を起動します ==="

# Docker Composeでデスクトップ環境を起動
docker compose -f docker-compose-novnc.yml up -d

echo ""
echo "🖥️  noVNCデスクトップ環境が起動中..."
echo ""
echo "📱 アクセス方法:"
echo "   ブラウザ: http://localhost:6081"
echo "   パスワード: mypassword"
echo ""
echo "🔧 VNCクライアント:"
echo "   接続先: localhost:5901"
echo "   パスワード: vncpassword"
echo ""
echo "📁 マウントされたフォルダ:"
echo "   /code (現在のプロジェクト)"
echo ""
echo "⏹️  停止方法:"
echo "   docker compose -f docker-compose-novnc.yml down"
echo ""

# ログを表示
echo "📋 起動ログを確認中..."
sleep 5
docker logs ubuntu-desktop-vnc --tail 20
