import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# (Keep your existing test functions below)

# 1. Trending API Verification
def test_get_trending_success():
    response = client.get("/trending?limit=3")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert len(json_data["data"]) == 3
    assert json_data["data"][0]["popularity_score"] >= json_data["data"][1]["popularity_score"]

def test_get_trending_validation_error():
    response = client.get("/trending?limit=0")
    assert response.status_code == 422

# 2. Customer Profile Verification
def test_get_customer_profile_success():
    response = client.get("/customers/CUST_10")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Mokshitha"

def test_get_customer_profile_not_found():
    response = client.get("/customers/UNKNOWN_USER")
    assert response.status_code == 404

# 3. Customer Activity Aggregation Tree Verification
def test_get_customer_activity_active():
    response = client.get("/customers/CUST_10/activity")
    assert response.status_code == 200
    data = response.json()
    assert data["has_activity"] is True
    assert "recommendations" in data["data"]
    assert "feedback" in data["data"]

def test_get_customer_activity_cold_start():
    response = client.get("/customers/CUST_999/activity")
    assert response.status_code == 200
    assert response.json()["has_activity"] is False

# 4. Similar Articles Verification
def test_get_similar_articles_success():
    response = client.get("/articles/0108775015/similar?limit=2")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2

def test_get_similar_articles_not_found():
    response = client.get("/articles/NON_EXISTENT_ID/similar")
    assert response.status_code == 404

# 5. Personalized Recommendation Verification
def test_get_personalized_active_user():
    response = client.get("/personalized/CUST_10?limit=2")
    assert response.status_code == 200
    assert response.json()["is_fallback"] is False

def test_get_personalized_cold_start():
    response = client.get("/personalized/CUST_999?limit=2")
    assert response.status_code == 200
    assert response.json()["is_fallback"] is True