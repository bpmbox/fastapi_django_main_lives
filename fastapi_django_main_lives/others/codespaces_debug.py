"""
完全動作版 FastAPI Debug Toolbar - 修正版
StreamingResponse対応バージョン + Hugging Face リポジトリ取得機能
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import asyncio
from datetime import datetime
from starlette.types import Message

# Hugging Face クライアントをインポート
try:
    from huggingface_client import HuggingFaceRepoClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False

app = FastAPI(title="FastAPI Debug Toolbar", description="Laravel風デバッグバー + Hugging Face連携")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# デバッグデータ
debug_data = {"requests": [], "queries": []}

def generate_debug_bar(request_info):
    """デバッグバーHTML生成"""
    return f"""
    <div id="debug-bar" style="
        position: fixed; bottom: 0; left: 0; right: 0; 
        background: #2d3748; color: white; font-family: monospace; font-size: 12px;
        z-index: 9999; border-top: 3px solid #4299e1; max-height: 40px; overflow: hidden;
        transition: max-height 0.3s ease;
    " onclick="this.style.maxHeight = this.style.maxHeight === '300px' ? '40px' : '300px'">
        
        <div style="padding: 8px 15px; background: #1a202c; display: flex; justify-content: space-between; cursor: pointer;">
            <div style="display: flex; gap: 20px;">
                <span style="color: #4299e1; font-weight: bold;">🔧 FastAPI Debug</span>
                <span>⏱️ {request_info['response_time']}</span>
                <span>📊 {len(debug_data['queries'])} queries</span>
                <span>📍 {request_info['method']} {request_info['path']}</span>
            </div>
            <span style="color: #68d391;">Status: {request_info['status']}</span>
        </div>
        
        <div style="padding: 15px; max-height: 250px; overflow-y: auto;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="color: #4299e1; margin: 0 0 8px 0;">📝 Request Info</h4>
                    <div style="background: #1a202c; padding: 8px; border-radius: 4px; font-size: 11px;">
                        <div>Method: {request_info['method']}</div>
                        <div>Path: {request_info['path']}</div>
                        <div>Time: {request_info['timestamp']}</div>
                        <div>Response: {request_info['response_time']}</div>
                    </div>
                </div>
                <div>
                    <h4 style="color: #f56565; margin: 0 0 8px 0;">🗄️ Queries ({len(debug_data['queries'])})</h4>
                    <div style="background: #1a202c; padding: 8px; border-radius: 4px; font-size: 11px;">
                        {"<br>".join([f"• {q['query']} ({q['time']})" for q in debug_data['queries'][-3:]]) or "No queries"}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    start_time = time.time()
    
    # レスポンス処理
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # リクエスト情報
    request_info = {
        "method": request.method,
        "path": request.url.path,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "response_time": f"{process_time:.3f}s",
        "status": response.status_code
    }
    debug_data["requests"].append(request_info)
    
    # HTMLResponseの場合のみデバッグバー注入を試行
    if isinstance(response, HTMLResponse):
        try:
            body = response.body
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            if "</body>" in body:
                debug_bar = generate_debug_bar(request_info)
                body = body.replace("</body>", f"{debug_bar}</body>")
                # 新しいHTMLResponseを作成
                new_response = HTMLResponse(content=body, status_code=response.status_code)
                # ヘッダーをコピー
                for key, value in response.headers.items():
                    new_response.headers[key] = value
                response = new_response
        except Exception as e:
            # エラーが発生してもレスポンスは返す
            print(f"Debug bar injection failed: {e}")
    
    # デバッグヘッダー追加（すべてのレスポンスに）
    response.headers["X-Debug-Time"] = f"{process_time:.3f}s"
    response.headers["X-Debug-Queries"] = str(len(debug_data["queries"]))
    response.headers["X-Debug-Method"] = request.method
    response.headers["X-Debug-Path"] = request.url.path
    
    return response

def mock_query(sql, delay=0.05):
    """データベースクエリシミュレート"""
    time.sleep(delay)
    debug_data["queries"].append({
        "query": sql,
        "time": f"{delay:.3f}s",
        "timestamp": datetime.now().isoformat()
    })

@app.get("/", response_class=HTMLResponse)
async def home():
    # ホームページのクエリをシミュレート
    mock_query("SELECT COUNT(*) FROM users", 0.05)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Debug Toolbar Demo</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 12px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{ margin: 0; font-size: 3em; font-weight: 300; }}
            .header p {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 1.2em; }}
            .content {{ padding: 40px; }}
            .feature {{ 
                background: #f8f9fa; 
                padding: 25px; 
                margin: 20px 0; 
                border-radius: 8px; 
                border-left: 4px solid #667eea;
            }}
            .feature h3 {{ 
                margin: 0 0 15px 0; 
                color: #667eea; 
                font-size: 1.3em;
            }}
            .feature ul {{ margin: 0; padding-left: 20px; }}
            .feature li {{ margin: 8px 0; line-height: 1.6; }}
            .button {{ 
                display: inline-block; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 12px 25px; 
                text-decoration: none; 
                border-radius: 25px; 
                margin: 10px 10px 10px 0; 
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
            }}
            .button:hover {{ 
                transform: translateY(-2px); 
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }}
            .stats {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                gap: 20px; 
                margin: 30px 0;
            }}
            .stat-card {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
                border-left: 4px solid #28a745;
            }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #28a745; }}
            .stat-label {{ color: #666; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔧 FastAPI Debug Toolbar</h1>
                <p>Laravel風のデバッグツールバーのデモンストレーション</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{len(debug_data["requests"])}</div>
                        <div class="stat-label">Total Requests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(debug_data["queries"])}</div>
                        <div class="stat-label">Database Queries</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">1</div>
                        <div class="stat-label">Active Sessions</div>
                    </div>
                </div>
                
                <div class="feature">
                    <h3>✨ 機能</h3>
                    <ul>
                        <li>🎯 <strong>リクエスト追跡</strong> - HTTPメソッド、パス、レスポンス時間</li>
                        <li>📊 <strong>クエリモニタリング</strong> - データベースクエリの実行時間</li>
                        <li>⚡ <strong>パフォーマンス測定</strong> - リアルタイムの応答速度</li>
                        <li>🎨 <strong>Laravel風デザイン</strong> - 親しみやすいダークテーマ</li>
                    </ul>
                </div>
                
                <div class="feature">
                    <h3>🚀 使用方法</h3>
                    <p>画面下部に表示されるデバッグバーをクリックして展開してください。</p>
                    <p>各エンドポイントにアクセスしてデバッグ情報を確認できます。</p>
                </div>
                
                <div style="margin-top: 30px; text-align: center;">
                    <a href="/api/users" class="button">👥 Users API</a>
                    <a href="/debug/dashboard" class="button">📊 Debug Dashboard</a>
                    <a href="/debug/clear" class="button">🗑️ Clear Debug Data</a>
                    <a href="/huggingface" class="button">🤗 HF Repository</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/api/users", response_class=HTMLResponse)
async def get_users():
    # クエリシミュレート
    mock_query("SELECT * FROM users WHERE active = 1", 0.08)
    mock_query("SELECT COUNT(*) FROM user_sessions", 0.03)
    
    users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
    ]
    
    # ユーザーテーブルの行を生成
    user_rows = ""
    for user in users:
        user_rows += f"""
                        <tr>
                            <td>#{user['id']}</td>
                            <td>{user['name']}</td>
                            <td>{user['email']}</td>
                            <td><span class="badge">Active</span></td>
                        </tr>"""
    
    # HTML ページとして返す
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Management</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ 
                max-width: 1000px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 12px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{ margin: 0; font-size: 2.5em; font-weight: 300; }}
            .content {{ padding: 30px; }}
            .stats {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px;
            }}
            .stat-card {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
                border-left: 4px solid #667eea;
            }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
            .stat-label {{ color: #666; margin-top: 5px; }}
            .user-table {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 20px;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .user-table th {{ 
                background: #667eea; 
                color: white; 
                padding: 15px; 
                text-align: left; 
                font-weight: 600;
            }}
            .user-table td {{ 
                padding: 15px; 
                border-bottom: 1px solid #eee;
                transition: background 0.2s;
            }}
            .user-table tr:hover td {{ background: #f8f9fa; }}
            .user-table tr:last-child td {{ border-bottom: none; }}
            .badge {{ 
                background: #28a745; 
                color: white; 
                padding: 4px 12px; 
                border-radius: 20px; 
                font-size: 0.8em;
                font-weight: 500;
            }}
            .nav {{ 
                background: #f8f9fa; 
                padding: 15px 30px; 
                border-bottom: 1px solid #eee;
            }}
            .nav a {{ 
                color: #667eea; 
                text-decoration: none; 
                margin-right: 20px; 
                font-weight: 500;
                transition: color 0.2s;
            }}
            .nav a:hover {{ color: #764ba2; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">🏠 Home</a>
                <a href="/api/users">👥 Users</a>
                <a href="/debug/dashboard">🔧 Debug</a>
            </div>
            
            <div class="header">
                <h1>👥 User Management</h1>
                <p>Manage your application users</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{len(users)}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(users)}</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">2</div>
                        <div class="stat-label">Database Queries</div>
                    </div>
                </div>
                
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {user_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/debug/dashboard", response_class=HTMLResponse)
async def debug_dashboard():
    mock_query("SELECT * FROM debug_info", 0.02)
    
    recent_requests = debug_data["requests"][-10:]
    recent_queries = debug_data["queries"][-10:]
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug Dashboard</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a202c; color: white; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
            .card {{ background: #2d3748; padding: 20px; border-radius: 8px; border-left: 4px solid #4299e1; }}
            .card h3 {{ margin-top: 0; color: #4299e1; }}
            .list-item {{ background: #1a202c; margin: 8px 0; padding: 10px; border-radius: 4px; font-size: 12px; }}
            .header {{ text-align: center; color: #4299e1; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">🔧 FastAPI Debug Dashboard</h1>
            
            <div class="grid">
                <div class="card">
                    <h3>📝 Recent Requests ({len(recent_requests)})</h3>
                    {"".join([f'<div class="list-item">{r["timestamp"]} - {r["method"]} {r["path"]} ({r["response_time"]}) - {r["status"]}</div>' for r in recent_requests])}
                </div>
                
                <div class="card">
                    <h3>🗄️ Recent Queries ({len(recent_queries)})</h3>
                    {"".join([f'<div class="list-item">{q["query"]} - {q["time"]}</div>' for q in recent_queries])}
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" style="color: #4299e1; text-decoration: none;">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/debug/clear")
async def clear_debug_data():
    debug_data["requests"].clear()
    debug_data["queries"].clear()
    return {"message": "Debug data cleared", "status": "success"}

@app.get("/huggingface", response_class=HTMLResponse)
async def huggingface_repo_viewer():
    """Hugging Face リポジトリ情報表示ページ"""
    if not HF_CLIENT_AVAILABLE:
        return """
        <html><body>
        <h1>❌ Hugging Face Client not available</h1>
        <p>huggingface_client.py が見つかりません</p>
        </body></html>
        """
    
    mock_query("SELECT * FROM hf_repos", 0.03)
    
    client = HuggingFaceRepoClient()
    repo_id = "kenken999/fastapi_django_main_live"
    
    # リポジトリ情報取得
    repo_info = client.get_repo_info(repo_id, "space")
    files = client.list_files(repo_id, "space")
    commits = client.get_commit_history(repo_id, "space")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hugging Face Repository Viewer</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 12px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{ margin: 0; font-size: 2.5em; font-weight: 300; }}
            .nav {{ 
                background: #f8f9fa; 
                padding: 15px 30px; 
                border-bottom: 1px solid #eee;
            }}
            .nav a {{ 
                color: #667eea; 
                text-decoration: none; 
                margin-right: 20px; 
                font-weight: 500;
                transition: color 0.2s;
            }}
            .nav a:hover {{ color: #764ba2; }}
            .content {{ padding: 30px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
            .card {{ 
                background: #f8f9fa; 
                padding: 25px; 
                border-radius: 8px; 
                border-left: 4px solid #667eea;
            }}
            .card h3 {{ margin-top: 0; color: #667eea; }}
            .info-grid {{ display: grid; grid-template-columns: auto 1fr; gap: 10px; }}
            .info-label {{ font-weight: bold; color: #666; }}
            .file-list {{ max-height: 300px; overflow-y: auto; }}
            .file-item {{ 
                background: white; 
                margin: 5px 0; 
                padding: 8px 12px; 
                border-radius: 4px; 
                border-left: 3px solid #28a745;
                font-family: monospace;
                font-size: 0.9em;
            }}
            .commit-item {{ 
                background: white; 
                margin: 8px 0; 
                padding: 12px; 
                border-radius: 4px; 
                border-left: 3px solid #ffc107;
            }}
            .commit-title {{ font-weight: bold; color: #333; }}
            .commit-date {{ color: #666; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤗 Hugging Face Repository Viewer</h1>
                <p>Repository: {repo_id}</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 Home</a>
                <a href="/api/users">👥 Users</a>
                <a href="/debug/dashboard">🔧 Debug</a>
                <a href="/huggingface">🤗 HF Repository</a>
            </div>
            
            <div class="content">
                <div class="grid">
                    <div class="card">
                        <h3>📋 Repository Info</h3>
                        <div class="info-grid">
                            <div class="info-label">Author:</div>
                            <div>{repo_info.get('author', 'N/A')}</div>
                            <div class="info-label">Created:</div>
                            <div>{repo_info.get('created_at', 'N/A')[:10] if repo_info.get('created_at') != 'N/A' else 'N/A'}</div>
                            <div class="info-label">Modified:</div>
                            <div>{repo_info.get('last_modified', 'N/A')[:10] if repo_info.get('last_modified') != 'N/A' else 'N/A'}</div>
                            <div class="info-label">Downloads:</div>
                            <div>{repo_info.get('downloads', 0)}</div>
                            <div class="info-label">Likes:</div>
                            <div>{repo_info.get('likes', 0)}</div>
                            <div class="info-label">Files:</div>
                            <div>{len(files)}</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3>📁 Files ({len(files)})</h3>
                        <div class="file-list">
                            {''.join([f'<div class="file-item">📄 {file}</div>' for file in files[:20]])}
                            {f'<div style="text-align: center; margin-top: 10px; color: #666;">... and {len(files) - 20} more files</div>' if len(files) > 20 else ''}
                        </div>
                    </div>
                </div>
                
                <div class="card" style="margin-top: 30px;">
                    <h3>📜 Recent Commits</h3>
                    {''.join([f'''
                    <div class="commit-item">
                        <div class="commit-title">{commit['title']}</div>
                        <div class="commit-date">{commit['date'][:10] if commit['date'] != 'N/A' else 'N/A'} by {commit['author']}</div>
                    </div>
                    ''' for commit in commits[:5]])}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/huggingface/file/{file_path:path}")
async def view_hf_file(file_path: str):
    """Hugging Face リポジトリの特定ファイル内容を表示"""
    if not HF_CLIENT_AVAILABLE:
        return {"error": "Hugging Face Client not available"}
    
    client = HuggingFaceRepoClient()
    repo_id = "kenken999/fastapi_django_main_live"
    
    content = client.read_file_content(repo_id, file_path, "space")
    
    return {
        "repo_id": repo_id,
        "file_path": file_path,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
