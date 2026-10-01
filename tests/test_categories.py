def test_create_category(client):

    response = client.post(
        "/categories/",
        json={
            "name": "Technology"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Technology"


def test_get_categories(client):

    client.post(
        "/categories/",
        json={
            "name": "Technology"
        }
    )

    client.post(
        "/categories/",
        json={
            "name": "Programming"
        }
    )

    response = client.get(
        "/categories/"
    )

    assert response.status_code == 200

    categories = response.json()

    assert len(categories) == 2
    assert categories[0]["name"] == "Technology"
    assert categories[1]["name"] == "Programming"


def test_duplicate_category(client):

    client.post(
        "/categories/",
        json={
            "name": "Technology"
        }
    )

    response = client.post(
        "/categories/",
        json={
            "name": "Technology"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Category already exists"
    )