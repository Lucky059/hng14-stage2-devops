from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

# Initialize the TestClient
client = TestClient(app)

# Test 1: Health Check Endpoint
def test_health_check():
    """Test that the health endpoint returns 200 and correct status"""
    # Mocking the redis ping to return True
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

        # We don't need lpush to actually do anything, just not fail
        mock_instance.lpush.return_value = 1
        mock_instance.hset.return_value = 1

        response = client.post("/jobs")
        assert response.status_code == 201
        assert "job_id" in response.json()
        # Verify Redis was called to store the job
        assert mock_instance.lpush.called
        assert mock_instance.hset.called

# Test 3: Get Job Status (Success Case)
def test_get_job_status():
    """Test retrieving a job status from Redis"""
    with patch("main.get_redis_client") as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        # Simulate Redis returning a 'completed' status
        mock_instance.hget.return_value = "completed"

        # Use a fake job ID
        test_id = "12345"
        response = client.get(f"/jobs/{test_id}")

        assert response.status_code == 200
        assert response.json()["job_id"] == test_id
        assert response.json()["status"] == "completed"

# Test 4: Get Job Status (Not Found Case)
def test_get_job_status_not_found():
    """Test that a non-existent job ID returns a 404"""
    with patch("main.get_redis_client") as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance

        # Simulate Redis returning None (job doesn't exist)
        mock_instance.hget.return_value = None

        test_id = "non-existent-id"
        response = client.get(f"/jobs/{test_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
