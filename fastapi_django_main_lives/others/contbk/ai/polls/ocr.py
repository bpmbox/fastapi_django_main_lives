import pytesseract
from PIL import Image

def ocr_extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text