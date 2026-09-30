def create_user_and_login(client):

    client.post(
        "/auth/register",
        json={
            "username": "postuser",
            "email": "postuser@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "postuser",
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def test_create_post(client):

    token = create_user_and_login(
        client
    )

    response = client.post(
        "/posts/",
        json={
            "title": "Test Blog Post",
            "content": "This is test content.",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Blog Post"
    assert data["content"] == "This is test content."
    assert data["published"] is True


def test_create_post_requires_authentication(client):

    response = client.post(
        "/posts/",
        json={
            "title": "Unauthorized Post",
            "content": "This should fail.",
            "published": True
        }
    )

    assert response.status_code == 401


def test_get_published_posts(client):

    token = create_user_and_login(
        client
    )

    client.post(
        "/posts/",
        json={
            "title": "Public Post",
            "content": "Public content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/posts/"
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "Public Post"


def test_get_my_posts(client):

    token = create_user_and_login(
        client
    )

    client.post(
        "/posts/",
        json={
            "title": "My Post",
            "content": "My content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/posts/my",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "My Post"


def test_update_own_post(client):

    token = create_user_and_login(
        client
    )

    create_response = client.post(
        "/posts/",
        json={
            "title": "Old Title",
            "content": "Old content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Title",
            "content": "Updated content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_delete_own_post(client):

    token = create_user_and_login(
        client
    )

    create_response = client.post(
        "/posts/",
        json={
            "title": "Delete Me",
            "content": "Delete this post",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    post_id = create_response.json()["id"]

    response = client.delete(
        f"/posts/{post_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Post deleted successfully"
    )


def test_search_posts(client):

    token = create_user_and_login(
        client
    )

    client.post(
        "/posts/",
        json={
            "title": "Python FastAPI",
            "content": "Backend development",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/posts/?search=FastAPI"
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "Python FastAPI"