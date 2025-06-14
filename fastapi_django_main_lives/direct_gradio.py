import gradio as gr

def chat_function(message):
    return f"🤖 AI応答: {message}\n\n現在時刻: 2025-06-13\nGradioが正常に動作しています！"

# Gradioインターフェースを作成
demo = gr.Interface(
    fn=chat_function,
    inputs=gr.Textbox(placeholder="メッセージを入力してください..."),
    outputs="text",
    title="💬 Direct Gradio Chat",
    description="直接起動のGradioインターフェース"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
