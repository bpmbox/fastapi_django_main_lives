import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb

def format_response(chunk, full_response):
    # Message
    if chunk["type"] == "message":
        full_response += chunk.get("content", "")
        if chunk.get("end", False):
            full_response += "\n"

    # Code
    if chunk["type"] == "code":
        if chunk.get("start", False):
            full_response += "```python\n"
        full_response += chunk.get("content", "").replace("`", "")
        if chunk.get("end", False):
            full_response += "\n```\n"

    # Output
    if chunk["type"] == "confirmation":
        if chunk.get("start", False):
            full_response += "```python\n"
        full_response += chunk.get("content", {}).get("code", "")
        if chunk.get("end", False):
            full_response += "```\n"

    # Console
    if chunk["type"] == "console":
        if chunk.get("start", False):
            full_response += "```python\n"
        if chunk.get("format", "") == "active_line":
            console_content = chunk.get("content", "")
            if console_content is None:
                full_response += "No output available on console."
        if chunk.get("format", "") == "output":
            console_content = chunk.get("content", "")
            full_response += console_content
        if chunk.get("end", False):
            full_response += "\n```\n"

    # Image
    if chunk["type"] == "image":
        if chunk.get("start", False) or chunk.get("end", False):
            full_response += "\n"
        else:
            image_format = chunk.get("format", "")
            if image_format == "base64.png":
                image_content = chunk.get("content", "")
                if image_content:
                    image = Image.open(BytesIO(base64.b64decode(image_content)))
                    new_image = Image.new("RGB", image.size, "white")
                    new_image.paste(image, mask=image.split()[3])
                    buffered = BytesIO()
                    new_image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    full_response += f"![Image](data:image/png;base64,{img_str})\n"

    return full_response


# Set the environment variable.
def chat_with_interpreter(
    message, history, a=None, b=None, c=None, d=None
):  # , openai_api_key):
    # Set the API key for the interpreter
    # interpreter.llm.api_key = openai_api_key

    if message == "reset":
        interpreter.messages = []
        interpreter.reset()
        return "Interpreter reset", history
    full_response = ""
    # add_conversation(history,20)
    user_entry = {"role": "user", "type": "message", "content": message}
    #messages.append(user_entry)
    # Call interpreter.chat and capture the result
    # message = message + "\nシンタックスを確認してください。"
    # result = interpreter.chat(message)
    for chunk in interpreter.chat(message, display=False, stream=True):
        # print(chunk)
        # output = '\n'.join(item['content'] for item in result if 'content' in item)
        full_response = format_response(chunk, full_response)
        yield full_response  # chunk.get("content", "")
    no_process_file(message,"ai")
    # Extract the 'content' field from all elements in the result

    yield full_response
    return full_response, history

PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <img src="https://ysharma-dummy-chat-app.hf.space/file=/tmp/gradio/8e75e61cc9bab22b7ce3dec85ab0e6db1da5d107/Meta_lockup_positive%20primary_RGB.jpg" style="width: 80%; max-width: 550px; height: auto; opacity: 0.55;  ">
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">Meta llama3</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">Ask me anything...</p>
</div>
"""

chatbot = gr.Chatbot(height=650, placeholder=PLACEHOLDER, label="Gradio ChatInterface")



gradio_interface = gr.ChatInterface(
    fn=chat_with_interpreter,
    chatbot=chatbot,
    fill_height=True,
    additional_inputs_accordion=gr.Accordion(
        label="⚙️ Parameters", open=False, render=False
    ),
    additional_inputs=[
        gr.Slider(
            minimum=0,
            maximum=1,
            step=0.1,
            value=0.95,
            label="Temperature",
            render=False,
        ),
        gr.Slider(
            minimum=128,
            maximum=4096,
            step=1,
            value=512,
            label="Max new tokens",
            render=False,
        ),
    ],
    # democs,
    examples=[
        ["HTMLのサンプルを作成して"],
        [
            "CUDA_VISIBLE_DEVICES=0 llamafactory-cli train examples/lora_single_gpu/llama3_lora_sft.yaml"
        ],
    ],
    cache_examples=False,
)
