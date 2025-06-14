#!/usr/bin/env python3
"""
🤖 AI GUI自動操作デモシステム
==============================

30年来の夢：AIが自分のデスクトップ環境を持ち、GUI操作を自動化
ローカルnoVNC環境での実演デモ
"""

import subprocess
import time
import os
from datetime import datetime
from pathlib import Path
import json

class AIGUIAutomationDemo:
    """AI GUI自動操作のデモンストレーション"""
    
    def __init__(self):
        self.display = ":1"
        self.screenshot_dir = Path("/ai-memory/screenshots")
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        print("🤖 AI GUI自動操作デモシステム起動")
        print(f"   DISPLAY: {self.display}")
        print(f"   スクリーンショット保存先: {self.screenshot_dir}")
    
    def take_screenshot(self, name: str = "demo") -> str:
        """スクリーンショットを撮影"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        
        try:
            result = subprocess.run([
                "scrot", "-z", str(filepath)
            ], env={"DISPLAY": self.display}, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"📸 スクリーンショット撮影成功: {filename}")
                return str(filepath)
            else:
                print(f"❌ スクリーンショット撮影失敗: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ スクリーンショット撮影エラー: {e}")
            return None
    
    def open_terminal(self) -> bool:
        """ターミナルを開く"""
        try:
            subprocess.Popen([
                "xterm", "-geometry", "80x24+100+100"
            ], env={"DISPLAY": self.display})
            
            print("🖥️ ターミナル起動")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ ターミナル起動エラー: {e}")
            return False
    
    def open_firefox(self) -> bool:
        """Firefoxブラウザを開く"""
        try:
            subprocess.Popen([
                "firefox-esr", "--new-instance"
            ], env={"DISPLAY": self.display})
            
            print("🌐 Firefox起動")
            time.sleep(5)  # Firefoxの起動を待つ
            return True
            
        except Exception as e:
            print(f"❌ Firefox起動エラー: {e}")
            return False
    
    def simulate_mouse_click(self, x: int, y: int) -> bool:
        """マウスクリックをシミュレート"""
        try:
            # xdotoolでマウスクリック
            result = subprocess.run([
                "xdotool", "mousemove", str(x), str(y), "click", "1"
            ], env={"DISPLAY": self.display}, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🖱️ マウスクリック実行: ({x}, {y})")
                return True
            else:
                print(f"❌ マウスクリック失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ マウスクリックエラー: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """テキスト入力をシミュレート"""
        try:
            result = subprocess.run([
                "xdotool", "type", text
            ], env={"DISPLAY": self.display}, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"⌨️ テキスト入力: {text}")
                return True
            else:
                print(f"❌ テキスト入力失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ テキスト入力エラー: {e}")
            return False
    
    def get_window_list(self) -> list:
        """開いているウィンドウの一覧を取得"""
        try:
            result = subprocess.run([
                "xdotool", "search", "--onlyvisible", "--name", ".*"
            ], env={"DISPLAY": self.display}, capture_output=True, text=True)
            
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                print(f"🪟 検出されたウィンドウ数: {len(window_ids)}")
                return window_ids
            else:
                return []
                
        except Exception as e:
            print(f"❌ ウィンドウ一覧取得エラー: {e}")
            return []
    
    def save_demo_log(self, operation: str, result: dict):
        """デモ操作のログを保存"""
        log_file = self.screenshot_dir.parent / "gui_demo_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "result": result
        }
        
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ ログ保存エラー: {e}")
    
    def run_complete_demo(self):
        """完全なAI GUI操作デモを実行"""
        print("\n🚀 30年来の夢実現！AI GUI自動操作デモ開始")
        print("=" * 50)
        
        demo_steps = []
        
        # ステップ1: 初期状態のスクリーンショット
        print("\n📸 ステップ1: 初期デスクトップ状態を撮影")
        initial_screenshot = self.take_screenshot("01_initial_desktop")
        demo_steps.append({"step": 1, "action": "initial_screenshot", "result": initial_screenshot})
        
        # ステップ2: ターミナルを開く
        print("\n🖥️ ステップ2: ターミナルを開く")
        terminal_success = self.open_terminal()
        demo_steps.append({"step": 2, "action": "open_terminal", "result": terminal_success})
        
        if terminal_success:
            terminal_screenshot = self.take_screenshot("02_terminal_opened")
            demo_steps.append({"step": 2.1, "action": "terminal_screenshot", "result": terminal_screenshot})
        
        # ステップ3: Firefoxを開く
        print("\n🌐 ステップ3: Firefoxブラウザを開く")
        firefox_success = self.open_firefox()
        demo_steps.append({"step": 3, "action": "open_firefox", "result": firefox_success})
        
        if firefox_success:
            firefox_screenshot = self.take_screenshot("03_firefox_opened")
            demo_steps.append({"step": 3.1, "action": "firefox_screenshot", "result": firefox_screenshot})
        
        # ステップ4: ウィンドウ一覧を取得
        print("\n🪟 ステップ4: 開いているウィンドウを確認")
        windows = self.get_window_list()
        demo_steps.append({"step": 4, "action": "get_windows", "result": len(windows)})
        
        # ステップ5: テキスト入力のデモ（ターミナルに）
        print("\n⌨️ ステップ5: ターミナルでコマンド入力")
        time.sleep(1)
        
        # ターミナルをクリック（アクティブ化）
        click_success = self.simulate_mouse_click(400, 200)
        if click_success:
            time.sleep(1)
            text_success = self.type_text("echo 'Hello from AI GUI Automation!'")
            demo_steps.append({"step": 5, "action": "type_text", "result": text_success})
            
            if text_success:
                time.sleep(1)
                # Enterキーを押す
                subprocess.run(["xdotool", "key", "Return"], env={"DISPLAY": self.display})
                time.sleep(2)
                
                command_screenshot = self.take_screenshot("04_command_executed")
                demo_steps.append({"step": 5.1, "action": "command_screenshot", "result": command_screenshot})
        
        # ステップ6: 最終状態のスクリーンショット
        print("\n📸 ステップ6: 最終デスクトップ状態を撮影")
        final_screenshot = self.take_screenshot("05_final_desktop")
        demo_steps.append({"step": 6, "action": "final_screenshot", "result": final_screenshot})
        
        # デモ結果をまとめ
        print("\n🎯 AI GUI自動操作デモ完了！")
        print("=" * 50)
        
        # 成功したステップをカウント
        successful_steps = sum(1 for step in demo_steps if step.get("result"))
        total_steps = len(demo_steps)
        success_rate = (successful_steps / total_steps) * 100
        
        print(f"✅ 成功ステップ: {successful_steps}/{total_steps}")
        print(f"📊 成功率: {success_rate:.1f}%")
        
        # 作成されたスクリーンショットを表示
        screenshots = [step["result"] for step in demo_steps 
                      if step["action"].endswith("_screenshot") and step["result"]]
        
        print(f"\n📸 撮影されたスクリーンショット: {len(screenshots)}枚")
        for screenshot in screenshots:
            print(f"   📷 {Path(screenshot).name}")
        
        # ログを保存
        self.save_demo_log("complete_demo", {
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "success_rate": success_rate,
            "screenshots": screenshots,
            "demo_steps": demo_steps
        })
        
        print("\n🎊 30年来の夢、実現！")
        print("   AIが自分のGUIデスクトップを操作する時代が到来しました！")
        print(f"   noVNC URL: http://localhost:6080")
        print(f"   スクリーンショット保存先: {self.screenshot_dir}")
        
        return demo_steps

def main():
    """メイン実行関数"""
    # xdotoolがインストールされているか確認
    try:
        subprocess.run(["which", "xdotool"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("📦 xdotoolをインストールします...")
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "xdotool"], check=True)
        print("✅ xdotoolインストール完了")
    
    # デモシステムを開始
    demo = AIGUIAutomationDemo()
    result = demo.run_complete_demo()
    
    return result

if __name__ == "__main__":
    main()
