from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_create_team():
    response = client.post("/teams/", json={"name": "testteam"})
    assert response.status_code == 200
    assert response.json()["message"] == "Team created successfully"

def test_read_teams():
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) > 0