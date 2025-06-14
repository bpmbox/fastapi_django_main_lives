import pytesseract
from PIL import Image
import os

def ocr_image(image_path):
    """
    Extract text from an image using OCR
    """
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text