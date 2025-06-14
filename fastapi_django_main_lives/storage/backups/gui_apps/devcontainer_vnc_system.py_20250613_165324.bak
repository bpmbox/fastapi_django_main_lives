#!/usr/bin/env python3
"""
🌟 DevContainer版 VNC統合自動化システム
==========================================

ローカルVNC環境での画面操作 + キャプチャ + AI記憶
DevContainer環境に最適化されたバージョン
"""

import os
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path
import signal
import atexit

class DevContainerVNCSystem:
    """DevContainer環境でのVNC自動化システム"""
    
    def __init__(self):
        self.display = ":99"
        self.vnc_port = "5999"
        self.vnc_password = "ai2025"
        self.resolution = "1920x1080"
        self.memory_path = "/ai-memory/vnc"
        self.xvfb_process = None
        self.vnc_process = None
        
        self.setup_directories()
        
    def setup_directories(self):
        """必要ディレクトリ作成"""
        os.makedirs(self.memory_path, exist_ok=True)
        os.makedirs(f"{self.memory_path}/screenshots", exist_ok=True)
        os.makedirs(f"{self.memory_path}/operations", exist_ok=True)
        
    def start_virtual_display(self):
        """仮想ディスプレイ起動"""
        print(f"🖥️ 仮想ディスプレイ起動: DISPLAY={self.display}")
        
        # Xvfb起動
        cmd = [
            "Xvfb", self.display,
            "-screen", "0", f"{self.resolution}x24",
            "-ac", "+extension", "GLX"
        ]
        
        self.xvfb_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(2)  # 起動待機
        
        # 環境変数設定
        os.environ["DISPLAY"] = self.display
        
        print(f"✅ 仮想ディスプレイ起動完了: PID {self.xvfb_process.pid}")
        
    def start_vnc_server(self):
        """VNCサーバー起動"""
        print(f"🌐 VNCサーバー起動: ポート {self.vnc_port}")
        
        # VNCパスワードファイル作成
        passwd_file = "/tmp/vncpasswd"
        subprocess.run([
            "x11vnc", "-storepasswd", self.vnc_password, passwd_file
        ], check=True)
        
        # VNCサーバー起動
        cmd = [
            "x11vnc",
            "-display", self.display,
            "-rfbport", self.vnc_port,
            "-passwd", passwd_file,
            "-shared", "-forever",
            "-noxdamage"
        ]
        
        self.vnc_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(2)  # 起動待機
        print(f"✅ VNCサーバー起動完了: PID {self.vnc_process.pid}")
        print(f"🔗 VNC接続: localhost:{self.vnc_port} (パスワード: {self.vnc_password})")
        
    def stop_services(self):
        """サービス停止"""
        print("🛑 VNCサービス停止中...")
        
        if self.vnc_process:
            self.vnc_process.terminate()
            self.vnc_process.wait()
            print("✅ VNCサーバー停止")
            
        if self.xvfb_process:
            self.xvfb_process.terminate()
            self.xvfb_process.wait()
            print("✅ 仮想ディスプレイ停止")
            
    def capture_screen(self, output_path=None):
        """画面キャプチャ"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self.memory_path}/screenshots/screen_{timestamp}.png"
        
        # scrotでスクリーンショット
        cmd = ["scrot", "-z", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ スクリーンショット成功: {output_path}")
            self.log_operation("screenshot", {"path": output_path}, True)
            return output_path
        else:
            print(f"❌ スクリーンショット失敗: {result.stderr}")
            self.log_operation("screenshot", {"path": output_path}, False, result.stderr)
            return None
            
    def click_coordinates(self, x, y):
        """座標クリック"""
        cmd = ["xdotool", "mousemove", str(x), str(y), "click", "1"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ クリック成功: ({x}, {y})")
            self.log_operation("click", {"x": x, "y": y}, True)
            return True
        else:
            print(f"❌ クリック失敗: {result.stderr}")
            self.log_operation("click", {"x": x, "y": y}, False, result.stderr)
            return False
            
    def type_text(self, text):
        """テキスト入力"""
        cmd = ["xdotool", "type", text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ テキスト入力成功: {text}")
            self.log_operation("type", {"text": text}, True)
            return True
        else:
            print(f"❌ テキスト入力失敗: {result.stderr}")
            self.log_operation("type", {"text": text}, False, result.stderr)
            return False
            
    def open_application(self, app_name):
        """アプリケーション起動"""
        cmd = [app_name]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(3)  # アプリ起動待機
        
        print(f"✅ アプリケーション起動: {app_name} (PID: {process.pid})")
        self.log_operation("open_app", {"app": app_name, "pid": process.pid}, True)
        return process
        
    def log_operation(self, operation, params, success, error=None):
        """操作ログ記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "parameters": params,
            "success": success,
            "error": error
        }
        
        log_file = f"{self.memory_path}/operations/operations.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    def get_operation_history(self, limit=10):
        """操作履歴取得"""
        log_file = f"{self.memory_path}/operations/operations.jsonl"
        if not os.path.exists(log_file):
            return []
            
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        operations = []
        for line in lines[-limit:]:
            try:
                operations.append(json.loads(line.strip()))
            except:
                continue
                
        return operations
        
    def demo_automation(self):
        """自動化デモ実行"""
        print("🎭 VNC自動化デモ開始！")
        print("=" * 50)
        
        # 1. 画面キャプチャ
        print("📸 初期画面キャプチャ...")
        self.capture_screen()
        
        # 2. Firefox起動
        print("🌐 Firefox起動...")
        firefox = self.open_application("firefox")
        time.sleep(5)
        
        # 3. 画面キャプチャ（Firefox起動後）
        print("📸 Firefox起動後キャプチャ...")
        self.capture_screen()
        
        # 4. クリック操作テスト
        print("🖱️ クリック操作テスト...")
        self.click_coordinates(400, 300)
        
        # 5. テキスト入力テスト
        print("⌨️ テキスト入力テスト...")
        self.type_text("AI-Human Collaboration Success!")
        
        # 6. 最終画面キャプチャ
        print("📸 最終画面キャプチャ...")
        final_screenshot = self.capture_screen()
        
        print("\n🎉 デモ完了！")
        print(f"📁 スクリーンショット保存先: {self.memory_path}/screenshots/")
        print(f"📊 操作ログ: {self.memory_path}/operations/operations.jsonl")
        
        # Firefox終了
        firefox.terminate()
        
        return final_screenshot

def main():
    """メイン実行"""
    vnc_system = DevContainerVNCSystem()
    
    # 終了時クリーンアップ登録
    atexit.register(vnc_system.stop_services)
    
    try:
        # VNC環境起動
        vnc_system.start_virtual_display()
        vnc_system.start_vnc_server()
        
        print(f"""
🎉 DevContainer VNC統合システム起動完了！
=========================================

🖥️ 仮想ディスプレイ: {vnc_system.display} ({vnc_system.resolution})
🌐 VNC接続: localhost:{vnc_system.vnc_port}
🔐 パスワード: {vnc_system.vnc_password}
📁 AI記憶: {vnc_system.memory_path}

💡 VNCビューアーで接続して画面を確認できます！
""")
        
        # デモ実行
        input("🚀 デモを実行しますか？ (Enter キーで開始)")
        vnc_system.demo_automation()
        
        # 操作履歴表示
        print("\n📊 操作履歴:")
        history = vnc_system.get_operation_history()
        for i, op in enumerate(history[-5:], 1):
            status = "✅" if op['success'] else "❌"
            print(f"  {i}. {status} {op['operation']}: {op['timestamp']}")
        
        print("\n🎯 VNCサーバーは起動中です")
        print("終了するには Ctrl+C を押してください")
        
        # 無限待機
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 終了要求を受信...")
        vnc_system.stop_services()
        print("✅ 正常終了")

if __name__ == "__main__":
    main()
