"""
シンプルなWeb Routes - Gradioテスト用
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

# 直接Gradio実行ルート（テスト用）
@router.get("/tools/chat/direct")
async def chat_direct(request: Request):
    """
    チャット機能の直接実行（シンプル版）
    """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💬 AI Chat Tool</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }}
            .chat-box {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; min-height: 200px; }}
            .input-group {{ display: flex; gap: 10px; margin-top: 20px; }}
            .input-group input {{ flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }}
            .input-group button {{ padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; }}
            .response {{ background: white; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 4px; }}
            .url-info {{ background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💬 AI Chat Interface</h1>
                <div class="url-info">📍 現在のURL: {request.url}</div>
                <p>PWA & キャプチャテスト対応のチャットツール</p>
            </div>
            
            <div class="chat-box" id="chatBox">
                <div class="response">
                    <strong>🤖 AI:</strong> こんにちは！何かお手伝いできることはありますか？
                </div>
            </div>
            
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="メッセージを入力してください..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">送信</button>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
        
        <script>
            function sendMessage() {{
                const input = document.getElementById('messageInput');
                const chatBox = document.getElementById('chatBox');
                const message = input.value.trim();
                
                if (message) {{
                    const userDiv = document.createElement('div');
                    userDiv.className = 'response';
                    userDiv.style.borderLeftColor = '#28a745';
                    userDiv.innerHTML = '<strong>👤 あなた:</strong> ' + message;
                    chatBox.appendChild(userDiv);
                    
                    setTimeout(() => {{
                        const aiDiv = document.createElement('div');
                        aiDiv.className = 'response';
                        aiDiv.innerHTML = '<strong>🤖 AI:</strong> ' + message + ' について理解しました。現在のURL: ' + window.location.href + '<br>タイムスタンプ: ' + new Date().toLocaleString();
                        chatBox.appendChild(aiDiv);
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }}, 500);
                    
                    input.value = '';
                    chatBox.scrollTop = chatBox.scrollHeight;
                }}
            }}
        </script>
    </body>
    </html>
    """)

@router.get("/tools/code-generator/direct")
async def code_generator_direct(request: Request):
    """
    コード生成機能の直接実行（シンプル版）
    """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 Code Generator</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }}
            .url-info {{ background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }}
            pre {{ background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Code Generator</h1>
                <div class="url-info">📍 現在のURL: {request.url}</div>
                <p>AIによるコード生成ツール - PWA対応</p>
            </div>
            
            <div>
                <h3>生成されたコード:</h3>
                <pre><code># AI生成コード例
def hello_world():
    print("Hello, World from AI Code Generator!")
    print("現在のURL: {request.url}")
    print("タイムスタンプ: 2025-06-13")
    return "生成完了"

if __name__ == "__main__":
    hello_world()
</code></pre>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
    </body>
    </html>
    """)

@router.get("/tools/screenshot/direct")
async def screenshot_direct(request: Request):
    """
    スクリーンショット機能の直接実行（シンプル版）
    """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📸 Screenshot Tool</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }}
            .url-info {{ background: #e9ecef; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px; margin-bottom: 20px; }}
            .capture-area {{ background: #f8f9fa; border-radius: 8px; padding: 30px; text-align: center; margin: 20px 0; }}
            .status {{ background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; padding: 15px; border-radius: 6px; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📸 Screenshot & Capture Tool</h1>
                <div class="url-info">📍 現在のURL: {request.url}</div>
                <p>PWA対応のスクリーンキャプチャツール</p>
            </div>
            
            <div class="capture-area">
                <h3>📱 PWAキャプチャテスト</h3>
                <p>このページはPWA/URL-basedスクリーンキャプチャのテスト用です</p>
            </div>
            
            <div class="status">
                <strong>📝 キャプチャ情報:</strong><br>
                ・URL: {request.url}<br>
                ・タイムスタンプ: 2025-06-13<br>
                ・PWA対応: 準備完了
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/dashboard" style="color: #007bff; text-decoration: none;">← ダッシュボードに戻る</a>
            </p>
        </div>
    </body>
    </html>
    """)
