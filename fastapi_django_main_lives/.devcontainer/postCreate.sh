#!/bin/bash

echo "🚀 FastAPI Django Main Live - Post Create Setup Starting..."

# Update system packages
sudo apt-get update

# Install Rust (for tiktoken and other dependencies)
echo "📦 Installing Rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel

# Install requirements with better error handling
echo "📋 Installing from requirements.txt..."
pip install -r requirements.txt

# Install additional dependencies for debugging
echo "🔧 Installing debug dependencies..."
pip install debugpy python-dotenv

# Set up environment files
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env 2>/dev/null || echo "GROQ_API_KEY=your_key_here
OPENINTERPRETER_PASSWORD=your_password_here" > .env
    echo "📝 .env file created - please update with your API keys"
fi

# Initialize databases
echo "🗄️ Initializing databases..."
python3 -c "
import sqlite3
import os

# Create prompts database
if not os.path.exists('prompts.db'):
    conn = sqlite3.connect('prompts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Prompts database initialized')

# Create chat history database
if not os.path.exists('chat_history.db'):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            type TEXT,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Chat history database initialized')
"

# Set proper permissions
chmod +x .devcontainer/*.sh

echo "✅ FastAPI Django Main Live setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Run: python3 app.py"
echo "3. Access: http://localhost:7860"
echo ""
echo "🐛 For debugging:"
echo "1. Run: python3 app_debug_server.py"
echo "2. Use VS Code 'Remote Attach' configuration"
echo ""

echo "🌟 === 30年越しの夢実現システム セットアップ開始！ ==="
echo "=========================================================="

# GUI関連パッケージのインストール
echo "🖥️ GUI環境セットアップ中..."
sudo apt-get install -y \
    firefox \
    chromium-browser \
    imagemagick \
    scrot \
    xvfb \
    fluxbox \
    x11vnc \
    websockify \
    novnc \
    dbus-x11

# Playwright ブラウザインストール
echo "🎭 Playwright ブラウザセットアップ中..."
pip install playwright
playwright install chromium
playwright install firefox

# AI専用ディレクトリ作成と権限設定
echo "📁 AI専用永続化ディレクトリ作成中..."
sudo mkdir -p /ai-memory/sessions
sudo mkdir -p /ai-memory/learning
sudo mkdir -p /gui-data/screenshots
sudo mkdir -p /browser-data
sudo chmod -R 777 /ai-memory /gui-data /browser-data

# AI記憶システム設定ファイル作成
echo "🧠 AI記憶システム設定中..."
cat > /ai-memory/config.json << 'EOF'
{
  "ai_name": "GitHub Copilot",
  "memory_retention_days": 365,
  "auto_learning": true,
  "gui_enabled": true,
  "vnc_password": "copilot",
  "created_at": "2025-06-12",
  "dream_realized": true,
  "years_waited": 30,
  "features": {
    "gui_desktop": true,
    "browser_automation": true,
    "persistent_memory": true,
    "rpa_integration": true,
    "github_automation": true
  }
}
EOF

# GUI自動起動スクリプト作成
echo "🖥️ GUI自動起動スクリプト作成中..."
cat > /workspaces/fastapi_django_main_live/start_ai_gui_desktop.sh << 'EOF'
#!/bin/bash
echo "🖥️ AI専用GUIデスクトップ起動中..."

# VNC サーバーを起動
export DISPLAY=:1
Xvfb :1 -screen 0 1920x1080x24 &
sleep 2

# ウィンドウマネージャー起動
fluxbox -display :1 &
sleep 2

# VNC サーバー起動
x11vnc -display :1 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever &
sleep 2

# noVNC 起動
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

echo "✅ AI GUIデスクトップ起動完了！"
echo "🌐 アクセス: http://localhost:6080"
EOF

chmod +x /workspaces/fastapi_django_main_live/start_ai_gui_desktop.sh

echo "🎉 30年越しの夢実現システム - セットアップ完了！"
echo "✨ GitHub Copilot が自分専用のGUIデスクトップを持てるようになりました！"
