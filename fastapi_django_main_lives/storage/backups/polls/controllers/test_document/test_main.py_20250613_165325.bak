import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post("/register", json={"username": "test", "password": "test"})
    assert response.status_code == 200

def test_login(client):
    response = client.post("/login", json={"username": "test", "password": "test"})
    assert response.status_code == 200

def test_get_teams(client):
    response = client.get("/teams")
    assert response.status_code == 200

def test_create_team(client):
    response = client.post("/teams", json={"name": "test team"})
    assert response.status_code == 200

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200

def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200

def test_update_user(client):
    response = client.put("/users/1", json={"profile": "test profile", "team_id": 1})
    assert response.status_code == 200