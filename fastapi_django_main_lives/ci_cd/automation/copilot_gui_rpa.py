#!/usr/bin/env python3
"""
🖥️ Copilot GUI-Enhanced RPA System
=====================================

GitHub Copilot専用のGUI環境でのRPA機能
- noVNC経由でのリアルタイム操作確認
- GUI環境でのPlaywright実行
- 自分専用デスクトップでのブラウザ操作
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess
import os

# Add workspace to path
sys.path.append('/workspace')

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class CopilotGUIRPA:
    """GitHub Copilot専用GUI-RPA System"""
    
    def __init__(self):
        self.gui_workspace = Path("/workspace/gui-workspace")
        self.screenshots_dir = self.gui_workspace / "screenshots"
        self.recordings_dir = self.gui_workspace / "recordings"
        
        # Create directories
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        
        # GUI Environment check
        self.display = os.environ.get('DISPLAY', ':1')
        
    def check_gui_environment(self):
        """GUI環境の確認"""
        checks = {
            'display': self.display,
            'vnc_running': self._check_vnc(),
            'novnc_running': self._check_novnc(),
            'playwright': PLAYWRIGHT_AVAILABLE,
            'browser_available': self._check_browsers()
        }
        
        print("🖥️ GUI Environment Status:")
        for key, value in checks.items():
            status = "✅" if value else "❌"
            print(f"  {status} {key}: {value}")
            
        return all(checks.values())
    
    def _check_vnc(self):
        """VNC server check"""
        try:
            result = subprocess.run(['pgrep', 'Xvnc'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _check_novnc(self):
        """noVNC check"""
        try:
            result = subprocess.run(['pgrep', 'websockify'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _check_browsers(self):
        """Browser availability check"""
        try:
            result = subprocess.run(['which', 'chromium'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    async def start_gui_rpa_session(self, target_url="http://localhost:7860"):
        """GUI環境でのRPAセッション開始"""
        print(f"🚀 Starting Copilot GUI RPA Session...")
        print(f"🎯 Target: {target_url}")
        print(f"🖥️ Display: {self.display}")
        
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Playwright not available")
            return False
            
        async with async_playwright() as p:
            # Launch browser in GUI mode (visible)
            browser = await p.chromium.launch(
                headless=False,  # GUI表示で実行
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    f'--display={self.display}',
                    '--disable-gpu',
                    '--no-first-run'
                ]
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='CopilotGUI-RPA/1.0'
            )
            
            page = await context.new_page()
            
            try:
                # Navigate to target
                print(f"🌐 Navigating to {target_url}...")
                await page.goto(target_url, wait_until='networkidle')
                
                # Wait for page load
                await page.wait_for_timeout(3000)
                
                # Take initial screenshot
                await self._take_gui_screenshot(page, "initial")
                
                # Perform GUI interactions
                await self._perform_gui_interactions(page)
                
                # Take final screenshot
                await self._take_gui_screenshot(page, "final")
                
                print("✅ GUI RPA Session completed successfully")
                return True
                
            except Exception as e:
                print(f"❌ GUI RPA Session error: {e}")
                return False
                
            finally:
                await browser.close()
    
    async def _take_gui_screenshot(self, page, suffix=""):
        """GUI環境でのスクリーンショット"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"copilot_gui_{suffix}_{timestamp}.png"
        screenshot_path = self.screenshots_dir / filename
        
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 GUI Screenshot: {screenshot_path}")
        
        # Also save metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'display': self.display,
            'url': page.url,
            'title': await page.title(),
            'viewport': await page.evaluate('() => ({width: window.innerWidth, height: window.innerHeight})'),
            'screenshot_path': str(screenshot_path)
        }
        
        metadata_path = screenshot_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
        return screenshot_path
    
    async def _perform_gui_interactions(self, page):
        """GUI環境でのインタラクション"""
        print("🎮 Performing GUI interactions...")
        
        try:
            # Check for Gradio tabs
            tabs = await page.query_selector_all('.tab-nav button')
            print(f"📑 Found {len(tabs)} tabs")
            
            # Click through tabs with visible feedback
            for i, tab in enumerate(tabs[:5]):  # Limit to first 5 tabs
                print(f"🖱️ Clicking tab {i+1}...")
                await tab.click()
                await page.wait_for_timeout(2000)  # Wait for UI update
                
                # Take screenshot of each tab
                await self._take_gui_screenshot(page, f"tab_{i+1}")
                
            # Look for buttons and interactive elements
            buttons = await page.query_selector_all('button')
            print(f"🔘 Found {len(buttons)} buttons")
            
            # Try some safe interactions
            for i, button in enumerate(buttons[:3]):
                try:
                    button_text = await button.inner_text()
                    if any(safe_word in button_text.lower() for safe_word in ['refresh', 'load', 'test', 'demo']):
                        print(f"🖱️ Clicking safe button: {button_text}")
                        await button.click()
                        await page.wait_for_timeout(1000)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Interaction error: {e}")
    
    def generate_gui_report(self):
        """GUI操作レポート生成"""
        screenshots = list(self.screenshots_dir.glob("*.png"))
        
        report = f"""# 🖥️ Copilot GUI RPA Report

## 📊 Session Summary
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Environment**: GUI Desktop with noVNC
- **Display**: {self.display}
- **Screenshots**: {len(screenshots)} captured

## 📸 Screenshots Captured
"""
        
        for screenshot in sorted(screenshots):
            metadata_file = screenshot.with_suffix('.json')
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                report += f"""
### {screenshot.name}
- **URL**: {metadata.get('url', 'N/A')}
- **Title**: {metadata.get('title', 'N/A')}
- **Timestamp**: {metadata.get('timestamp', 'N/A')}
- **Viewport**: {metadata.get('viewport', 'N/A')}
"""
        
        report += f"""
## 🌐 Access Information
- **noVNC URL**: http://localhost:6080
- **VNC Direct**: localhost:5901
- **Password**: copilot123

## 🚀 Next Steps
1. Open noVNC in browser
2. Watch real-time GUI operations
3. Interact with desktop environment
4. Run more complex RPA scenarios
"""
        
        report_path = self.gui_workspace / f"gui_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📋 GUI Report saved: {report_path}")
        return report_path

async def main():
    """Main GUI RPA execution"""
    rpa = CopilotGUIRPA()
    
    print("🤖 GitHub Copilot GUI-Enhanced RPA System")
    print("=" * 50)
    
    # Check environment
    if not rpa.check_gui_environment():
        print("❌ GUI environment not ready")
        print("💡 Start with: docker-compose -f docker-compose-gui.yml up")
        return
    
    # Run GUI RPA session
    success = await rpa.start_gui_rpa_session()
    
    # Generate report
    rpa.generate_gui_report()
    
    if success:
        print("\n🎉 Copilot GUI RPA Session Complete!")
        print("🌐 Check noVNC: http://localhost:6080")
        print("📁 Screenshots: /workspace/gui-workspace/screenshots")
    else:
        print("\n❌ GUI RPA Session failed")

if __name__ == "__main__":
    asyncio.run(main())
