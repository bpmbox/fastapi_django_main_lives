import gradio as gr

def team_list():
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Team List")
            teams = []  # Call API to get teams
            for team in teams:
                with gr.Row():
                    gr.Textbox(value=team.name)
                    gr.Button("View Team")