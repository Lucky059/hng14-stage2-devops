import os
import uuid
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Configuration from Environment Variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Initialize a global Redis client
# This allows the unit tests to monkeypatch the connection easily
redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD, 
    decode_responses=True
)

@app.get("/health")
def health_check():
    """Checks the health of the API and its connection to Redis."""
    try:
        redis_client.ping()
        return {"status": "ok", "redis": "connected"}
    except Exception:
        # We report 'ok' for the API but 'disconnected' for Redis 
        # to prevent unnecessary container restarts during testing.
        return {"status": "ok", "redis": "disconnected"}

@app.post("/jobs", status_code=201)
def create_job():
    """Creates a new job and pushes it to the Redis queue."""
    job_id = str(uuid.uuid4())
    try:
        redis_client.lpush("job_queue", job_id)
        redis_client.hset(f"job:{job_id}", "status", "pending")
        return {"job_id": job_id}
    except Exception as e:
        # If the database fails, return a 500
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    """Retrieves the status of a specific job."""
    # 1. Fetch from Redis
    try:
        status = redis_client.hget(f"job:{job_id}", "status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 2. Return 404 if the job doesn't exist
    # This must be outside the try/except to avoid being caught as a 500
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": status}
