import unittest
from lib.ocr import ocr_image

class TestOCR(unittest.TestCase):
    def test_ocr_image(self):
        # Load a sample image
        with open("sample_image.jpg", "rb") as f:
            image_data = f.read()

        # Perform OCR on the image
        text = ocr_image(image_data)

        # Assert that the OCR result is not empty
        self.assertIsNotNone(text)

if __name__ == "__main__":
    unittest.main()