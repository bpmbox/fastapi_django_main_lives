import shutil
import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
import async_timeout
import asyncio


DESCRIPTION = """
<div>
<h1 style="text-align: center;">develop site</h1>
<p>🦕 共同開発 AIシステム設定 LINE開発 CHATGPTS CHATGPTアシスタント設定 AI自動開発設定 APPSHEET GAS PYTHON</p>
</div>
<!-- Start of HubSpot Embed Code -->
  <script type="text/javascript" id="hs-script-loader" async defer src="//js-na1.hs-scripts.com/46277896.js"></script>
<!-- End of HubSpot Embed Code -->
"""

LICENSE = """
<p/>
<!-- Start of HubSpot Embed Code -->
  <script type="text/javascript" id="hs-script-loader" async defer src="//js-na1.hs-scripts.com/46277896.js"></script>
<!-- End of HubSpot Embed Code -->
---
Built with Meta Llama 3
"""

PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <img src="https://ysharma-dummy-chat-app.hf.space/file=/tmp/gradio/8e75e61cc9bab22b7ce3dec85ab0e6db1da5d107/Meta_lockup_positive%20primary_RGB.jpg" style="width: 80%; max-width: 550px; height: auto; opacity: 0.55;  ">
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">Meta llama3</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">Ask me anything...</p>
</div>
"""


# チャットインターフェースの関数定義
# def chat_with_interpreter(message):
#    return "Response: " + message


# カスタムCSSの定義
css = """
.gradio-container {
    height: 100vh; /* 全体の高さを100vhに設定 */
    display: flex;
    flex-direction: column;
}
.gradio-tabs {
    flex: 1; /* タブ全体の高さを最大に設定 */
    display: flex;
    flex-direction: column;
}
.gradio-tab-item {
    flex: 1; /* 各タブの高さを最大に設定 */
    display: flex;
    flex-direction: column;
    overflow: hidden; /* オーバーフローを隠す */
}
.gradio-block {
    flex: 1; /* ブロックの高さを最大に設定 */
    display: flex;
    flex-direction: column;
}
.gradio-chatbot {
    height: 100vh; /* チャットボットの高さを100vhに設定 */
    overflow-y: auto; /* 縦スクロールを有効にする */
}
"""
GENERATION_TIMEOUT_SEC = 60
# Gradio block
chatbot2 = gr.Chatbot(height=450, placeholder=PLACEHOLDER, label="Gradio ChatInterface")

with gr.Blocks(fill_height=True, css=css) as chat:
    # gr.Markdown(DESCRIPTION)
    # gr.DuplicateButton(value="Duplicate Space for private use", elem_id="duplicate-button")
    gr.ChatInterface(
        fn=completion,
        chatbot=chatbot2,
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
        examples=[
            ["HTMLのサンプルを作成して"],
            [
                "CUDA_VISIBLE_DEVICES=0 llamafactory-cli train examples/lora_single_gpu/llama3_lora_sft.yaml"
            ],
        ],
        cache_examples=False,
    )

    gr.Markdown(LICENSE)
