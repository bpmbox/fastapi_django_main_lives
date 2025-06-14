#!/bin/bash

echo "🔄 FastAPI Django Main Live - Post Start Setup..."
echo "🧠 AI GUI System - PostStart Initialization"

# Ensure Rust is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Set environment variables for GUI
export DISPLAY=:1
export XVFB_RES=1920x1080x24

# Check if all dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "
try:
    import gradio
    import fastapi
    import open_interpreter
    import sqlite3
    print('✅ All core dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Run: pip install -r requirements.txt')
"

# Start GUI services - Using Persistent Docker Desktop
echo "🖥️ Initializing AI Persistent GUI Desktop..."

# Check if docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker is available - Starting persistent GUI environment..."
    
    # Start the persistent GUI environment
    if [ -f "ai_persistent_gui_manager.py" ]; then
        echo "🚀 Starting AI Persistent GUI Manager..."
        python3 ai_persistent_gui_manager.py &
        sleep 5
    else
        echo "⚠️ AI Persistent GUI Manager not found, using fallback method..."
        
        # Fallback: Direct docker-compose
        if [ -f "docker-compose-persistent-gui.yml" ]; then
            echo "🐳 Starting GUI with docker-compose..."
            docker-compose -f docker-compose-persistent-gui.yml up -d
            sleep 5
        fi
    fi
else
    echo "⚠️ Docker not available, using local GUI services..."
    
    # Fallback to local GUI services
    # Check if X server is running
    if ! pgrep -x "Xvfb" > /dev/null; then
        echo "🖥️ Starting Xvfb..."
        Xvfb :1 -screen 0 1920x1080x24 &
        sleep 2
    fi

    # Check if desktop environment is running
    if ! pgrep -x "fluxbox" > /dev/null; then
        echo "🖥️ Starting Fluxbox desktop..."
        DISPLAY=:1 fluxbox &
        sleep 2
    fi

    # Try to start VNC and noVNC
    if ! pgrep -x "x11vnc" > /dev/null; then
        echo "📺 Starting VNC server..."
        DISPLAY=:1 x11vnc -display :1 -forever -passwd copilot -rfbport 5901 -shared -bg
        sleep 2
    fi
    
    # Try websockify for noVNC
    if ! pgrep -f "websockify" > /dev/null && command -v websockify &> /dev/null; then
        echo "🌐 Starting noVNC with websockify..."
        websockify --web=/usr/share/novnc/ 6080 localhost:5901 &
        sleep 2
    fi
fi

# Restore AI memory
echo "🧠 Restoring AI Memory..."

# Check if AI memory restoration script exists
if [ -f "ai_memory_restoration.py" ]; then
    echo "🧠 Running AI memory restoration..."
    python3 ai_memory_restoration.py
else
    echo "⚠️ AI memory restoration script not found"
fi

# Initialize AI memory system
echo "🧠 Initializing AI Memory System..."
python3 -c "
from ai_memory_system import ai_memory
print('🧠 AI Memory System Status:')
print(ai_memory.generate_memory_summary())
" 2>/dev/null || echo "⚠️ AI Memory System not yet available"

# Create directories for AI operations
echo "📁 Setting up AI directories..."
mkdir -p /ai-memory/screenshots
mkdir -p /ai-memory/downloads
mkdir -p /ai-memory/temp
mkdir -p /gui-data/profiles
mkdir -p /browser-data/downloads

# Set permissions
chmod -R 755 /ai-memory 2>/dev/null || true
chmod -R 755 /gui-data 2>/dev/null || true
chmod -R 755 /browser-data 2>/dev/null || true

# Start browser environment
echo "🌐 Checking browser environment..."
if [ ! -f "/browser-data/.browser-initialized" ]; then
    echo "🌐 Initializing browser environment..."
    mkdir -p /browser-data/firefox-profile
    touch /browser-data/.browser-initialized
fi

# Display helpful information
echo ""
echo "🚀 FastAPI Django Main Live is ready!"
echo "✅ AI GUI System startup complete!"
echo ""
echo "📱 Available services:"
echo "  • Main App: http://localhost:7860"
echo "  • Test Manager: http://localhost:7861" 
echo "  • Debug Port: 5678"
echo "  • AI GUI Desktop (Persistent): http://localhost:6081"
echo "  • AI GUI Desktop (Fallback): http://localhost:6080"
echo "  • VNC Direct Access: localhost:5902 (Persistent) / localhost:5901 (Fallback)"
echo ""
echo "🛠️ Quick commands:"
echo "  • Start main app: python3 app.py"
echo "  • Start debug mode: python3 app_debug_server.py"
echo "  • Test prompt manager: python3 test_prompt_manager.py"
echo "  • Test AI GUI system: python3 ai_gui_system.py"
echo ""
echo "📊 System Status:"
echo "   - X Server: $(pgrep -x Xvfb > /dev/null && echo '✅ Running' || echo '❌ Not running')"
echo "   - Desktop: $(pgrep -x fluxbox > /dev/null && echo '✅ Running' || echo '❌ Not running')"
echo "   - noVNC: $(pgrep -f novnc > /dev/null && echo '✅ Running' || echo '❌ Not running')"
echo "   - AI Memory: $([ -d '/ai-memory' ] && echo '✅ Available' || echo '❌ Not available')"
echo ""
echo "🔐 VNC Password: copilot"
echo "🎯 30-Year Dream Status: SYSTEM READY FOR AI GUI AUTOMATION!"
echo ""
