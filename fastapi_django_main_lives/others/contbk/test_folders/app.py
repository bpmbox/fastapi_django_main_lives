import gradio as gr
from components.text_input import TextInputComponent
from components.image_input import ImageInputComponent
from components.output import OutputComponent
from models.model import Model

def main():
    text_input = TextInputComponent()
    image_input = ImageInputComponent()
    output = OutputComponent()

    model = Model()

    demo = gr.Interface(
        fn=model.predict,
        inputs=[text_input.component, image_input.component],
        outputs=output.component,
        title="Gradio App",
        description="An example Gradio app"
    )

    demo.launch()

if __name__ == "__main__":
    main()