#!/bin/bash

echo "🚀 Starting Copilot GUI-Enhanced RPA System"
echo "=" * 50

# Check if running in DevContainer
if [ ! -f /.dockerenv ]; then
    echo "⚠️ This script should run in DevContainer"
    echo "💡 Use: DevContainer: Rebuild and Reopen in Container"
    exit 1
fi

# Start VNC and noVNC
echo "🖥️ Starting GUI Environment..."
/usr/local/bin/start-vnc.sh &

# Wait for VNC to start
sleep 5

# Start Gradio app
echo "🎨 Starting Gradio Application..."
cd /workspace
python app.py &

# Wait for app to start
sleep 10

# Run GUI RPA test
echo "🤖 Running Copilot GUI RPA Test..."
python copilot_gui_rpa.py

echo "✅ System Ready!"
echo ""
echo "🌐 Access Points:"
echo "  - noVNC GUI:    http://localhost:6080"
echo "  - Gradio App:   http://localhost:7860"
echo "  - VNC Direct:   localhost:5901"
echo ""
echo "🔑 VNC Password: copilot123"
echo "📁 GUI Workspace: /workspace/gui-workspace"
echo ""
echo "🎮 In noVNC, you can:"
echo "  - See real-time browser automation"
echo "  - Interact with desktop environment"
echo "  - Watch Playwright in action"
echo "  - Control GUI applications"
