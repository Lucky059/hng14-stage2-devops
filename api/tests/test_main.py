from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
# We import app directly; PYTHONPATH in CI will handle the location
from main import app

client = TestClient(app)


# Test 1: Health Check Endpoint
def test_health_check():
    """Test that the health endpoint returns 200 and correct status"""
    with patch("main.get_redis_client") as mock_redis:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock_redis.return_value = mock_instance

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# Test 2: Create Job Endpoint
def test_create_job():
    """Test creating a job adds it to Redis and returns a job_id"""
    with patch("main.get_redis_client") as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        mock_instance.lpush.return_value = 1
        mock_instance.hset.return_value = 1

        response = client.post("/jobs")
        assert response.status_code == 201
        assert "job_id" in response.json()


# Test 3: Get Job Status (Not Found Case)
def test_get_job_status_not_found():
    """Test that a non-existent job ID returns a 404"""
    with patch("main.get_redis_client") as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        mock_instance.hget.return_value = None

        response = client.get("/jobs/non-existent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
