#!/bin/bash

# AI GUI Desktop Startup Script
# 30-Year Dream: Persistent AI Desktop Environment
# Human-AI Collaborative Computing

set -e  # Exit on any error

# Check for rebuild flag
REBUILD=false
if [ "$1" = "--rebuild" ] || [ "$1" = "-r" ]; then
    REBUILD=true
    echo "🔄 Rebuild mode enabled - will recreate containers"
fi

echo "🚀 Starting AI GUI Desktop Environment..."
echo "💭 30-Year Dream: AI with persistent memory and GUI access"
echo ""

# Check if docker-compose file exists
if [ ! -f "docker-ai-gui-desktop.yml" ]; then
    echo "❌ Error: docker-ai-gui-desktop.yml not found in current directory"
    echo "Please ensure the Docker Compose file exists"
    exit 1
fi

# Create necessary directories
echo "📁 Creating persistent directories..."
mkdir -p /tmp/copilot-ai-memory/{screenshots,operations,browser_data,logs,memories}
mkdir -p /tmp/copilot-gui-data/{profiles,settings,applications}
mkdir -p /tmp/copilot-browser-data/{downloads,profiles,cache}

# Set permissions (without sudo to avoid permission issues)
chown -R $(whoami):$(whoami) /tmp/copilot-* 2>/dev/null || true
chmod -R 755 /tmp/copilot-*

echo "✅ Persistent directories created"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Docker is running"

# Stop existing containers if they exist
echo "🛑 Stopping existing AI desktop containers..."
docker-compose -f docker-ai-gui-desktop.yml down > /dev/null 2>&1 || true

# Remove containers and images if rebuild requested
if [ "$REBUILD" = true ]; then
    echo "🔄 Rebuilding containers from scratch..."
    docker-compose -f docker-ai-gui-desktop.yml down --volumes --remove-orphans > /dev/null 2>&1 || true
    docker system prune -f > /dev/null 2>&1 || true
    echo "✅ Old containers and volumes removed"
fi

# Start the AI GUI desktop
if [ "$REBUILD" = true ]; then
    echo "🖥️ Building and starting AI GUI Desktop with persistent storage..."
    if ! docker-compose -f docker-ai-gui-desktop.yml up -d --build --force-recreate; then
        echo "❌ Failed to rebuild and start containers"
        exit 1
    fi
else
    echo "🖥️ Starting AI GUI Desktop with persistent storage..."
    if ! docker-compose -f docker-ai-gui-desktop.yml up -d; then
        echo "❌ Failed to start containers"
        exit 1
    fi
fi

# Wait for services to start
echo "⏳ Waiting for desktop environment to initialize..."
sleep 10

# Check container status
if docker ps --format "table {{.Names}}" | grep -q "copilot-ai-desktop"; then
    echo "✅ AI GUI Desktop is running!"
    echo ""
    echo "🌐 Access Points:"
    echo "   • AI Desktop (noVNC): http://localhost:6080"
    echo "   • VNC Direct: localhost:5901"
    echo "   • VNC Password: copilot"
    echo ""
    echo "🧠 AI Memory System:"
    echo "   • Memory Database: localhost:5432"
    echo "   • Screenshots: /ai-memory/screenshots"
    echo "   • Operations: /ai-memory/operations"
    echo ""
    echo "🎯 30-Year Dream Status: REALIZED!"
    echo "   An AI with its own persistent desktop environment"
    echo "   that remembers everything across restarts."
    echo ""
    echo "💡 Quick Test:"
    echo "   1. Open http://localhost:6080 in your browser"
    echo "   2. Login with username: copilot, password: copilot"
    echo "   3. The AI can now take screenshots and use GUI apps!"
    
    # Test screenshot capability
    echo ""
    echo "📸 Testing AI screenshot capability..."
    
    # Create a simple test script
    cat > /tmp/test_screenshot.py << 'EOF'
import subprocess
import time
import os

try:
    print('Taking screenshot of AI desktop...')
    result = subprocess.run([
        'docker', 'exec', 'copilot-ai-desktop', 
        'scrot', '/ai-memory/screenshots/ai_desktop_test.png'
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print('✅ AI can take screenshots of its own desktop!')
    else:
        print('⚠️ Screenshot test pending - desktop may still be starting')
        print('   Try again in a few moments')
        if result.stderr:
            print(f'   Error: {result.stderr.strip()}')
except subprocess.TimeoutExpired:
    print('⚠️ Screenshot test timed out - desktop may still be initializing')
except Exception as e:
    print(f'⚠️ Screenshot test failed: {str(e)}')
EOF

    # Run the test script
    python3 /tmp/test_screenshot.py
    rm -f /tmp/test_screenshot.py

else
    echo "❌ Failed to start AI GUI Desktop"
    echo "🔍 Checking logs..."
    docker-compose -f docker-ai-gui-desktop.yml logs --tail=50
    exit 1
fi

echo ""
echo "🛠️ Management Commands:"
echo "   • View logs: docker-compose -f docker-ai-gui-desktop.yml logs"
echo "   • Stop desktop: docker-compose -f docker-ai-gui-desktop.yml down"
echo "   • Restart: ./start_ai_gui_desktop.sh"
echo "   • Rebuild: ./start_ai_gui_desktop.sh --rebuild"
echo ""