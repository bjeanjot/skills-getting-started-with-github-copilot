import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- Test récupération des activités ---
def test_get_activities():
    # Arrange
    # (rien à préparer, on utilise l'état initial)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- Test inscription d'un participant ---
def test_signup_participant():
    # Arrange
    email = "testuser1@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup: désinscrire pour ne pas polluer les autres tests
    client.delete(f"/activities/{activity}/unregister?email={email}")

# --- Test double inscription (doit échouer) ---
def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

# --- Test désinscription d'un participant ---
def test_unregister_participant():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

# --- Test désinscription d'un non-inscrit (doit échouer) ---
def test_unregister_non_participant():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]

# --- Test inscription à une activité inexistante (doit échouer) ---
def test_signup_nonexistent_activity():
    # Arrange
    email = "testuser4@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
