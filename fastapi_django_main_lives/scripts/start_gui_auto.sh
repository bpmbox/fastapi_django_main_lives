#!/bin/bash

# AI GUI Desktop Auto-Startup Script
# This script automatically starts the GUI desktop environment

set -e

# Color codes for output
COLOR_RESET='\033[0m'
COLOR_CYAN='\033[1;36m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[1;31m'

echo -e "${COLOR_CYAN}🚀 Starting AI GUI Desktop Environment...${COLOR_RESET}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${COLOR_RED}❌ Docker is not running. Please start Docker first.${COLOR_RESET}"
    exit 1
fi

# Stop any existing GUI containers
echo -e "${COLOR_YELLOW}🛑 Stopping any existing GUI containers...${COLOR_RESET}"
docker-compose -f docker-ai-gui-desktop.yml down >/dev/null 2>&1 || true

# Start the GUI desktop environment
echo -e "${COLOR_CYAN}📦 Starting AI GUI Desktop containers...${COLOR_RESET}"
docker-compose -f docker-ai-gui-desktop.yml up -d

# Wait for services to be ready
echo -e "${COLOR_YELLOW}⏳ Waiting for services to start...${COLOR_RESET}"
sleep 10

# Check if containers are running
if docker-compose -f docker-ai-gui-desktop.yml ps | grep -q "Up"; then
    echo -e "${COLOR_GREEN}✅ AI GUI Desktop Environment is now running!${COLOR_RESET}"
    echo ""
    echo -e "${COLOR_GREEN}🌐 Access URLs:${COLOR_RESET}"
    echo -e "  🖥️  Web GUI (noVNC): ${COLOR_CYAN}http://localhost:6080${COLOR_RESET}"
    echo -e "  🔗 VNC Direct:       ${COLOR_CYAN}localhost:5901${COLOR_RESET}"
    echo -e "  🗄️  Database:         ${COLOR_CYAN}localhost:5432${COLOR_RESET}"
    echo ""
    echo -e "${COLOR_GREEN}🔑 Default Credentials:${COLOR_RESET}"
    echo -e "  👤 Username: ${COLOR_CYAN}copilot${COLOR_RESET}"
    echo -e "  🔒 Password: ${COLOR_CYAN}copilot${COLOR_RESET}"
    echo ""
    echo -e "${COLOR_YELLOW}💡 Tip: Open http://localhost:6080 in your browser to access the desktop${COLOR_RESET}"
    
    # Auto-open browser if available
    if command -v "$BROWSER" >/dev/null 2>&1; then
        echo -e "${COLOR_CYAN}🚀 Opening GUI in browser...${COLOR_RESET}"
        "$BROWSER" "http://localhost:6080" >/dev/null 2>&1 &
    fi
else
    echo -e "${COLOR_RED}❌ Failed to start GUI Desktop Environment${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}📋 Container status:${COLOR_RESET}"
    docker-compose -f docker-ai-gui-desktop.yml ps
    exit 1
fi
