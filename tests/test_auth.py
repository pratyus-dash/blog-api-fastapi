def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True
    assert data["is_admin"] is False


def test_duplicate_username(client):

    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "password123"
        }
    )

    assert second_response.status_code == 400


def test_login(client):

    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_protected_route_requires_authentication(client):

    response = client.get(
        "/protected"
    )

    assert response.status_code == 401


def test_protected_route_with_valid_token(client):

    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"