#!/usr/bin/env python3
"""
noVNC画面操作のテストスクリプト
"""

import subprocess
import time
import requests
import os

def wait_for_novnc(timeout=300):
    """noVNCが起動するまで待機"""
    print("🔄 noVNCの起動を待機中...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:6081", timeout=5)
            if response.status_code == 200:
                print("✅ noVNCが起動しました！")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("⏳ 待機中... (Ctrl+Cで中断)")
        time.sleep(5)
    
    print("❌ タイムアウト: noVNCが起動しませんでした")
    return False

def check_container_status():
    """コンテナの状態を確認"""
    try:
        result = subprocess.run([
            "docker", "ps", "--filter", "name=ubuntu-desktop-vnc", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ], capture_output=True, text=True)
        
        print("📋 コンテナ状態:")
        print(result.stdout)
        
        # ログも確認
        log_result = subprocess.run([
            "docker", "logs", "ubuntu-desktop-vnc", "--tail", "10"
        ], capture_output=True, text=True)
        
        print("\n📝 最新ログ:")
        print(log_result.stdout)
        if log_result.stderr:
            print("⚠️ エラーログ:")
            print(log_result.stderr)
            
    except Exception as e:
        print(f"❌ ステータス確認エラー: {e}")

def run_automation_test():
    """自動化テストを実行"""
    print("🤖 画面自動化テストを開始...")
    
    # コンテナ内でPythonスクリプトを実行
    try:
        result = subprocess.run([
            "docker", "exec", "ubuntu-desktop-vnc", 
            "python3", "/code/desktop_automation.py"
        ], capture_output=True, text=True, timeout=60)
        
        print("📤 実行結果:")
        print(result.stdout)
        if result.stderr:
            print("⚠️ エラー:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ タイムアウト: スクリプト実行に時間がかかりすぎました")
    except Exception as e:
        print(f"❌ 実行エラー: {e}")

def main():
    """メイン実行"""
    print("🚀 noVNC環境テストを開始します")
    
    # 1. コンテナの状態確認
    check_container_status()
    
    # 2. noVNCの起動待機
    if wait_for_novnc():
        print("\n🌐 ブラウザでアクセスしてください:")
        print("   URL: http://localhost:6081")
        print("   パスワード: mypassword")
        
        # 3. 自動化テスト実行の選択
        choice = input("\n自動化テストを実行しますか? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            run_automation_test()
        
        print("\n✅ テスト完了！")
    else:
        print("❌ noVNCに接続できませんでした")

if __name__ == "__main__":
    main()
