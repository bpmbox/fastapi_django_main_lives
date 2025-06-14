import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

print("Starting minimal ASGI app...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

try:
    application = get_asgi_application()
    print("✓ Django ASGI application created successfully")
except Exception as e:
    print(f"✗ Django ASGI application creation failed: {e}")
    application = None

app = FastAPI()
print("✓ FastAPI application created successfully")

# ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✓ CORS middleware added successfully")

@app.get("/")
def read_root():
    return {"message": "FastAPI + Django app is working!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

print("✓ Basic routes defined successfully")
print("ASGI app setup complete!")
