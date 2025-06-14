"""
RPAシステム with Gradio
========================

Playwright + Gradio を使った Web RPA システム

機能:
- 🎯 ウェブページスクリーンショット
- 🖱️ 画面操作自動化
- 📸 画像比較・認識
- 🔄 定期実行・監視
- 📊 実行履歴・ログ管理
"""

import asyncio
import os
import sys
import datetime
import json
import sqlite3
from typing import Optional, List, Dict, Tuple
from pathlib import Path
import traceback

import gradio as gr
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# Playwrightのインポート（遅延インポート）
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not installed. Install with: pip install playwright && playwright install")

# インターフェースメタデータ
interface_title = "🤖 RPA自動化システム"
interface_description = "Playwright + Gradio による Web RPA・画面自動化"

class RPAManager:
    def __init__(self, db_path: str = "rpa_history.db"):
        """RPA管理システムの初期化"""
        self.db_path = db_path
        self.init_database()
        self.browser = None
        self.page = None
        
    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # RPA実行履歴テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rpa_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                url TEXT,
                action_type TEXT NOT NULL,
                parameters TEXT,
                screenshot_path TEXT,
                success BOOLEAN,
                error_message TEXT,
                execution_time REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # RPAタスクテンプレートテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rpa_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT NOT NULL UNIQUE,
                description TEXT,
                actions TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ RPA データベース初期化完了")
    
    async def capture_screenshot(self, url: str, selector: str = None, wait_time: int = 3) -> Tuple[Image.Image, str]:
        """
        ウェブページのスクリーンショットを取得
        
        Args:
            url: 対象URL
            selector: 特定要素のセレクタ（オプション）
            wait_time: 待機時間（秒）
            
        Returns:
            (画像, エラーメッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # ページ読み込み
                await page.goto(url, wait_until='networkidle')
                
                # 待機
                await asyncio.sleep(wait_time)
                
                # スクリーンショット取得
                if selector:
                    # 特定要素のスクリーンショット
                    element = await page.query_selector(selector)
                    if element:
                        screenshot_bytes = await element.screenshot()
                    else:
                        screenshot_bytes = await page.screenshot()
                        return None, f"セレクタ '{selector}' が見つかりません"
                else:
                    # ページ全体のスクリーンショット
                    screenshot_bytes = await page.screenshot(full_page=True)
                
                await browser.close()
                
                # PIL画像に変換
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                # 実行履歴を保存
                self.save_execution(
                    task_name="スクリーンショット取得",
                    url=url,
                    action_type="screenshot",
                    parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                    success=True
                )
                
                return img, "✅ スクリーンショット取得成功"
                
        except Exception as e:
            error_msg = f"❌ エラー: {str(e)}"
            
            # エラーログを保存
            self.save_execution(
                task_name="スクリーンショット取得",
                url=url,
                action_type="screenshot",
                parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    async def click_element(self, url: str, selector: str, wait_time: int = 3) -> Tuple[Image.Image, str]:
        """
        要素をクリックして結果をキャプチャ
        
        Args:
            url: 対象URL
            selector: クリック対象のセレクタ
            wait_time: クリック後の待機時間
            
        Returns:
            (クリック後の画像, メッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # ページ読み込み
                await page.goto(url, wait_until='networkidle')
                
                # 要素を待機してクリック
                await page.wait_for_selector(selector, timeout=10000)
                await page.click(selector)
                
                # 待機
                await asyncio.sleep(wait_time)
                
                # クリック後のスクリーンショット
                screenshot_bytes = await page.screenshot(full_page=True)
                await browser.close()
                
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                # 実行履歴を保存
                self.save_execution(
                    task_name="要素クリック",
                    url=url,
                    action_type="click",
                    parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                    success=True
                )
                
                return img, f"✅ 要素クリック成功: {selector}"
                
        except Exception as e:
            error_msg = f"❌ クリックエラー: {str(e)}"
            
            self.save_execution(
                task_name="要素クリック",
                url=url,
                action_type="click",
                parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    async def fill_form(self, url: str, form_data: Dict[str, str], submit_selector: str = None) -> Tuple[Image.Image, str]:
        """
        フォーム入力と送信
        
        Args:
            url: 対象URL
            form_data: {セレクタ: 入力値} の辞書
            submit_selector: 送信ボタンのセレクタ
            
        Returns:
            (実行後の画像, メッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, wait_until='networkidle')
                
                # フォーム入力
                for selector, value in form_data.items():
                    await page.wait_for_selector(selector, timeout=10000)
                    await page.fill(selector, value)
                    await asyncio.sleep(0.5)
                
                # 送信ボタンクリック
                if submit_selector:
                    await page.click(submit_selector)
                    await asyncio.sleep(3)
                
                # 結果のスクリーンショット
                screenshot_bytes = await page.screenshot(full_page=True)
                await browser.close()
                
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                self.save_execution(
                    task_name="フォーム入力",
                    url=url,
                    action_type="fill_form",
                    parameters=json.dumps({"form_data": form_data, "submit_selector": submit_selector}),
                    success=True
                )
                
                return img, "✅ フォーム入力・送信成功"
                
        except Exception as e:
            error_msg = f"❌ フォーム入力エラー: {str(e)}"
            
            self.save_execution(
                task_name="フォーム入力",
                url=url,
                action_type="fill_form",
                parameters=json.dumps({"form_data": form_data, "submit_selector": submit_selector}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    async def collect_images_from_page(self, url: str, image_selector: str = "img", 
                                      download_path: str = None, limit: int = 10) -> Tuple[List[str], str]:
        """
        ウェブページから画像を取得・ダウンロード
        
        Args:
            url: 対象URL
            image_selector: 画像要素のセレクタ（デフォルト: "img"）
            download_path: ダウンロード先パス
            limit: 取得画像数の上限
            
        Returns:
            (ダウンロードファイルパスのリスト, メッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return [], "Playwright がインストールされていません"
        
        if not download_path:
            download_path = "/workspaces/fastapi_django_main_live/docs/images/collected"
        
        import os
        import requests
        from urllib.parse import urljoin, urlparse
        from pathlib import Path
        
        # ダウンロードディレクトリ作成
        Path(download_path).mkdir(parents=True, exist_ok=True)
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(2)
                
                # 画像要素を取得
                image_elements = await page.query_selector_all(image_selector)
                print(f"🖼️ {len(image_elements)}個の画像要素を発見")
                
                downloaded_files = []
                
                for i, img_element in enumerate(image_elements[:limit]):
                    try:
                        # 画像のsrc属性を取得
                        src = await img_element.get_attribute('src')
                        if not src:
                            continue
                        
                        # 相対パスを絶対パスに変換
                        image_url = urljoin(url, src)
                        
                        # ファイル名を生成
                        parsed_url = urlparse(image_url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename or '.' not in filename:
                            filename = f"image_{i+1}.jpg"
                        
                        # ファイルパス
                        file_path = os.path.join(download_path, filename)
                        
                        # 画像をダウンロード
                        response = requests.get(image_url, stream=True, timeout=10)
                        if response.status_code == 200:
                            with open(file_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            downloaded_files.append(file_path)
                            print(f"✅ ダウンロード完了: {filename}")
                        else:
                            print(f"⚠️ ダウンロード失敗: {image_url} (Status: {response.status_code})")
                            
                    except Exception as e:
                        print(f"⚠️ 画像処理エラー: {e}")
                        continue
                
                await browser.close()
                
                # 実行履歴保存
                self.save_execution(
                    task_name="画像取得",
                    url=url,
                    action_type="collect_images",
                    parameters=json.dumps({
                        "image_selector": image_selector,
                        "download_path": download_path,
                        "limit": limit,
                        "downloaded_count": len(downloaded_files)
                    }),
                    success=True
                )
                
                return downloaded_files, f"✅ {len(downloaded_files)}個の画像を取得しました"
                
        except Exception as e:
            error_msg = f"❌ 画像取得エラー: {str(e)}"
            
            self.save_execution(
                task_name="画像取得",
                url=url,
                action_type="collect_images",
                parameters=json.dumps({
                    "image_selector": image_selector,
                    "download_path": download_path,
                    "limit": limit
                }),
                success=False,
                error_message=str(e)
            )
            
            return [], error_msg
    
    async def create_image_gallery(self, image_paths: List[str], output_path: str = None) -> str:
        """
        取得した画像から一覧ギャラリーを作成
        
        Args:
            image_paths: 画像ファイルパスのリスト
            output_path: 出力HTMLファイルパス
            
        Returns:
            生成されたHTMLファイルパス
        """
        if not output_path:
            output_path = "/workspaces/fastapi_django_main_live/docs/image_gallery.html"
        
        # HTMLギャラリー生成
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📸 RPA画像取得ギャラリー</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
        }}
        .image-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }}
        .image-info {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .stats {{
            text-align: center;
            margin-bottom: 20px;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 RPA画像取得ギャラリー</h1>
        <div class="stats">
            <p>🎯 取得画像数: <strong>{image_count}</strong></p>
            <p>📅 生成日時: <strong>{timestamp}</strong></p>
        </div>
        <div class="gallery">
            {image_cards}
        </div>
    </div>
</body>
</html>"""
        
        # 画像カード生成
        image_cards = ""
        for i, image_path in enumerate(image_paths, 1):
            import os
            filename = os.path.basename(image_path)
            # 相対パスに変換
            rel_path = os.path.relpath(image_path, os.path.dirname(output_path))
            
            image_cards += f"""
            <div class="image-card">
                <img src="{rel_path}" alt="取得画像 {i}">
                <div class="image-info">
                    <strong>#{i}</strong> - {filename}
                </div>
            </div>
            """
        
        # HTMLコンテンツ完成
        final_html = html_content.format(
            image_count=len(image_paths),
            timestamp=datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
            image_cards=image_cards
        )
        
        # ファイル出力
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        return output_path

    def save_execution(self, task_name: str, url: str, action_type: str, 
                      parameters: str, success: bool, error_message: str = None):
        """実行履歴をデータベースに保存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rpa_executions 
                (task_name, url, action_type, parameters, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (task_name, url, action_type, parameters, success, error_message))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ 実行履歴保存エラー: {e}")
    
    def get_execution_history(self, limit: int = 20) -> List[Dict]:
        """実行履歴を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT task_name, url, action_type, success, error_message, created_at
                FROM rpa_executions 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "task_name": row[0],
                    "url": row[1],
                    "action_type": row[2],
                    "success": row[3],
                    "error_message": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"⚠️ 履歴取得エラー: {e}")
            return []

# グローバルインスタンス
rpa_manager = RPAManager()

def create_rpa_interface():
    """RPA Gradio インターフェースを作成"""
    
    def screenshot_wrapper(url, selector, wait_time):
        """スクリーンショット取得のラッパー関数"""
        if not url:
            return None, "❌ URLを入力してください"
        
        try:
            img, message = asyncio.run(rpa_manager.capture_screenshot(url, selector or None, wait_time))
            return img, message
        except Exception as e:
            return None, f"❌ エラー: {str(e)}"
    
    def click_wrapper(url, selector, wait_time):
        """クリック操作のラッパー関数"""
        if not url or not selector:
            return None, "❌ URLとセレクタを入力してください"
        
        try:
            img, message = asyncio.run(rpa_manager.click_element(url, selector, wait_time))
            return img, message
        except Exception as e:
            return None, f"❌ エラー: {str(e)}"
    
    def get_history_display():
        """実行履歴を表示用フォーマットで取得"""
        history = rpa_manager.get_execution_history(10)
        if not history:
            return "📊 実行履歴はありません"
        
        lines = ["# 🕒 RPA実行履歴", ""]
        for i, record in enumerate(history, 1):
            status = "✅" if record["success"] else "❌"
            lines.append(f"## {i}. {status} {record['task_name']}")
            lines.append(f"- **URL**: {record['url']}")
            lines.append(f"- **アクション**: {record['action_type']}")
            lines.append(f"- **日時**: {record['created_at']}")
            if record["error_message"]:
                lines.append(f"- **エラー**: {record['error_message']}")
            lines.append("")
        
        return "\n".join(lines)
    
    with gr.Blocks(title="🤖 RPA自動化システム", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 RPA自動化システム")
        gr.Markdown("Playwright + Gradio による Web自動化・画面操作ツール")
        
        if not PLAYWRIGHT_AVAILABLE:
            gr.Markdown("""
            ## ⚠️ セットアップが必要です
            
            Playwrightをインストールしてください:
            ```bash
            pip install playwright
            playwright install
            ```
            """)
        
        with gr.Tab("📸 スクリーンショット"):
            gr.Markdown("## 🎯 ウェブページキャプチャ")
            
            with gr.Row():
                with gr.Column(scale=2):
                    url_input = gr.Textbox(
                        label="🌐 URL",
                        placeholder="https://example.com",
                        value="https://www.google.com"
                    )
                with gr.Column(scale=1):
                    wait_time = gr.Slider(
                        label="⏱️ 待機時間(秒)",
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1
                    )
            
            selector_input = gr.Textbox(
                label="🎯 セレクタ (オプション)",
                placeholder="body, .class-name, #id-name など",
                value=""
            )
            
            screenshot_btn = gr.Button("📸 スクリーンショット取得", variant="primary", size="lg")
            
            with gr.Row():
                screenshot_output = gr.Image(label="📷 取得画像")
                screenshot_message = gr.Textbox(label="📝 実行結果", lines=3)
            
            screenshot_btn.click(
                screenshot_wrapper,
                inputs=[url_input, selector_input, wait_time],
                outputs=[screenshot_output, screenshot_message]
            )
        
        with gr.Tab("🖱️ 画面操作"):
            gr.Markdown("## 🎯 要素クリック・操作")
            
            with gr.Row():
                click_url = gr.Textbox(
                    label="🌐 URL",
                    placeholder="https://example.com",
                    scale=2
                )
                click_wait = gr.Slider(
                    label="⏱️ 待機時間",
                    minimum=1,
                    maximum=10,
                    value=3,
                    scale=1
                )
            
            click_selector = gr.Textbox(
                label="🎯 クリック対象セレクタ",
                placeholder="button, .btn, #submit など",
                value=""
            )
            
            click_btn = gr.Button("🖱️ クリック実行", variant="primary", size="lg")
            
            with gr.Row():
                click_output = gr.Image(label="📷 実行後画像")
                click_message = gr.Textbox(label="📝 実行結果", lines=3)
            
            click_btn.click(
                click_wrapper,
                inputs=[click_url, click_selector, click_wait],
                outputs=[click_output, click_message]
            )
        
        with gr.Tab("🖼️ 画像取得"):
            gr.Markdown("## 🎯 ウェブページから画像収集")
            
            def image_collect_wrapper(url, selector, limit, download_path):
                """画像取得のラッパー関数"""
                if not url:
                    return [], "❌ URLを入力してください", ""
                
                try:
                    files, message = asyncio.run(rpa_manager.collect_images_from_page(
                        url, selector or "img", download_path or None, int(limit)
                    ))
                    
                    if files:
                        # ギャラリーHTML作成
                        gallery_path = asyncio.run(rpa_manager.create_image_gallery(files))
                        gallery_url = f"file://{gallery_path}"
                        return files, message, f"📖 ギャラリー作成: {gallery_path}"
                    else:
                        return [], message, ""
                        
                except Exception as e:
                    return [], f"❌ エラー: {str(e)}", ""
            
            with gr.Row():
                with gr.Column(scale=2):
                    image_url = gr.Textbox(
                        label="🌐 URL",
                        placeholder="https://example.com",
                        value="https://www.google.com/search?q=cats&tbm=isch"
                    )
                with gr.Column(scale=1):
                    image_limit = gr.Slider(
                        label="📊 取得数上限",
                        minimum=1,
                        maximum=50,
                        value=5,
                        step=1
                    )
            
            with gr.Row():
                image_selector = gr.Textbox(
                    label="🎯 画像セレクタ",
                    placeholder="img (デフォルト)",
                    value="img",
                    scale=2
                )
                download_path = gr.Textbox(
                    label="📁 ダウンロード先",
                    placeholder="/workspaces/fastapi_django_main_live/docs/images/collected (デフォルト)",
                    value="",
                    scale=2
                )
            
            collect_btn = gr.Button("🖼️ 画像取得開始", variant="primary", size="lg")
            
            with gr.Row():
                with gr.Column():
                    collected_files = gr.File(
                        label="📁 取得ファイル一覧",
                        file_count="multiple",
                        height=200
                    )
                with gr.Column():
                    collect_message = gr.Textbox(label="📝 実行結果", lines=3)
                    gallery_info = gr.Textbox(label="📖 ギャラリー情報", lines=2)
            
            collect_btn.click(
                image_collect_wrapper,
                inputs=[image_url, image_selector, image_limit, download_path],
                outputs=[collected_files, collect_message, gallery_info]
            )
        
        with gr.Tab("📊 実行履歴"):
            gr.Markdown("## 🕒 RPA実行履歴")
            
            refresh_btn = gr.Button("🔄 履歴更新", variant="secondary")
            history_display = gr.Markdown(value=get_history_display())
            
            refresh_btn.click(
                get_history_display,
                outputs=history_display
            )
        
        with gr.Tab("ℹ️ ヘルプ"):
            gr.Markdown("""
            ## 📚 RPA自動化システム ヘルプ
            
            ### 🎯 機能概要
            - **📸 スクリーンショット**: ウェブページの画面キャプチャ
            - **🖱️ 画面操作**: 要素のクリック、フォーム入力
            - **📷 画像取得**: ウェブページからの画像ダウンロード
            - **📊 履歴管理**: 実行履歴の記録・表示
            
            ### 🔧 セレクタ例
            - **要素タイプ**: `button`, `input`, `a`
            - **クラス**: `.btn`, `.form-control`, `.nav-link`
            - **ID**: `#submit`, `#login-form`, `#search-box`
            - **属性**: `[name="email"]`, `[type="submit"]`
            
            ### 💡 使用例
            1. **Google検索**: 
               - URL: `https://www.google.com`
               - セレクタ: `[name="q"]` (検索ボックス)
            
            2. **ボタンクリック**:
               - セレクタ: `button`, `.btn-primary`, `#submit-btn`
            
            3. **画像取得**:
               - URL: `https://example.com`
               - 画像セレクタ: `img`
               - ダウンロード先: `/path/to/download`
            
            ### ⚠️ 注意事項
            - 対象サイトの利用規約を確認してください
            - 過度なアクセスは避けてください
            - エラーが発生した場合は履歴を確認してください
            """)
    
    return interface

# このファイルのメインエクスポート
gradio_interface = create_rpa_interface()

# スタンドアロン実行用
if __name__ == "__main__":
    print("🤖 RPA自動化システム起動中...")
    gradio_interface.launch(
        server_port=7865,
        share=False,
        debug=True
    )
