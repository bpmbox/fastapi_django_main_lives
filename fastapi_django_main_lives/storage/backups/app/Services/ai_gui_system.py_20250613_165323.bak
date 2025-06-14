#!/usr/bin/env python3
"""
🖥️ AI GUI操作システム
===================

GitHub CopilotがnoVNC経由でGUIデスクトップを操作
記憶システムと連携して操作履歴を保存
"""

import asyncio
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, Any
import json

# Playwright インポート（GUI環境用）
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# AI記憶システム
from ai_memory_system import save_gui_memory, save_ai_learning

class AIGUISystem:
    """AI GUI操作システム"""化Docker GUI環境対応）"""
    
    def __init__(self, vnc_url: str = "http://localhost:6080"):use_persistent_container: bool = True):
        self.vnc_url = vnc_url
        self.screenshot_dir = Path("/gui-data/screenshots")ainer
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        self.browser_data_dir = Path("/browser-data")
        self.browser_data_dir.mkdir(parents=True, exist_ok=True)
            self.screenshot_dir = Path("/ai-memory/screenshots")
        print(f"🖥️ AI GUI システム初期化")Path("/browser-data")
        print(f"   VNC URL: {self.vnc_url}")ata")
        print(f"   スクリーンショット: {self.screenshot_dir}")
            self.screenshot_dir = Path("/gui-data/screenshots")
    async def start_browser_session(self) -> tuple:data")
        """ブラウザセッションを開始"""dir = Path("/gui-data")
        if not PLAYWRIGHT_AVAILABLE:
        # ディレクトリ作成
        for directory in [self.screenshot_dir, self.browser_data_dir, self.gui_data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"🖥️ AI GUI システム初期化（永続化対応）")
        print(f"   VNC URL: {self.vnc_url}")
        print(f"   永続化コンテナ: {use_persistent_container}")
        print(f"   スクリーンショット: {self.screenshot_dir}")
        print(f"   ブラウザデータ: {self.browser_data_dir}")
    
    async def start_browser_session(self) -> tuple:
        """ブラウザセッションを開始"""
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Playwright が利用できません")
            return None, None
        
        try:
            playwright = await async_playwright().start()
            
            # Chromiumを起動（永続化データを使用）
            browser = await playwright.chromium.launch(
                headless=False,  # GUI環境なのでheadful
                user_data_dir=str(self.browser_data_dir / "chromium_profile"),
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ]
            )
            
            print("✅ ブラウザ起動成功")
            return playwright, browser
            
        except Exception as e:
            print(f"❌ ブラウザ起動エラー: {e}")
            return None, None
    
    async def capture_desktop_screenshot(self, description: str = "") -> str:
        """デスクトップ全体のスクリーンショットを撮影"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshot_dir / f"desktop_{timestamp}.png"
            
            # スクリーンショット撮影（GUI環境用）
            cmd = ["import", "-window", "root", str(screenshot_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"📸 デスクトップキャプチャ成功: {screenshot_path.name}")
                
                # 記憶に保存
                save_gui_memory(
                    action_type="desktop_screenshot",
                    screenshot_path=str(screenshot_path),
                    success=True,
                    notes=description
                )
                
                return str(screenshot_path)
            else:
                print(f"❌ スクリーンショット失敗: {result.stderr}")
                return ""
                
        except Exception as e:
            print(f"❌ スクリーンショットエラー: {e}")
            return ""
    
    async def open_url_in_browser(self, url: str) -> tuple:
        """指定URLをブラウザで開く"""
        playwright, browser = await self.start_browser_session()
        if not browser:
            return None, "ブラウザ起動失敗"
        
        try:
            # 新しいページを作成
            page = await browser.new_page()
            
            # URLに移動
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)  # 読み込み待機
            
            # ページのスクリーンショット
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshot_dir / f"browser_{timestamp}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            
            print(f"🌐 ブラウザでURL開く成功: {url}")
            
            # 記憶に保存
            save_gui_memory(
                action_type="open_url",
                target_url=url,
                screenshot_path=str(screenshot_path),
                success=True
            )
            
            return page, str(screenshot_path)
            
        except Exception as e:
            error_msg = f"URL読み込みエラー: {e}"
            print(f"❌ {error_msg}")
            
            save_gui_memory(
                action_type="open_url",
                target_url=url,
                success=False,
                notes=error_msg
            )
            
            return None, error_msg
    
    async def interact_with_element(self, page, selector: str, 
                                  action: str = "click", text: str = None) -> bool:
        """ページ要素との相互作用"""
        try:
            # 要素が存在するまで待機
            await page.wait_for_selector(selector, timeout=10000)
            
            if action == "click":
                await page.click(selector)
                print(f"🖱️ クリック成功: {selector}")
                
            elif action == "type" and text:
                await page.fill(selector, text)
                print(f"⌨️ テキスト入力成功: {selector}")
                
            elif action == "scroll":
                await page.evaluate(f"""
                    document.querySelector('{selector}').scrollIntoView();
                """)
                print(f"📜 スクロール成功: {selector}")
            
            # 操作後のスクリーンショット
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshot_dir / f"interaction_{timestamp}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            
            # 記憶に保存
            save_gui_memory(
                action_type=f"interact_{action}",
                selector=selector,
                action_data={"text": text} if text else None,
                screenshot_path=str(screenshot_path),
                success=True
            )
            
            return True
            
        except Exception as e:
            print(f"❌ 要素操作エラー ({action}): {e}")
            
            save_gui_memory(
                action_type=f"interact_{action}",
                selector=selector,
                success=False,
                notes=str(e)
            )
            
            return False
    
    async def analyze_page_content(self, page) -> Dict[str, Any]:
        """ページ内容を分析"""
        try:
            # ページ情報取得
            title = await page.title()
            url = page.url
            
            # エラー要素をチェック
            error_elements = await page.query_selector_all('[class*="error"], [class*="Error"], .alert-danger')
            has_errors = len(error_elements) > 0
            
            # Gradio特有の要素をチェック
            gradio_elements = await page.query_selector_all('.gradio-container, .gr-interface')
            is_gradio = len(gradio_elements) > 0
            
            # フォーム要素の数
            input_count = len(await page.query_selector_all('input, textarea'))
            button_count = len(await page.query_selector_all('button'))
            
            analysis = {
                "title": title,
                "url": url,
                "has_errors": has_errors,
                "is_gradio": is_gradio,
                "input_count": input_count,
                "button_count": button_count,
                "timestamp": datetime.now().isoformat()
            }
            
            # 学習データとして保存
            save_ai_learning("page_analysis", analysis)
            
            print(f"🔍 ページ分析完了: {title}")
            return analysis
            
        except Exception as e:
            print(f"❌ ページ分析エラー: {e}")
            return {"error": str(e)}
    
    def setup_gui_environment(self):
        """GUI環境をセットアップ"""
        try:
            print("🔧 GUI環境セットアップ中...")
            
            # 必要なパッケージをインストール
            packages = [
                "firefox",
                "chromium-browser", 
                "imagemagick",
                "scrot",
                "xvfb",
                "fluxbox"
            ]
            
            for package in packages:
                cmd = ["apt-get", "install", "-y", package]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {package} インストール完了")
                else:
                    print(f"⚠️ {package} インストール失敗: {result.stderr}")
            
            # Playwrightブラウザをインストール
            if PLAYWRIGHT_AVAILABLE:
                cmd = ["playwright", "install", "chromium"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Playwright Chromium インストール完了")
                else:
                    print(f"⚠️ Playwright インストール失敗: {result.stderr}")
            
            print("✅ GUI環境セットアップ完了")
            
        except Exception as e:
            print(f"❌ GUI環境セットアップエラー: {e}")
    
    async def run_automated_task(self, task_description: str, target_url: str) -> str:
        """自動化タスクを実行"""
        print(f"🤖 自動化タスク開始: {task_description}")
        print(f"   対象URL: {target_url}")
        
        # ブラウザでURLを開く
        page, screenshot_path = await self.open_url_in_browser(target_url)
        if not page:
            return "❌ ブラウザでのURL読み込み失敗"
        
        # ページ内容を分析
        analysis = await self.analyze_page_content(page)
        
        # デスクトップスクリーンショットも撮影
        desktop_screenshot = await self.capture_desktop_screenshot(
            f"自動化タスク: {task_description}"
        )
        
        # 結果をまとめる
        result = f"""
🤖 **自動化タスク完了**

📋 **タスク**: {task_description}
🌐 **URL**: {target_url}
📸 **ブラウザスクリーンショット**: {screenshot_path}
🖥️ **デスクトップスクリーンショット**: {desktop_screenshot}

🔍 **ページ分析結果**:
- タイトル: {analysis.get('title', 'N/A')}
- Gradioアプリ: {'はい' if analysis.get('is_gradio') else 'いいえ'}
- エラー検出: {'はい' if analysis.get('has_errors') else 'いいえ'}
- 入力要素: {analysis.get('input_count', 0)}個
- ボタン要素: {analysis.get('button_count', 0)}個
"""
        
        # ブラウザを閉じる
        try:
            await page.close()
            await page.context.browser.close()
        except:
            pass
        
        print("✅ 自動化タスク完了")
        return result

# グローバルGUIシステム
ai_gui = AIGUISystem()

async def gui_open_url(url: str) -> str:
    """便利関数: URLを開いてスクリーンショット"""
    page, screenshot = await ai_gui.open_url_in_browser(url)
    if page:
        await page.close()
        return f"✅ URLを開きました: {screenshot}"
    else:
        return f"❌ URL読み込み失敗: {url}"

async def gui_automated_task(description: str, url: str) -> str:
    """便利関数: 自動化タスクを実行"""
    return await ai_gui.run_automated_task(description, url)

def gui_setup():
    """便利関数: GUI環境セットアップ"""
    ai_gui.setup_gui_environment()

if __name__ == "__main__":
    # テスト実行
    async def test_gui_system():
        print("🖥️ AI GUI システム テスト")
        print("=" * 50)
        
        # GUI環境セットアップ
        gui_setup()
        
        # 自動化タスクをテスト
        result = await gui_automated_task(
            "Gradioアプリの動作確認とスクリーンショット",
            "http://localhost:7860"
        )
        
        print(result)
    
    asyncio.run(test_gui_system())
