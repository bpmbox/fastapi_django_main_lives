from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from django.conf import settings

def init_django_app(app: FastAPI, application):
    if settings.MOUNT_DJANGO_APP:
        app.mount("/django", application)  # type:ignore
        app.mount("/static", StaticFiles(directory="staticfiles"), name="static")
