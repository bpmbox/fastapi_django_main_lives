import os
from PIL import Image
from io import BytesIO

class ImageSaver:
    def __init__(self, image_data):
        self.image_data = image_data

    def save_image(self, file_path):
        image = Image.open(BytesIO(self.image_data))
        image.save(file_path)