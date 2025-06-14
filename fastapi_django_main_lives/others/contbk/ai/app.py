from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import gradio as gr
from plantuml import PlantUML

app = Flask(__name__)

# Initialize PlantUML
plantuml = PlantUML()

@app.route('/ocr', methods=['POST'])
def ocr():
    img = request.files['image']
    img.save('temp.jpg')
    text = pytesseract.image_to_string(Image.open('temp.jpg'))
    return jsonify({'text': text})

@app.route('/plantuml', methods=['POST'])
def plantuml_diagram():
    code = request.form['code']
    diagram = plantuml.get_svg_string(code)
    return jsonify({'diagram': diagram})

if __name__ == '__main__':
    app.run(debug=True)