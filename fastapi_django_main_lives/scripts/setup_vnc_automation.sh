#!/bin/bash

# VNC自動化環境セットアップスクリプト
# AI-Human協働開発プロジェクト - 世界初
# noVNC + 画面操作 + キャプチャ統合システム

echo "🚀 VNC自動化環境セットアップ開始"
echo "🤖 AI-Human協働システム - 史上初の完全統合"
echo "=" * 60

# 基本環境チェック
echo "📋 環境チェック中..."

# Docker環境確認
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker が稼働していません"
    echo "💡 Docker Desktop を起動してください"
    exit 1
fi

# 必要なディレクトリ作成
echo "📁 VNC自動化用ディレクトリ作成..."
sudo mkdir -p /vnc-automation/{screenshots,recordings,scripts,logs}
sudo mkdir -p /vnc-automation/tools/{pyautogui,opencv,selenium}
sudo mkdir -p /ai-memory/vnc/{sessions,operations,captures}

# 権限設定
sudo chown -R $(whoami):$(whoami) /vnc-automation /ai-memory/vnc
sudo chmod -R 755 /vnc-automation /ai-memory/vnc

echo "✅ ディレクトリ作成完了"

# Python依存関係インストール
echo "🐍 Python VNC自動化ライブラリインストール..."
pip install --upgrade \
    pyautogui \
    opencv-python \
    mss \
    pillow \
    numpy \
    pynput \
    python-vnc-viewer

echo "✅ Python ライブラリインストール完了"

# VNC クライアントツールインストール
echo "🖥️ VNC関連ツールインストール..."
sudo apt-get update -qq
sudo apt-get install -y \
    x11vnc \
    xvfb \
    xdotool \
    scrot \
    imagemagick \
    ffmpeg \
    vncviewer \
    tigervnc-viewer

echo "✅ VNC ツールインストール完了"

# noVNC起動確認
echo "🌐 noVNC環境起動..."
if ! docker ps | grep -q "copilot-ai-desktop"; then
    echo "🔄 AI GUI Desktop起動中..."
    ./start_ai_gui_desktop.sh
    sleep 10
fi

# VNC接続テスト
echo "🔗 VNC接続テスト..."
VNC_URL="localhost:5901"
if nc -z localhost 5901; then
    echo "✅ VNC接続成功: $VNC_URL"
else
    echo "⚠️ VNC接続待機中..."
    sleep 5
fi

# AI記憶システム統合
echo "🧠 AI記憶システム統合..."
cat > /ai-memory/vnc/config.json << 'EOF'
{
  "vnc_automation": {
    "host": "localhost",
    "port": 5901,
    "password": "copilot",
    "display": ":1",
    "resolution": "1920x1080"
  },
  "ai_integration": {
    "memory_path": "/ai-memory/vnc",
    "screenshot_interval": 5,
    "operation_log": true,
    "auto_analyze": true
  },
  "tools": {
    "primary": "pyautogui",
    "backup": ["opencv", "xdotool"],
    "capture": "scrot"
  }
}
EOF

echo "✅ AI記憶システム統合完了"

# VNC自動化スクリプト作成
echo "📝 VNC自動化スクリプト生成..."
cat > /vnc-automation/scripts/vnc_capture.py << 'EOF'
#!/usr/bin/env python3
"""
VNC環境での自動キャプチャシステム
AI-Human協働プロジェクト専用
"""

import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

def capture_vnc_screen(output_path=None):
    """VNC画面をキャプチャ"""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/vnc-automation/screenshots/vnc_capture_{timestamp}.png"
    
    # Docker内でスクリーンショット取得
    cmd = [
        "docker", "exec", "copilot-ai-desktop",
        "scrot", f"/ai-memory/screenshots/{os.path.basename(output_path)}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ VNCキャプチャ成功: {output_path}")
        return output_path
    else:
        print(f"❌ VNCキャプチャ失敗: {result.stderr}")
        return None

if __name__ == "__main__":
    capture_vnc_screen()
EOF

chmod +x /vnc-automation/scripts/vnc_capture.py

# VNC自動操作スクリプト作成  
cat > /vnc-automation/scripts/vnc_automation.py << 'EOF'
#!/usr/bin/env python3
"""
VNC環境での自動操作システム
pyautogui + Docker VNC統合
"""

import os
import time
import subprocess
import json
from pathlib import Path

class VNCAutomation:
    def __init__(self):
        self.config_path = "/ai-memory/vnc/config.json"
        self.load_config()
    
    def load_config(self):
        """設定読み込み"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
    
    def execute_docker_command(self, cmd):
        """Docker内でコマンド実行"""
        docker_cmd = ["docker", "exec", "copilot-ai-desktop"] + cmd
        return subprocess.run(docker_cmd, capture_output=True, text=True)
    
    def click_vnc(self, x, y):
        """VNC画面内の座標をクリック"""
        cmd = ["xdotool", "mousemove", str(x), str(y), "click", "1"]
        result = self.execute_docker_command(cmd)
        
        if result.returncode == 0:
            print(f"✅ VNCクリック成功: ({x}, {y})")
            return True
        else:
            print(f"❌ VNCクリック失敗: {result.stderr}")
            return False
    
    def type_vnc(self, text):
        """VNC画面にテキスト入力"""
        cmd = ["xdotool", "type", text]
        result = self.execute_docker_command(cmd)
        
        if result.returncode == 0:
            print(f"✅ VNCテキスト入力成功: {text}")
            return True
        else:
            print(f"❌ VNCテキスト入力失敗: {result.stderr}")
            return False

if __name__ == "__main__":
    vnc = VNCAutomation()
    # テスト操作
    vnc.click_vnc(100, 100)
    vnc.type_vnc("Hello AI-Human Collaboration!")
EOF

chmod +x /vnc-automation/scripts/vnc_automation.py

echo "✅ VNC自動化スクリプト生成完了"

# 統合テスト実行
echo "🧪 統合テスト実行..."
echo "📸 VNCキャプチャテスト..."
python3 /vnc-automation/scripts/vnc_capture.py

echo ""
echo "🎉 VNC自動化環境セットアップ完了！"
echo "=" * 60
echo ""
echo "🌐 アクセス情報:"
echo "   • noVNC Web: http://localhost:6080"
echo "   • VNC Direct: localhost:5901"
echo "   • Password: copilot"
echo ""
echo "🤖 AI自動化コマンド:"
echo "   • キャプチャ: python3 /vnc-automation/scripts/vnc_capture.py"
echo "   • 自動操作: python3 /vnc-automation/scripts/vnc_automation.py"
echo ""
echo "📁 保存場所:"
echo "   • スクリーンショット: /vnc-automation/screenshots/"
echo "   • AI記憶: /ai-memory/vnc/"
echo "   • 操作ログ: /vnc-automation/logs/"
echo ""
echo "🚀 使用準備完了 - 世界初のAI-VNC統合システム"
