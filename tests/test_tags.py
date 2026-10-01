def test_create_tag(client):

    response = client.post(
        "/tags/",
        json={
            "name": "FastAPI"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "FastAPI"


def test_get_tags(client):

    client.post(
        "/tags/",
        json={
            "name": "FastAPI"
        }
    )

    client.post(
        "/tags/",
        json={
            "name": "Python"
        }
    )

    response = client.get(
        "/tags/"
    )

    assert response.status_code == 200

    tags = response.json()

    assert len(tags) == 2
    assert tags[0]["name"] == "FastAPI"
    assert tags[1]["name"] == "Python"


def test_duplicate_tag(client):

    client.post(
        "/tags/",
        json={
            "name": "FastAPI"
        }
    )

    response = client.post(
        "/tags/",
        json={
            "name": "FastAPI"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Tag already exists"
    )