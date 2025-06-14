import logging
from appscript import AppScript
from ocr import OCR

logging.basicConfig(level=logging.INFO)

def main():
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/credentials.json')
    appscript = AppScript(credentials)

    image_path = 'path/to/image.jpg'
    ocr = OCR(image_path)
    img_ocr = ocr.recognize()

    if img_ocr:
        appscript.loggers(f'////////⭐️⭐️⭐️⭐️ Bot_gas_main_dev 個人情報の確認{img_ocr}')
        appscript.google_chat_insert(f'///////⭐️⭐️⭐️⭐️個人情報の確認{img_ocr}')

if __name__ == '__main__':
    main()