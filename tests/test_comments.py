def register_and_login(
    client,
    username,
    email
):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def create_post(client, token):

    response = client.post(
        "/posts/",
        json={
            "title": "Comment Test Post",
            "content": "Post content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response.json()["id"]


def test_create_comment(client):

    token = register_and_login(
        client,
        "commentuser",
        "comment@example.com"
    )

    post_id = create_post(
        client,
        token
    )

    response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "Great post!"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "Great post!"
    assert data["post_id"] == post_id
    assert data["author_id"] == 1


def test_create_comment_requires_authentication(client):

    token = register_and_login(
        client,
        "postuser",
        "post@example.com"
    )

    post_id = create_post(
        client,
        token
    )

    response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "Unauthorized comment"
        }
    )

    assert response.status_code == 401


def test_get_post_comments(client):

    token = register_and_login(
        client,
        "commentuser",
        "comment@example.com"
    )

    post_id = create_post(
        client,
        token
    )

    client.post(
        f"/comments/{post_id}",
        json={
            "content": "First comment"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    client.post(
        f"/comments/{post_id}",
        json={
            "content": "Second comment"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        f"/comments/post/{post_id}"
    )

    assert response.status_code == 200

    comments = response.json()

    assert len(comments) == 2
    assert comments[0]["content"] == "First comment"
    assert comments[1]["content"] == "Second comment"


def test_delete_own_comment(client):

    token = register_and_login(
        client,
        "commentuser",
        "comment@example.com"
    )

    post_id = create_post(
        client,
        token
    )

    create_response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "Delete this comment"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    comment_id = create_response.json()["id"]

    response = client.delete(
        f"/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Comment deleted successfully"
    )


def test_user_cannot_delete_another_users_comment(client):

    first_token = register_and_login(
        client,
        "userone",
        "userone@example.com"
    )

    post_id = create_post(
        client,
        first_token
    )

    comment_response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "User one comment"
        },
        headers={
            "Authorization": f"Bearer {first_token}"
        }
    )

    comment_id = comment_response.json()["id"]

    second_token = register_and_login(
        client,
        "usertwo",
        "usertwo@example.com"
    )

    response = client.delete(
        f"/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {second_token}"
        }
    )

    assert response.status_code == 403


def test_comment_on_nonexistent_post(client):

    token = register_and_login(
        client,
        "commentuser",
        "comment@example.com"
    )

    response = client.post(
        "/comments/999",
        json={
            "content": "This should fail"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404