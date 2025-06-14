from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_team():
    response = client.post("/teams/", json={"name": "test"})
    assert response.status_code == 200

def test_read_teams():
    response = client.get("/teams/")
    assert response.status_code == 200