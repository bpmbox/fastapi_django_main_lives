import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "test", "password": "test"})
    assert response.status_code == 200

def test_login():
    response = client.post("/login/", json={"name": "test", "password": "test"})
    assert response.status_code == 200

def test_get_teams():
    response = client.get("/teams/")
    assert response.status_code == 200

def test_create_team():
    response = client.post("/teams/", json={"name": "test"})
    assert response.status_code == 200

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200

def test_update_user():
    response = client.put("/users/1", json={"name": "test", "profile": "test", "tags": "test"})
    assert response.status_code == 200