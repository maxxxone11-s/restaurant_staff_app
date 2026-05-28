from uuid import uuid4

def create_test_user_data():
    email = f"test_{uuid4().hex}@gmail.com"
    password = "test123test"
    return email, password

def register_user(client, email, password):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "test",
            "restaurant_name": "testtest",
            "position": "default"
        }
    )

def login_user(client, email, password):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )