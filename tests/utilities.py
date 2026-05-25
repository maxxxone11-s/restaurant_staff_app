from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.api.deps import get_db
from tests.db import get_db_for_testing

client = TestClient(app)
app.dependency_overrides[get_db] = get_db_for_testing

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