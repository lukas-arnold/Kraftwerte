import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_read_update_delete_kraftwert():
    # Create
    response = client.post("/kraftwerte/", json={
        "muskelgruppe": "Brust",
        "uebung": "Bankdrücken",
        "gewicht": 80,
        "wiederholungen": 10
    })
    assert response.status_code == 201
    data = response.json()
    assert data["muskelgruppe"] == "Brust"
    kraftwert_id = data["id"]

    # Read one
    response = client.get(f"/kraftwerte/{kraftwert_id}")
    assert response.status_code == 200
    assert response.json()["id"] == kraftwert_id

    # Update
    response = client.put(f"/kraftwerte/{kraftwert_id}", json={
        "muskelgruppe": "Brust",
        "uebung": "Bankdrücken",
        "gewicht": 85,
        "wiederholungen": 8
    })
    assert response.status_code == 200
    data = response.json()
    assert data["gewicht"] == 85

    # Read all
    response = client.get("/kraftwerte/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Delete
    response = client.delete(f"/kraftwerte/{kraftwert_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/kraftwerte/{kraftwert_id}")
    assert response.status_code == 404
