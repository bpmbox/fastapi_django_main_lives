"""
システムスクリーンショット自動取得ツール
=====================================

RPA機能を使用してシステムの画面キャプチャを自動取得
"""

import os
import time
from pathlib import Path
import subprocess
from controllers.conversation_logger import log_this_conversation

def capture_system_screenshots():
    """システムのスクリーンショットを自動取得"""
    
    screenshots_dir = Path("/workspaces/fastapi_django_main_live/docs/images/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    # 取得するページとファイル名のマッピング
    capture_targets = [
        {
            "url": "https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/",
            "filename": "main_dashboard.png",
            "description": "メインダッシュボード"
        },
        {
            "url": "http://localhost:7865",
            "filename": "contbk_dashboard.png", 
            "description": "ContBK統合ダッシュボード"
        }
    ]
    
    results = []
    
    for target in capture_targets:
        try:
            print(f"📸 スクリーンショット取得中: {target['description']}")
            
            # RPA機能を使用してスクリーンショット取得
            result = capture_webpage_screenshot(
                url=target["url"],
                output_path=screenshots_dir / target["filename"],
                description=target["description"]
            )
            
            results.append({
                "target": target,
                "success": result,
                "file_path": screenshots_dir / target["filename"]
            })
            
            print(f"{'✅' if result else '❌'} {target['description']}: {result}")
            
        except Exception as e:
            print(f"❌ エラー: {target['description']} - {e}")
            results.append({
                "target": target,
                "success": False,
                "error": str(e)
            })
    
    return results

def capture_webpage_screenshot(url: str, output_path: Path, description: str) -> bool:
    """Webページのスクリーンショットを取得"""
    
    try:
        # RPA自動化システムを使用
        from contbk.gra_12_rpa.rpa_automation import take_screenshot_of_url
        
        # スクリーンショット取得
        success = take_screenshot_of_url(
            url=url,
            output_file=str(output_path),
            wait_time=3  # 3秒待機
        )
        
        if success and output_path.exists():
            print(f"✅ スクリーンショット保存: {output_path}")
            return True
        else:
            print(f"❌ スクリーンショット取得失敗: {url}")
            return False
            
    except ImportError:
        print("⚠️ RPA機能が利用できません。別の方法を試します...")
        return capture_with_selenium(url, output_path)
    except Exception as e:
        print(f"❌ RPA機能エラー: {e}")
        return capture_with_selenium(url, output_path)

def capture_with_selenium(url: str, output_path: Path) -> bool:
    """Seleniumを使用してスクリーンショット取得"""
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Chromeオプション設定
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Webドライバー起動
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # ページにアクセス
            driver.get(url)
            time.sleep(3)  # ページ読み込み待機
            
            # スクリーンショット取得
            driver.save_screenshot(str(output_path))
            
            print(f"✅ Seleniumでスクリーンショット取得: {output_path}")
            return True
            
        finally:
            driver.quit()
            
    except ImportError:
        print("⚠️ Seleniumが利用できません")
        return False
    except Exception as e:
        print(f"❌ Seleniumエラー: {e}")
        return False

def upload_screenshots_to_git():
    """スクリーンショットをGitにコミット"""
    
    try:
        # Git add
        result = subprocess.run([
            'git', 'add', 'docs/images/screenshots/'
        ], capture_output=True, text=True, cwd='/workspaces/fastapi_django_main_live')
        
        if result.returncode == 0:
            print("✅ スクリーンショットをGitにステージング")
        else:
            print(f"⚠️ Git add警告: {result.stderr}")
        
        # Git commit
        result = subprocess.run([
            'git', 'commit', '-m', 
            '📸 システムスクリーンショット追加\n\n- メインダッシュボードキャプチャ\n- ContBK統合ダッシュボードキャプチャ\n- ドキュメント用画面資料完備'
        ], capture_output=True, text=True, cwd='/workspaces/fastapi_django_main_live')
        
        if result.returncode == 0:
            print("✅ スクリーンショットをコミット")
            return True
        else:
            print(f"⚠️ コミット結果: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Git操作エラー: {e}")
        return False

def main():
    """メイン実行関数"""
    
    print("🚀 システムスクリーンショット自動取得開始...")
    
    # スクリーンショット取得
    results = capture_system_screenshots()
    
    # 結果確認
    successful_captures = [r for r in results if r.get('success', False)]
    
    print(f"\n📊 取得結果: {len(successful_captures)}/{len(results)} 成功")
    
    if successful_captures:
        print("\n✅ 取得成功:")
        for result in successful_captures:
            print(f"  - {result['target']['description']}: {result['file_path']}")
        
        # Gitにアップロード
        if upload_screenshots_to_git():
            print("\n🎉 スクリーンショットのアップロード完了!")
        else:
            print("\n⚠️ Gitアップロードでエラーが発生しました")
    else:
        print("\n❌ スクリーンショット取得に失敗しました")
    
    # 会話履歴に記録
    log_this_conversation(
        user_msg="キャプチャした資料はアップした？",
        assistant_msg=f"スクリーンショット自動取得ツールを作成・実行しました。{len(successful_captures)}/{len(results)}個のスクリーンショット取得に成功。",
        context="システムスクリーンショット自動取得",
        files=["screenshot_capture.py", "docs/images/screenshots/"],
        tools=["RPA", "Selenium", "Git"],
        tags=["screenshot", "documentation", "automation"]
    )
    
    return results

if __name__ == "__main__":
    main()
