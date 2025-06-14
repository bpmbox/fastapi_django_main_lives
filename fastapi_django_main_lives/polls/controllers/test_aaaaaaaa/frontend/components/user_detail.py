import gradio as gr

def user_detail(user_id: int):
    with gr.Row():
        with gr.Column():
            gr.Markdown("## User Profile")
            user = []  # Call API to get user
            gr.Textbox(value=user.username)
            gr.Textbox(value=user.profile)
            gr.Button("Edit Profile")