import os
import uuid
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Requirement: Use environment variables for configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

@app.get("/health")
def health_check():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return {"status": "ok", "redis": "connected"}
    except Exception:
        return {"status": "ok", "redis": "disconnected"}

@app.post("/jobs", status_code=201)
def create_job():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    job_id = str(uuid.uuid4())
    r.lpush("job_queue", job_id)
    r.hset(f"job:{job_id}", "status", "pending")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
