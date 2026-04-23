import pytest
from fastapi.testclient import TestClient
from main import app
import redis
import fakeredis

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    """
    Since your code calls redis.Redis(host=...) inside every function,
    we must mock the 'redis.Redis' class itself to return a fake client.
    """
    fake_red = fakeredis.FakeRedis(decode_responses=True)
    
    # This replaces the redis.Redis class constructor with our fake instance
    monkeypatch.setattr(redis, "Redis", lambda **kwargs: fake_red)
    return fake_red

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    # Your code returns {"status": "ok", "redis": "connected"} when ping works
    assert response.json()["status"] == "ok"

def test_create_job():
    # Your code uses @app.post("/jobs")
    response = client.post("/jobs")
    assert response.status_code == 201
    assert "job_id" in response.json()

def test_get_job_not_found():
    # Testing the 404 logic in your @app.get("/jobs/{job_id}")
    response = client.get("/jobs/non-existent-id")
    assert response.status_code == 404
