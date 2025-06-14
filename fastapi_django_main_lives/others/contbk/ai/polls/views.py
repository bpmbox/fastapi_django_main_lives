from django.shortcuts import render
from .models import ImageModel
from .ocr import ocr_extract_text
from googleapiclient.discovery import build
from google.oauth2 import service_account

def index(request):
    if request.method == 'POST':
        image = request.FILES['image']
        img_obj = ImageModel(image=image)
        img_obj.save()
        ocr_text = ocr_extract_text(img_obj.image.path)
        img_obj.ocr_text = ocr_text
        img_obj.save()
        return render(request, 'polls/index.html', {'ocr_text': ocr_text})
    return render(request, 'polls/index.html')

def google_chat_insert(text):
    SCOPES = ['https://www.googleapis.com/auth/chat.service']
    SERVICE_ACCOUNT_FILE = 'path/to/service_account_key.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    chat_service = build('chat', 'v1', credentials=credentials)
    request_body = {'text': text}
    response = chat_service.spaces().messages().create(
        parent='spaces/AAAA', body=request_body).execute()
    print(response)