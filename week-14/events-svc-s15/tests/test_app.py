from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_event():
    response = client.post("/events/", json={
        "name": "Test Event",
        "location": "Test Location"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["location"] == "Test Location"
    assert "id" in data


def test_get_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_event_not_found():
    response = client.get("/events/999")
    assert response.status_code == 404


def test_health():
    response = client.get("/health")
    assert response.status_code == 200