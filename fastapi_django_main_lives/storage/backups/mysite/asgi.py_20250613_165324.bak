import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.cors import CORSMiddleware

import gradio as gr
from mysite.routers.gradio import setup_gradio_interfaces
from mysite.routers.fastapi import setup_webhook_routes,include_routers
from mysite.routers.database import setup_database_routes
from mysite.config.asgi_config import init_django_app
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
# ロガーの設定
from mysite.logger import logger
import threading
import aiofiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_asgi_application()

app = FastAPI()

# Djangoアプリケーションの初期化
init_django_app(app, application)

# ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gradioインターフェースの設定
gradio_interfaces = setup_gradio_interfaces()

## Webhookルートの設定
include_routers(app)
setup_webhook_routes(app)

# データベースルートの設定
setup_database_routes(app)



# Gradioアプリのマウント
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# テンプレートファイルが格納されているディレクトリを指定
templates = Jinja2Templates(directory="templates")

@app.get("/tests")
def get_some_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app = gr.mount_gradio_app(app, gradio_interfaces, "/")



def run_gradio():
    gradio_interfaces.launch(server_name="0.0.0.0", server_port=7861, share=True)
    #iface_2.launch(server_name="0.0.0.0", server_port=7861, share=True)

#threading.Thread(target=run_gradio).start()



