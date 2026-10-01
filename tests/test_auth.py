def register_user(
    client,
    username="testuser",
    email="testuser@example.com",
    password="password123"
):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def login_user(
    client,
    username="testuser",
    password="password123"
):
    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": password
        }
    )

    return response


def test_register_user(client):

    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True
    assert data["is_admin"] is False


def test_duplicate_username(client):

    first_response = register_user(client)

    assert first_response.status_code == 201

    second_response = register_user(
        client,
        email="another@example.com"
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Username already exists"
    )


def test_duplicate_email(client):

    first_response = register_user(client)

    assert first_response.status_code == 201

    second_response = register_user(
        client,
        username="anotheruser"
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Email already exists"
    )


def test_login(client):

    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    register_user(client)

    response = login_user(
        client,
        password="wrongpassword"
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):

    response = login_user(
        client,
        username="doesnotexist"
    )

    assert response.status_code == 401


def test_protected_route_requires_authentication(client):

    response = client.get(
        "/protected"
    )

    assert response.status_code == 401


def test_protected_route_with_valid_token(client):

    register_user(client)

    login_response = login_user(client)

    token = login_response.json()["access_token"]

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["user_id"] == 1


def test_register_password_is_hashed(client, db):

    register_user(client)

    from app.models import User

    user = db.query(User).filter(
        User.username == "testuser"
    ).first()

    assert user is not None
    assert user.hashed_password != "password123"


def test_short_password_validation(client):

    response = register_user(
        client,
        password="123"
    )

    assert response.status_code == 422