import pytest
from api.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post("/register", json={"username": "test", "password": "test"})
    assert response.status_code == 200

def test_login_user(client):
    response = client.post("/login", json={"username": "test", "password": "test"})
    assert response.status_code == 200