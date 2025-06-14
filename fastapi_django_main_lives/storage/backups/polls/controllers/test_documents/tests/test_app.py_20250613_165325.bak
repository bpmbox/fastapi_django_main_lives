import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "test_user", "password": "test_password"})
    assert response.status_code == 200

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200

def test_create_team():
    response = client.post("/teams/", json={"name": "test_team"})
    assert response.status_code == 200

def test_read_teams():
    response = client.get("/teams/")
    assert response.status_code == 200