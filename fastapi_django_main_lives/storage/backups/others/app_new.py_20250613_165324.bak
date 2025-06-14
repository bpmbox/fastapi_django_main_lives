#!/usr/bin/env python3
"""
Hugging Face Spaces FastAPI Debug Toolbar
GitHub Actions自動デプロイ版
"""
import os
import sys

# codespaces_debug.py から app をインポート
try:
    from codespaces_debug import app
    print("✅ FastAPI Debug Toolbar loaded successfully")
except ImportError as e:
    print(f"❌ Failed to import codespaces_debug: {e}")
    # フォールバック用の簡単なFastAPIアプリ
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    app = FastAPI(title="FastAPI Debug Toolbar - Error")
    
    @app.get("/")
    async def error_page():
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Debug Toolbar Error</title></head>
        <body>
            <h1>❌ Error Loading Debug Toolbar</h1>
            <p>Failed to load codespaces_debug.py</p>
            <p>Check the logs for more details.</p>
        </body>
        </html>
        """)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)
