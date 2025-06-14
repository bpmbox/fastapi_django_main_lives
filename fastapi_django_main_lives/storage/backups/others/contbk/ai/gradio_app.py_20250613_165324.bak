import gradio as gr
from app import app

with gr.Blocks() as demo:
    img = gr.Image(type="pil")
    btn = gr.Button("Run OCR")
    txt = gr.Textbox(label="Extracted Text")
    plantuml_code = gr.Textbox(label="PlantUML Code")
    plantuml_diagram = gr.Image(type="pil")

    def ocr(img):
        response = app.post('/ocr', files={'image': img})
        return response.json()['text']

    def plantuml_diagram(code):
        response = app.post('/plantuml', data={'code': code})
        return response.json()['diagram']

    btn.click(ocr, inputs=img, outputs=txt)
    btn.click(plantuml_diagram, inputs=plantuml_code, outputs=plantuml_diagram)

demo.launch()