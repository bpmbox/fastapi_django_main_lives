#!/bin/bash

echo "🔧 Setting up GUI Environment for GitHub Copilot..."

# Install additional Python packages
pip install --upgrade gradio playwright fastapi uvicorn

# Create GUI workspace directories
mkdir -p /workspace/gui-workspace
mkdir -p /workspace/gui-workspace/screenshots
mkdir -p /workspace/gui-workspace/recordings

# Setup Playwright
echo "🎭 Installing Playwright browsers..."
playwright install chromium firefox webkit
playwright install-deps

# Create GUI RPA Test Script
cat > /workspace/gui-workspace/gui_rpa_test.py << 'EOF'
#!/usr/bin/env python3
"""
🖥️ GUI Environment RPA Test for GitHub Copilot
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class CopilotGUITest:
    def __init__(self):
        self.screenshots_dir = Path("/workspace/gui-workspace/screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
    async def test_gui_environment(self):
        """GUI環境での自動テスト"""
        print("🤖 Copilot GUI Environment Test Starting...")
        
        async with async_playwright() as p:
            # Launch browser in GUI mode
            browser = await p.chromium.launch(
                headless=False,  # GUI表示
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--display=:1'
                ]
            )
            
            page = await browser.new_page()
            
            # Test local Gradio app
            try:
                await page.goto('http://localhost:7860')
                await page.wait_for_timeout(3000)
                
                # Take screenshot
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_path = self.screenshots_dir / f"gui_test_{timestamp}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                
                print(f"✅ Screenshot saved: {screenshot_path}")
                
                # Test interactions
                await self.test_gradio_interactions(page)
                
            except Exception as e:
                print(f"❌ Test error: {e}")
                
            await browser.close()
            
    async def test_gradio_interactions(self, page):
        """Gradio interface interactions"""
        try:
            # Click tabs, buttons, etc.
            tabs = await page.query_selector_all('.tab-nav button')
            for i, tab in enumerate(tabs[:3]):  # Test first 3 tabs
                await tab.click()
                await page.wait_for_timeout(1000)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_path = self.screenshots_dir / f"tab_{i}_{timestamp}.png"
                await page.screenshot(path=screenshot_path)
                print(f"📸 Tab {i} screenshot: {screenshot_path}")
                
        except Exception as e:
            print(f"⚠️ Interaction test error: {e}")

if __name__ == "__main__":
    tester = CopilotGUITest()
    asyncio.run(tester.test_gui_environment())
EOF

chmod +x /workspace/gui-workspace/gui_rpa_test.py

# Create desktop shortcut for Copilot workspace
mkdir -p /home/vscode/Desktop
cat > /home/vscode/Desktop/Copilot-Workspace.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Copilot RPA Workspace
Comment=GitHub Copilot GUI Environment
Exec=code /workspace
Icon=code
Terminal=false
Categories=Development;
EOF

chmod +x /home/vscode/Desktop/Copilot-Workspace.desktop

echo "✅ GUI Environment Setup Complete!"
echo "🌐 Access via: http://localhost:6080"
echo "🔑 VNC Password: copilot123"
echo "📁 GUI Workspace: /workspace/gui-workspace"
