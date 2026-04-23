from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test 1: Health Check (Mocks Redis Ping)
@patch("main.get_redis_client")
def test_health_check(mock_get_redis):
    mock_instance = MagicMock()
    mock_instance.ping.return_value = True
    mock_get_redis.return_value = mock_instance

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Test 2: Create Job (Mocks Redis LPUSH)
@patch("main.get_redis_client")
def test_create_job(mock_get_redis):
    mock_instance = MagicMock()
    mock_get_redis.return_value = mock_instance
    # Mocking the Redis methods to return success
    mock_instance.lpush.return_value = 1
    mock_instance.hset.return_value = 1

    response = client.post("/jobs")
    assert response.status_code == 201
    assert "job_id" in response.json()


# Test 3: Get Job Status (Mocks Redis HGET)
@patch("main.get_redis_client")
def test_get_job_status_success(mock_get_redis):
    mock_instance = MagicMock()
    mock_get_redis.return_value = mock_instance
    mock_instance.hget.return_value = "completed"

    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
