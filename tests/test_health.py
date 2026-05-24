from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200

def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "test12345678@gmail.com",
            "password": "test123test",
            "full_name": "test",
            "restaurant_name": "testtest",
            "position": "default"
        }
    )

    data = response.json()

    assert data['email'] == "test12345678@gmail.com"
    assert response.status_code == 200
    

def test_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "test12@gmail.com",
            "password": "test123test"
        }
    )

    data = response.json()

    assert data["access_token"] is not None
    assert data["token_type"] == 'bearer'