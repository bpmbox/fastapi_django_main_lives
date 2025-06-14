import gradio as gr

def display_html():
    html_content = """
    <h1>Hello, Gradio!</h1>
    <p>This is an example of displaying HTML content using Gradio.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
        <a href="test">aaa</a>
    </ul>
    """
    return html_content

# Gradioのインターフェースを作成
gradio_interfaces = gr.Interface(
    fn=display_html,  # HTMLコンテンツを返す関数
    inputs=[],  # 入力なし
    outputs=gr.HTML()  # HTMLコンテンツを表示
)


# Gradioのインターフェースを作成
with gr.Blocks() as gradio_interface:
    gr.HTML(display_html())
# インターフェースを起動
#iface.launch()
