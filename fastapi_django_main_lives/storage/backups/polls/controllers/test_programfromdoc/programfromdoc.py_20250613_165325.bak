import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb

gradio_interface = gr.Interface(
    fn=process_file,
    inputs=[
        "file",
        gr.Textbox(label="Additional Notes", lines=10),
        gr.Textbox(label="Folder Name"),
    ],
    outputs="text",
)