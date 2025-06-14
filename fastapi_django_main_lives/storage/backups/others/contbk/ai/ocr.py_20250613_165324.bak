import cv2
import pytesseract
from PIL import Image

class OCR:
    def __init__(self, image_path):
        self.image_path = image_path

    def recognize(self):
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(Image.fromarray(gray))
        return text