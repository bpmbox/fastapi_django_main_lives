import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_login_user():
    response = client.post("/login", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert response.json()["message"] == "Logged in successfully"

def test_get_teams():
    response = client.get("/teams")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_team():
    response = client.post("/teams", json={"name": "Test Team"})
    assert response.status_code == 200
    assert response.json()["message"] == "Team created successfully"

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "test"

def test_update_user():
    response = client.put("/users/1", json={"team_id": 1, "profile": "Test Profile", "tags": "Test Tags"})
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"