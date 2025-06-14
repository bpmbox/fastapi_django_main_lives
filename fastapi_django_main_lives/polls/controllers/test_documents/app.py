import gradio as gr
import requests

def create_user(username, password):
    response = requests.post("http://localhost:8000/users/", json={"username": username, "password": password})
    return response.json()

def create_team(name):
    response = requests.post("http://localhost:8000/teams/", json={"name": name})
    return response.json()

def read_users():
    response = requests.get("http://localhost:8000/users/")
    return response.json()

def read_teams():
    response = requests.get("http://localhost:8000/teams/")
    return response.json()

def read_user(user_id):
    response = requests.get(f"http://localhost:8000/users/{user_id}")
    return response.json()

def update_user(user_id, username, profile, tags):
    response = requests.put(f"http://localhost:8000/users/{user_id}", json={"username": username, "profile": profile, "tags": tags})
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
            gr.Markdown("## Team Creation")
            team_name = gr.Textbox(label="Team Name")
            submit_team = gr.Button("Create Team")
            submit_team.click(fn=create_team, inputs=[team_name], outputs="text")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## User List")
            users = gr.Dropdown(label="Users", choices=read_users())
            user_id = gr.Textbox(label="User ID")
            submit_user = gr.Button("Get User")
            submit_user.click(fn=read_user, inputs=[user_id], outputs="text")
        with gr.Column():
            gr.Markdown("## Team List")
            teams = gr.Dropdown(label="Teams", choices=read_teams())
            team_id = gr.Textbox(label="Team ID")
            submit_team = gr.Button("Get Team")
            submit_team.click(fn=read_teams, inputs=[team_id], outputs="text")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Update User")
            user_id = gr.Textbox(label="User ID")
            username = gr.Textbox(label="Username")
            profile = gr.Textbox(label="Profile")
            tags = gr.Textbox(label="Tags")
            submit = gr.Button("Update User")
            submit.click(fn=update_user, inputs=[user_id, username, profile, tags], outputs="text")

demo.launch()