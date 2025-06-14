import os
from lib.ocr import ocr_image
from lib.line_dev import send_image
from lib.gas import save_image_to_drive

def main():
    # Load image from AppSheet QA
    image_data = load_image_from_appsheet_qa()

    # Perform OCR on the image
    text = ocr_image(image_data)

    # Send the OCR result to Line Dev
    send_image(text)

    # Save the image to Google Drive using GAS
    save_image_to_drive(image_data)

if __name__ == "__main__":
    main()