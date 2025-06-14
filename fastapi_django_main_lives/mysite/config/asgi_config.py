import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from django.conf import settings

def init_django_app(app: FastAPI, application):
    if settings.MOUNT_DJANGO_APP:
        app.mount("/django", application)  # type:ignore
        
        # Django静的ファイルをマウント
        static_dir = "public/staticfiles"
        if os.path.exists(static_dir):
            app.mount("/static", StaticFiles(directory=static_dir), name="static")
            print(f"✅ Django静的ファイルを {static_dir} からマウントしました")
        else:
            print(f"⚠️  警告: {static_dir} ディレクトリが存在しません。collectstaticを実行してください。")
