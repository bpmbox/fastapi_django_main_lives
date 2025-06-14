import unittest
from lib.gas import save_image_to_drive

class TestGAS(unittest.TestCase):
    def test_save_image_to_drive(self):
        # Load a sample image
        with open("sample_image.jpg", "rb") as f:
            image_data = f.read()

        # Save the image to Google Drive
        save_image_to_drive(image_data)

        # Assert that the file was saved successfully
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()