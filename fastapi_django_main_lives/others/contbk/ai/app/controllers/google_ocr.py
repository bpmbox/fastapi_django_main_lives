import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def google_ocr(image_path):
    """
    Use Google Apps Script to extract text from an image using OCR
    """
    SCOPES = ['https://www.googleapis.com/auth/script.external_request']
    SERVICE_ACCOUNT_FILE = 'path/to/service_account_key.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, SCOPES)
    service = build('script', 'v1', credentials=credentials)

    with open(image_path, 'rb') as f:
        image_data = f.read()

    request_body = {
        'requests': [
            {
                'image': {
                    'content': image_data
                },
                'features': [
                    {
                        'type': 'TEXT_DETECTION'
                    }
                ]
            }
        ]
    }

    try:
        response = service.scripts().run(body=request_body).execute()
        text = response['responses'][0]['textAnnotations'][0]['description']
        return text
    except HttpError as e:
        print(f'Error: {e}')
        return None