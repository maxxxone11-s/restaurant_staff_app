from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.api.deps import get_db
from tests.db import get_db_for_testing

app.dependency_overrides[get_db] = get_db_for_testing

client = TestClient(app)

def create_test_user_data():
    email = f"test_{uuid4().hex}@gmail.com"
    password = "test123test"
    return email, password

def register_user(email, password):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "test",
            "restaurant_name": "testtest",
            "position": "default"
        }
    )

    return response

def login_user(email, password):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    return response

def test_health():
    response = client.get("/health")

    assert response.status_code == 200

def test_register():
    email, password = create_test_user_data()

    response = register_user(email, password)
    data = response.json()

    assert data['email'] == email
    assert response.status_code == 200
    

def test_login():
    email, password = create_test_user_data()
    register_user(email, password)

    response = login_user(email, password)
    data = response.json()

    assert data["access_token"] is not None
    assert data["token_type"] == 'bearer'

def test_all_user_cycle():
    email, password = create_test_user_data()
    register_user(email, password)
    response_login = login_user(email, password)

    data_login = response_login.json()
    access_token = data_login["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data_token = response.json()

    assert response.status_code == 200
    assert data_token["email"] == email
