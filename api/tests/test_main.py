
import pytest
from fastapi.testclient import TestClient
import fakeredis
# Correct import: pull the objects from the main module
from main import app, redis_client 

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_redis_mock(monkeypatch):
    """
    This fixture runs before every test. It replaces the real Redis 
    client with a fake one that lives in your computer's memory.
    """
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    # Target 'main.redis_client' specifically to intercept the connection
    monkeypatch.setattr("main.redis_client", fake_redis)

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_job():
    # Tests the POST route for job creation
    response = client.post("/jobs")
    assert response.status_code == 201
    assert "job_id" in response.json()

def test_get_job_not_found():
    # Tests the 404 logic for missing jobs
    response = client.get("/jobs/non-existent-uuid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
