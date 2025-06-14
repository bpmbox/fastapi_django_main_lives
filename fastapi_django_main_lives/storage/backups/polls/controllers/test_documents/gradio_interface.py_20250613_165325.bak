import gradio as gr
import requests

def create_user(username, password):
    response = requests.post("http://localhost:8000/users/", json={"name": username, "password": password})
    return response.json()

def read_users():
    response = requests.get("http://localhost:8000/users/")
    return response.json()

def create_team(team_name):
    response = requests.post("http://localhost:8000/teams/", json={"name": team_name})
    return response.json()

def read_teams():
    response = requests.get("http://localhost:8000/teams/")
    return response.json()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("## User Registration")
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            submit = gr.Button("Register")
            submit.click(fn=create_user, inputs=[username, password], outputs="text")
        with gr.Column():
            gr.Markdown("## User List")
            users = gr.Dataframe()
            refresh = gr.Button("Refresh")
            refresh.click(fn=read_users, outputs=users)
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Team Creation")
            team_name = gr.Textbox(label="Team Name")
            submit = gr.Button("Create Team")
            submit.click(fn=create_team, inputs=[team_name], outputs="text")
        with gr.Column():
            gr.Markdown("## Team List")
            teams = gr.Dataframe()
            refresh = gr.Button("Refresh")
            refresh.click(fn=read_teams, outputs=teams)