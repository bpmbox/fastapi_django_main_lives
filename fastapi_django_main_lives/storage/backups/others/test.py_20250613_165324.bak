from fastapi import FastAPI
import uvicorn
import asyncio
from pyngrok import ngrok, conf
import threading
#
# 設定
FASTAPI_PORT = 7861
NGROK_AUTHTOKEN = "2fAuM2mXP4rwyzcb6T7EjY8zkL6_4mkaaSLXVpf1enNc8c3Ff"

# FastAPI アプリ
app = FastAPI()

@app.get("/")
def root():
    print("📍 エンドポイント hit!")
    return {"message": "Hello from FastAPI with ngrok!"}

# ngrok 起動スレッド
def start_ngrok():
    conf.get_default().auth_token = NGROK_AUTHTOKEN
    public_url = ngrok.connect(FASTAPI_PORT)
    print(f"🚪 公開URL: {public_url}")

threading.Thread(target=start_ngrok, daemon=True).start()

# 非同期で uvicorn サーバーを起動（VSCodeでも例のエラーが出ない方法）
async def start_server():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=FASTAPI_PORT)
    server = uvicorn.Server(config)
    await server.serve()

# すでにイベントループが動いてるか確認して処理を分ける
try:
    asyncio.get_running_loop().create_task(start_server())
except RuntimeError:
    asyncio.run(start_server())
