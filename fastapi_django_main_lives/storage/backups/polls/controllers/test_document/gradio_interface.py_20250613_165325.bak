import gradio as gr
import requests

def register_user(username, password):
    response = requests.post("http://localhost:8000/register", json={"username": username, "password": password})
    return response.json()

def login_user(username, password):
    response = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
    return response.json()

def get_teams():
    response = requests.get("http://localhost:8000/teams")
    return response.json()

def create_team(name):
    response = requests.post("http://localhost:8000/teams", json={"name": name})
    return response.json()

def get_users():
    response = requests.get("http://localhost:8000/users")
    return response.json()

def get_user(user_id):
    response = requests.get(f"http://localhost:8000/users/{user_id}")
    return response.json()

def update_user(user_id, team_id, profile, tags):
    response = requests.put(f"http://localhost:8000/users/{user_id}", json={"team_id": team_id, "profile": profile, "tags": tags})
    return response.json()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("Register")
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            register_button = gr.Button("Register")
            register_button.click(register_user, inputs=[username, password], outputs="text")
        with gr.Column():
            gr.Markdown("Login")
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            login_button = gr.Button("Login")
            login_button.click(login_user, inputs=[username, password], outputs="text")

    with gr.Row():
        with gr.Column():
            gr.Markdown("Teams")
            team_name = gr.Textbox(label="Team Name")
            create_team_button = gr.Button("Create Team")
            create_team_button.click(create_team, inputs=[team_name], outputs="text")
            teams = gr.Dataframe(label="Teams")
            get_teams_button = gr.Button("Get Teams")
            get_teams_button.click(get_teams, outputs=[teams])

    with gr.Row():
        with gr.Column():
            gr.Markdown("Users")
            user_id = gr.Textbox(label="User ID")
            get_user_button = gr.Button("Get User")
            get_user_button.click(get_user, inputs=[user_id], outputs="text")
            users = gr.Dataframe(label="Users")
            get_users_button = gr.Button("Get Users")
            get_users_button.click(get_users, outputs=[users])

    with gr.Row():
        with gr.Column():
            gr.Markdown("Update User")
            user_id = gr.Textbox(label="User ID")
            team_id = gr.Textbox(label="Team ID")
            profile = gr.Textbox(label="Profile")
            tags = gr.Textbox(label="Tags")
            update_button = gr.Button("Update")
            update_button.click(update_user, inputs=[user_id, team_id, profile, tags], outputs="text")

demo.launch()