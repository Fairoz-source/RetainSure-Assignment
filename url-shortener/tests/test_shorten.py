import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 201
    data = res.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "invalid-url"})
    assert res.status_code == 500
    assert "error" in res.get_json()

def test_redirect_and_stats(client):
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    data = res.get_json()
    code = data["short_code"]

    res_redirect = client.get(f"/{code}", follow_redirects=False)
    assert res_redirect.status_code == 302

    res_stats = client.get(f"/api/stats/{code}")
    stats = res_stats.get_json()
    assert stats["url"] == "https://google.com"
    assert stats["clicks"] >= 1
    assert "created_at" in stats

def test_404_redirect(client):
    res = client.get("/nonexistent")
    assert res.status_code == 404

def test_404_stats(client):
    res = client.get("/api/stats/invalidcode")
    assert res.status_code == 404
