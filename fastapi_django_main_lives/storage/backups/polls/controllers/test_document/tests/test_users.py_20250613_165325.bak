from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "test", "password": "test"})
    assert response.status_code == 200

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200

def test_read_user():
    response = client.get("/users/test")
    assert response.status_code == 200