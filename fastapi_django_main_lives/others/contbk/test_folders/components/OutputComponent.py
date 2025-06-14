import gradio as gr

class OutputComponent:
    """Output component for the Gradio app"""
    def __init__(self, label: str, component_type: gr.Component):
        self.label = label
        self.component = component_type(label=label)