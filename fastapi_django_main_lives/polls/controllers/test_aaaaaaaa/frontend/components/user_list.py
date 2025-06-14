import gradio as gr

def user_list():
    with gr.Row():
        with gr.Column():
            gr.Markdown("## User List")
            users = []  # Call API to get users
            for user in users:
                with gr.Row():
                    gr.Textbox(value=user.username)
                    gr.Textbox(value=user.profile)
                    gr.Button("View Profile")