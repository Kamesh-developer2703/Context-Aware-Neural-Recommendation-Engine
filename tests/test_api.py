import requests

BASE_URL = "http://127.0.0.1:8000"


def test_recommendations():
    response = requests.get(
        f"{BASE_URL}/recommendations",
        params={"limit": 10},
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "recommendations" in data
    assert data["total"] <= 10


def test_customer_recommendations():
    response = requests.get(
        f"{BASE_URL}/recommendations/1",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == 1
    assert "recommendations" in data


def test_invalid_customer():
    response = requests.get(
        f"{BASE_URL}/recommendations/999999",
        timeout=10,
    )

    assert response.status_code == 404


def test_add_favorite():
    response = requests.post(
        f"{BASE_URL}/favorites",
        json={"article_id": 999},
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["article_id"] == 999


def test_get_favorites():
    response = requests.get(
        f"{BASE_URL}/favorites",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "favorites" in data


def test_duplicate_favorite():
    # Article 999 was added in the previous test
    response = requests.post(
        f"{BASE_URL}/favorites",
        json={"article_id": 999},
        timeout=10,
    )

    assert response.status_code == 409


def test_delete_favorite():
    response = requests.delete(
        f"{BASE_URL}/favorites/999",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["article_id"] == 999


def test_delete_missing_favorite():
    response = requests.delete(
        f"{BASE_URL}/favorites/999",
        timeout=10,
    )

    assert response.status_code == 404
def test_invalid_favorite_article():
    response = requests.post(
        f"{BASE_URL}/favorites",
        json={"article_id": -1},
        timeout=10,
    )

    assert response.status_code == 422