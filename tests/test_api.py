from tests.utilities import register_user, login_user, create_test_user_data

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

def test_register(client):
    email, password = create_test_user_data()

    response = register_user(client, email, password)
    data = response.json()

    assert data['email'] == email
    assert response.status_code == 200
    

def test_login(client):
    email, password = create_test_user_data()
    register_user(client, email, password)

    response = login_user(client, email, password)
    data = response.json()

    assert data["access_token"] is not None
    assert data["token_type"] == 'bearer'

def test_all_user_cycle(client):
    email, password = create_test_user_data()
    register_user(client, email, password)
    response_login = login_user(client, email, password)

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

def test_staff_me(client):
    response = client.get(
        "/staff/me"
    )

    assert response.status_code == 401