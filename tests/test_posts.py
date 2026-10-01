def register_and_login(
    client,
    username="postuser",
    email="postuser@example.com",
    password="password123"
):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": username,
            "password": password
        }
    )

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_post(
    client,
    token,
    title="Test Blog Post",
    content="Test content",
    published=True
):
    return client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published
        },
        headers=auth_headers(token)
    )


def test_create_post(client):

    token = register_and_login(client)

    response = create_post(
        client,
        token
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Blog Post"
    assert data["content"] == "Test content"
    assert data["published"] is True
    assert data["author_id"] == 1


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

    token = register_and_login(client)

    create_post(
        client,
        token,
        title="Public Post",
        content="Public content"
    )

    response = client.get("/posts/")

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "Public Post"


def test_unpublished_posts_are_not_public(client):

    token = register_and_login(client)

    response = create_post(
        client,
        token,
        title="Private Post",
        content="Private content",
        published=False
    )

    assert response.status_code == 201

    response = client.get("/posts/")

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_my_posts(client):

    token = register_and_login(client)

    create_post(
        client,
        token,
        title="My Post",
        content="My content"
    )

    response = client.get(
        "/posts/my",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "My Post"


def test_get_my_posts_requires_authentication(client):

    response = client.get("/posts/my")

    assert response.status_code == 401


def test_get_single_post(client):

    token = register_and_login(client)

    create_response = create_post(
        client,
        token
    )

    post_id = create_response.json()["id"]

    response = client.get(
        f"/posts/{post_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == post_id
    assert data["title"] == "Test Blog Post"


def test_get_nonexistent_post(client):

    response = client.get("/posts/999")

    assert response.status_code == 404


def test_update_own_post(client):

    token = register_and_login(client)

    create_response = create_post(
        client,
        token,
        title="Old Title",
        content="Old content"
    )

    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Title",
            "content": "Updated content",
            "published": True
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_user_cannot_update_another_users_post(client):

    first_token = register_and_login(
        client,
        username="userone",
        email="userone@example.com"
    )

    create_response = create_post(
        client,
        first_token,
        title="User One Post"
    )

    post_id = create_response.json()["id"]

    second_token = register_and_login(
        client,
        username="usertwo",
        email="usertwo@example.com"
    )

    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Hacked Title",
            "content": "Hacked content",
            "published": True
        },
        headers=auth_headers(second_token)
    )

    assert response.status_code == 403


def test_delete_own_post(client):

    token = register_and_login(client)

    create_response = create_post(
        client,
        token,
        title="Delete Me"
    )

    post_id = create_response.json()["id"]

    response = client.delete(
        f"/posts/{post_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Post deleted successfully"
    )


def test_user_cannot_delete_another_users_post(client):

    first_token = register_and_login(
        client,
        username="userone",
        email="userone@example.com"
    )

    create_response = create_post(
        client,
        first_token,
        title="User One Post"
    )

    post_id = create_response.json()["id"]

    second_token = register_and_login(
        client,
        username="usertwo",
        email="usertwo@example.com"
    )

    response = client.delete(
        f"/posts/{post_id}",
        headers=auth_headers(second_token)
    )

    assert response.status_code == 403


def test_search_posts(client):

    token = register_and_login(client)

    create_post(
        client,
        token,
        title="Python FastAPI",
        content="Backend development"
    )

    create_post(
        client,
        token,
        title="JavaScript",
        content="Frontend development"
    )

    response = client.get(
        "/posts/?search=FastAPI"
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 1
    assert posts[0]["title"] == "Python FastAPI"


def test_post_pagination(client):

    token = register_and_login(client)

    for i in range(5):
        create_post(
            client,
            token,
            title=f"Post {i}"
        )

    response = client.get(
        "/posts/?page=1&limit=2"
    )

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 2


def test_invalid_pagination(client):

    response = client.get(
        "/posts/?page=0"
    )

    assert response.status_code == 422