#!/usr/bin/env python3
"""
noVNC Desktop Automation Script
noVNC環境での画面操作・ブラウザ自動化スクリプト
"""

import time
import subprocess
import os
import pyautogui
import cv2
import numpy as np
from PIL import Image
import json

class DesktopAutomation:
    def __init__(self):
        # PyAutoGUIの設定
        pyautogui.PAUSE = 0.5  # 操作間の待機時間
        pyautogui.FAILSAFE = True  # フェイルセーフ機能
        
    def take_screenshot(self, filename="/tmp/screenshot.png"):
        """スクリーンショットを撮影"""
        try:
            # X11のスクリーンショット
            result = subprocess.run([
                "import", "-window", "root", filename
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ スクリーンショット保存: {filename}")
                return filename
            else:
                print(f"❌ スクリーンショット失敗: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ スクリーンショット例外: {e}")
            return None
    
    def get_screen_size(self):
        """画面サイズを取得"""
        try:
            result = subprocess.run([
                "xdpyinfo", "|", "grep", "dimensions"
            ], shell=True, capture_output=True, text=True)
            
            # 例: dimensions:    1024x768 pixels (270x203 millimeters)
            if "dimensions" in result.stdout:
                line = result.stdout.strip()
                # 正規表現で幅x高さを抽出
                import re
                match = re.search(r'(\d+)x(\d+)', line)
                if match:
                    width, height = int(match.group(1)), int(match.group(2))
                    print(f"🖥️ 画面サイズ: {width}x{height}")
                    return width, height
            
            # デフォルト値
            return 1024, 768
        except:
            return 1024, 768
    
    def click(self, x, y, button="left"):
        """指定座標をクリック"""
        try:
            click_map = {"left": "1", "right": "3", "middle": "2"}
            button_num = click_map.get(button, "1")
            
            result = subprocess.run([
                "xdotool", "mousemove", str(x), str(y), "click", button_num
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🖱️ クリック: ({x}, {y}) {button}ボタン")
                return True
            else:
                print(f"❌ クリック失敗: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ クリック例外: {e}")
            return False
    
    def double_click(self, x, y):
        """ダブルクリック"""
        return self.click(x, y) and self.click(x, y)
    
    def type_text(self, text):
        """テキストを入力"""
        try:
            result = subprocess.run([
                "xdotool", "type", text
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"⌨️ テキスト入力: '{text}'")
                return True
            else:
                print(f"❌ テキスト入力失敗: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ テキスト入力例外: {e}")
            return False
    
    def key_press(self, key):
        """キーを押す"""
        try:
            result = subprocess.run([
                "xdotool", "key", key
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🔑 キー押下: {key}")
                return True
            else:
                print(f"❌ キー押下失敗: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ キー押下例外: {e}")
            return False
    
    def scroll(self, x, y, direction="up", clicks=3):
        """スクロール"""
        try:
            scroll_map = {"up": "4", "down": "5"}
            button = scroll_map.get(direction, "4")
            
            # 指定座標に移動してスクロール
            subprocess.run(["xdotool", "mousemove", str(x), str(y)])
            
            for _ in range(clicks):
                result = subprocess.run([
                    "xdotool", "click", button
                ], capture_output=True, text=True)
            
            print(f"🔄 スクロール: ({x}, {y}) {direction} {clicks}回")
            return True
        except Exception as e:
            print(f"❌ スクロール例外: {e}")
            return False
    
    def drag(self, x1, y1, x2, y2):
        """ドラッグ操作"""
        try:
            result = subprocess.run([
                "xdotool", "mousemove", str(x1), str(y1),
                "mousedown", "1",
                "mousemove", str(x2), str(y2),
                "mouseup", "1"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🎯 ドラッグ: ({x1}, {y1}) → ({x2}, {y2})")
                return True
            else:
                print(f"❌ ドラッグ失敗: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ ドラッグ例外: {e}")
            return False
    
    def find_text_on_screen(self, text, screenshot_path="/tmp/screenshot.png"):
        """画面上でテキストを検索（簡易版）"""
        # まずスクリーンショットを撮影
        if not self.take_screenshot(screenshot_path):
            return None
        
        # ここでOCRライブラリ（例：tesseract）を使用することもできます
        # 今回は簡単な実装として座標を返すだけ
        print(f"🔍 テキスト検索: '{text}' (OCR機能は未実装)")
        return None
    
    def wait_for_image(self, image_path, timeout=10):
        """画像が画面に表示されるまで待機"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            screenshot_path = "/tmp/current_screen.png"
            if self.take_screenshot(screenshot_path):
                # OpenCVで画像マッチング（簡易版）
                print(f"🔍 画像待機: {image_path}")
                time.sleep(1)
        return False
    
    def get_window_list(self):
        """ウィンドウリストを取得"""
        try:
            result = subprocess.run([
                "xdotool", "search", "--name", "."
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                windows = result.stdout.strip().split('\n')
                print(f"🪟 ウィンドウ数: {len(windows)}")
                return windows
            return []
        except Exception as e:
            print(f"❌ ウィンドウリスト取得例外: {e}")
            return []
    
    def activate_window(self, window_id):
        """ウィンドウをアクティブにする"""
        try:
            result = subprocess.run([
                "xdotool", "windowactivate", str(window_id)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🪟 ウィンドウアクティブ: {window_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ ウィンドウアクティブ例外: {e}")
            return False
    
    def execute_command(self, command):
        """コマンドを実行"""
        try:
            # Alt+F2でランダイアログを開く（Ubuntu/GNOME）
            self.key_press("alt+F2")
            time.sleep(1)
            
            # コマンドを入力
            self.type_text(command)
            time.sleep(0.5)
            
            # Enterで実行
            self.key_press("Return")
            
            print(f"🚀 コマンド実行: {command}")
            return True
        except Exception as e:
            print(f"❌ コマンド実行例外: {e}")
            return False
    
    def open_application(self, app_name):
        """アプリケーションを開く"""
        applications = {
            "terminal": "gnome-terminal",
            "firefox": "firefox",
            "chrome": "google-chrome",
            "file-manager": "nautilus",
            "text-editor": "gedit",
            "calculator": "gnome-calculator"
        }
        
        command = applications.get(app_name.lower(), app_name)
        return self.execute_command(command)
    
    def get_mouse_position(self):
        """マウス座標を取得"""
        try:
            result = subprocess.run([
                "xdotool", "getmouselocation"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # 例: x:100 y:200 screen:0 window:12345
                output = result.stdout.strip()
                import re
                x_match = re.search(r'x:(\d+)', output)
                y_match = re.search(r'y:(\d+)', output)
                
                if x_match and y_match:
                    x, y = int(x_match.group(1)), int(y_match.group(1))
                    return x, y
            return None, None
        except Exception as e:
            print(f"❌ マウス座標取得例外: {e}")
            return None, None
    
    def setup_novnc_environment(self):
        """noVNC環境のセットアップ"""
        try:
            # 必要なパッケージのインストール確認
            packages = ["selenium", "requests", "beautifulsoup4"]
            for package in packages:
                try:
                    __import__(package.replace("-", "_"))
                    print(f"✅ {package} インストール済み")
                except ImportError:
                    print(f"📦 {package} をインストール中...")
                    subprocess.run(["pip3", "install", package], check=True)
            
            # ディスプレイ環境変数設定
            os.environ['DISPLAY'] = ':1'
            print("🖥️ Display環境を :1 に設定")
            
            # スクリーンショットディレクトリ作成
            os.makedirs("/code/screenshots", exist_ok=True)
            print("📁 スクリーンショットディレクトリ作成完了")
            
            return True
        except Exception as e:
            print(f"❌ 環境セットアップ失敗: {e}")
            return False
    
    def browser_automation(self, url="https://www.google.com"):
        """ブラウザ自動化"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            
            # Chromeオプション設定
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--display=:1")
            chrome_options.add_argument("--window-size=1920,1080")
            
            print("🌐 ブラウザを起動中...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            print(f"📄 ページタイトル: {driver.title}")
            
            # スクリーンショット撮影
            screenshot_path = "/code/screenshots/browser_automation.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 ブラウザスクリーンショット保存: {screenshot_path}")
            
            # 簡単な操作例
            if "google" in url.lower():
                try:
                    search_box = driver.find_element(By.NAME, "q")
                    search_box.send_keys("noVNC automation test")
                    search_box.submit()
                    time.sleep(3)
                    
                    # 検索結果のスクリーンショット
                    driver.save_screenshot("/code/screenshots/search_result.png")
                    print("🔍 Google検索を実行しました")
                except Exception as e:
                    print(f"⚠️ 検索操作スキップ: {e}")
            
            time.sleep(2)
            driver.quit()
            print("✅ ブラウザ自動化完了")
            
        except Exception as e:
            print(f"❌ ブラウザ自動化失敗: {e}")
    
    def gui_automation_demo(self):
        """GUI操作のデモンストレーション"""
        try:
            print("🖱️ GUI自動化デモを開始...")
            
            # 画面サイズ取得
            screen_width, screen_height = pyautogui.size()
            print(f"📐 画面サイズ: {screen_width}x{screen_height}")
            
            # マウス操作
            print("🖱️ マウスを画面中央に移動...")
            pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=1)
            
            # 右クリックメニュー表示
            pyautogui.rightClick()
            time.sleep(1)
            pyautogui.press('escape')  # メニューを閉じる
            
            # ターミナルを開く（Ctrl+Alt+T）
            print("💻 ターミナルを開いています...")
            pyautogui.hotkey('ctrl', 'alt', 't')
            time.sleep(2)
            
            # コマンド入力
            pyautogui.typewrite('echo "Hello from noVNC automation!"')
            pyautogui.press('enter')
            time.sleep(1)
            
            # スクリーンショット撮影
            self.take_screenshot("/code/screenshots/gui_demo.png")
            
            # ターミナルを閉じる
            pyautogui.hotkey('alt', 'f4')
            
            print("✅ GUI自動化デモ完了")
            
        except Exception as e:
            print(f"❌ GUI自動化失敗: {e}")
    
    def web_scraping_demo(self):
        """Webスクレイピングのデモ"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            print("🕷️ Webスクレイピングデモを開始...")
            
            # 簡単なWebページを取得
            response = requests.get("https://httpbin.org/html")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # タイトルを取得
            title = soup.find('title').text if soup.find('title') else "No title"
            print(f"📄 取得したページタイトル: {title}")
            
            # 結果をファイルに保存
            with open("/code/screenshots/scraping_result.txt", "w") as f:
                f.write(f"タイトル: {title}\n")
                f.write(f"取得時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"HTMLコンテンツ:\n{soup.prettify()}")
            
            print("📁 スクレイピング結果を保存しました")
            
        except Exception as e:
            print(f"❌ Webスクレイピング失敗: {e}")

def demo_automation():
    """デモンストレーション実行"""
    print("🚀 noVNC Desktop Automation デモを開始します")
    
    desktop = DesktopAutomation()
    
    # noVNC環境のセットアップ
    if not desktop.setup_novnc_environment():
        print("❌ 環境セットアップに失敗しました")
        return
    
    print("\n📋 実行するタスクを選択してください:")
    print("1. スクリーンショット撮影")
    print("2. ブラウザ自動化")
    print("3. GUI操作デモ")
    print("4. Webスクレイピングデモ")
    print("5. 全て実行")
    print("6. 既存のVNC操作デモ")
    
    choice = input("\n選択 (1-6): ").strip()
    
    if choice == "1":
        desktop.take_screenshot("/code/screenshots/manual_screenshot.png")
    elif choice == "2":
        desktop.browser_automation()
    elif choice == "3":
        desktop.gui_automation_demo()
    elif choice == "4":
        desktop.web_scraping_demo()
    elif choice == "5":
        # 全て実行
        desktop.take_screenshot("/code/screenshots/start_screenshot.png")
        time.sleep(2)
        desktop.browser_automation()
        time.sleep(2)
        desktop.gui_automation_demo()
        time.sleep(2)
        desktop.web_scraping_demo()
        time.sleep(2)
        desktop.take_screenshot("/code/screenshots/end_screenshot.png")
    elif choice == "6":
        # 既存のVNC操作デモ
        run_existing_vnc_demo(desktop)
    else:
        print("❌ 無効な選択です")

def run_existing_vnc_demo(desktop):
    """既存のVNC操作デモを実行"""
    print("🖥️ 既存のVNC操作デモを実行します...")
    
    # 1. スクリーンショット撮影
    desktop.take_screenshot("/code/screenshots/vnc_demo_start.png")
    
    # 2. 画面サイズ取得
    width, height = desktop.get_screen_size()
    if width and height:
        print(f"📐 画面サイズ: {width}x{height}")
    
    # 3. 画面中央をクリック
    center_x, center_y = width // 2, height // 2
    desktop.click(center_x, center_y)
    
    # 4. 現在のマウス位置を取得
    mouse_x, mouse_y = desktop.get_mouse_position()
    if mouse_x and mouse_y:
        print(f"🖱️ マウス位置: ({mouse_x}, {mouse_y})")
    
    # 5. テストテキスト入力
    time.sleep(1)
    desktop.type_text("Hello from noVNC AI! こんにちは！")
    
    # 6. キー操作のテスト
    time.sleep(1)
    desktop.key_press("ctrl+a")  # 全選択
    time.sleep(0.5)
    desktop.key_press("Delete")  # 削除
    
    # 7. アプリケーション起動テスト
    desktop.open_application("terminal")
    
    time.sleep(2)
    desktop.take_screenshot("/code/screenshots/vnc_demo_end.png")
    print("✅ VNCデモンストレーション完了！")


if __name__ == "__main__":
    demo_automation()
