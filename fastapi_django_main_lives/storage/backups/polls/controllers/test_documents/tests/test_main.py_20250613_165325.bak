import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_create_team():
    response = client.post("/teams/", json={"name": "test"})
    assert response.status_code == 200
    assert response.json()["message"] == "Team created successfully"

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_teams():
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_user():
    response = client.put("/users/1", json={"username": "test2", "profile": "test2", "tags": "test2"})
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"