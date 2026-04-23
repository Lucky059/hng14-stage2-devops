from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200

def test_submit_job():
    response = client.post("/submit", json={"task": "test-item"})
    assert response.status_code in [200, 201]
