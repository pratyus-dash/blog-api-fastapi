from app.models import User


def register_user(
    client,
    username,
    email
):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123"
        }
    )


def login_user(
    client,
    username
):
    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_get_my_profile(client):

    register_user(
        client,
        "profileuser",
        "profile@example.com"
    )

    token = login_user(
        client,
        "profileuser"
    )

    response = client.get(
        "/users/me",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "profileuser"
    assert data["email"] == "profile@example.com"
    assert data["is_active"] is True


def test_get_my_profile_requires_authentication(client):

    response = client.get(
        "/users/me"
    )

    assert response.status_code == 401


def test_normal_user_cannot_get_all_users(client):

    register_user(
        client,
        "normaluser",
        "normal@example.com"
    )

    token = login_user(
        client,
        "normaluser"
    )

    response = client.get(
        "/users/",
        headers=headers(token)
    )

    assert response.status_code == 403


def test_admin_can_get_all_users(client, db):

    register_user(
        client,
        "adminuser",
        "admin@example.com"
    )

    user = db.query(User).filter(
        User.username == "adminuser"
    ).first()

    user.is_admin = True
    db.commit()

    token = login_user(
        client,
        "adminuser"
    )

    response = client.get(
        "/users/",
        headers=headers(token)
    )

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1
    assert users[0]["username"] == "adminuser"


def test_admin_can_deactivate_user(client, db):

    register_user(
        client,
        "adminuser",
        "admin@example.com"
    )

    register_user(
        client,
        "targetuser",
        "target@example.com"
    )

    admin = db.query(User).filter(
        User.username == "adminuser"
    ).first()

    target = db.query(User).filter(
        User.username == "targetuser"
    ).first()

    admin.is_admin = True
    db.commit()

    admin_token = login_user(
        client,
        "adminuser"
    )

    response = client.patch(
        f"/users/{target.id}/deactivate",
        headers=headers(admin_token)
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "targetuser"
    assert data["is_active"] is False


def test_admin_can_activate_user(client, db):

    register_user(
        client,
        "adminuser",
        "admin@example.com"
    )

    register_user(
        client,
        "targetuser",
        "target@example.com"
    )

    admin = db.query(User).filter(
        User.username == "adminuser"
    ).first()

    target = db.query(User).filter(
        User.username == "targetuser"
    ).first()

    admin.is_admin = True
    target.is_active = False

    db.commit()

    admin_token = login_user(
        client,
        "adminuser"
    )

    response = client.patch(
        f"/users/{target.id}/activate",
        headers=headers(admin_token)
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "targetuser"
    assert data["is_active"] is True


def test_admin_cannot_deactivate_themselves(client, db):

    register_user(
        client,
        "adminuser",
        "admin@example.com"
    )

    admin = db.query(User).filter(
        User.username == "adminuser"
    ).first()

    admin.is_admin = True
    db.commit()

    admin_token = login_user(
        client,
        "adminuser"
    )

    response = client.patch(
        f"/users/{admin.id}/deactivate",
        headers=headers(admin_token)
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Admin cannot deactivate themselves"
    )


def test_normal_user_cannot_deactivate_user(client, db):

    register_user(
        client,
        "normaluser",
        "normal@example.com"
    )

    register_user(
        client,
        "targetuser",
        "target@example.com"
    )

    normal_token = login_user(
        client,
        "normaluser"
    )

    target = db.query(User).filter(
        User.username == "targetuser"
    ).first()

    response = client.patch(
        f"/users/{target.id}/deactivate",
        headers=headers(normal_token)
    )

    assert response.status_code == 403