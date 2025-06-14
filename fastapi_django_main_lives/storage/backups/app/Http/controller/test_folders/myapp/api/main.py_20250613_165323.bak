from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from gradio import Interface, outputs
from gradio.inputs import Image
from gradio.outputs import Textbox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pytesseract
import base64
from io import BytesIO
from PIL import Image as PILImage
import sqlite3
from sqlite3 import Error as sqliteError
import logging
from logging.handlers import RotatingFileHandler
import json
import requests

app = FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# SQLite database
engine = create_engine('sqlite:///mydb.db')
Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    result = Column(String)

Base.metadata.create_all(engine)

# Gradio interface
gradio_interface = Interface(
    fn=lambda x: judge(x),
    inputs='image',
    outputs='textbox',
    title='Image Uploader and OCR Judge',
    description='Upload an image and get OCR judgment'
)

# Google Apps Script (GAS) settings
GAS_SERVICE_ACCOUNT_KEY = 'path/to/service_account_key.json'
GAS_CREDENTIALS = service_account_key.json'
GAS_DRIVE_FOLDER_ID = 'folder_id'
GAS_S3_BUCKET_NAME = 'bucket_name'

# OCR keywords
OCR_KEYWORDS = ["", "", "", "", ""]

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    logger.info('Received image upload request')
    image_data = await image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return {'image_base64': image_base64}

@app.post("/judge")
async def judge_image(image_base64: str):
    logger.info('Received image judgment request')
    image_data = base64.b64decode(image_base64)
    image = PILImage.open(BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    if any(keyword in text for keyword in OCR_KEYWORDS):
        result = 'True'
    else:
        result = 'False'
    return {'result': result}

@app.get("/users")
async def get_results():
    logger.info('Received results request')
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results ORDER BY id DESC')
    results = c.fetchall()
    return {'results': results}

@app.get("/docs")
async def get_docs():
    logger.info('Received docs request')
    openapi_schema = get_openapi(title="My API", version="1.0.0")
    html = get_swagger_ui_html(openapi_schema=openapi_schema, title="My API")
    return HTMLResponse(content=html, media_type="text/html")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)