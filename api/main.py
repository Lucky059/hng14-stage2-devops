# api/main.py
from fastapi import FastAPI
import redis
import uuid
import os
from typing import Optional

app = FastAPI()


def get_redis():
    """Create a Redis client on demand to avoid startup blocking."""
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD") or None,
        decode_responses=True
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    r = get_redis()
    job_id = str(uuid.uuid4())
    # push job id to queue and set initial status
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = get_redis()
    status: Optional[str] = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status}

# Alias route so frontend calling /submit also works


@app.post("/submit")
def submit_job():
    return create_job()
