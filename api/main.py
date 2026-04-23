import os
import uuid
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Requirement: Use environment variables for configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Define the client globally so the test suite can intercept it
redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD, 
    decode_responses=True
)

@app.get("/health")
def health_check():
    try:
        redis_client.ping()
        return {"status": "ok", "redis": "connected"}
    except Exception:
        # We return 200/ok even if redis is down so the container doesn't 
        # restart during transient network blips, but report the status.
        return {"status": "ok", "redis": "disconnected"}

@app.post("/jobs", status_code=201)
def create_job():
    job_id = str(uuid.uuid4())
    try:
        redis_client.lpush("job_queue", job_id)
        redis_client.hset(f"job:{job_id}", "status", "pending")
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = redis_client.hget(f"job:{job_id}", "status")
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job_id": job_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
