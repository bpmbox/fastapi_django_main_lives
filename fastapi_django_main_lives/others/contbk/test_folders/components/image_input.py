import gradio as gr

class ImageInputComponent:
    def __init__(self):
        self.component = gr.Image(label="Image Input")

    def get_value(self):
        return self.component.value