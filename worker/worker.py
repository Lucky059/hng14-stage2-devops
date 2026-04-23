import os
import time
import redis
import logging

# Setup logging to see what's happening in the container logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker")

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)


def get_redis_client():
    # BUG FIX: Handle empty strings to avoid AuthenticationError
    pwd = REDIS_PASSWORD if REDIS_PASSWORD and REDIS_PASSWORD.strip() != "" else None

    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=pwd,
        decode_responses=True
    )


def process_worker():
    logger.info(f"Worker connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")

    while True:
        try:
            r = get_redis_client()
            # We use 'job_queue' to match the updated main.py logic
            # brpop blocks until a job is available
            job = r.brpop("job_queue", timeout=5)

            if job:
                job_id = job[1]
                logger.info(f"Processing job: {job_id}")

                # Simulate work
                r.hset(f"job:{job_id}", "status", "processing")
                time.sleep(2)  # Simulate task duration

                r.hset(f"job:{job_id}", "status", "completed")
                logger.info(f"Job {job_id} completed successfully.")

        except redis.AuthenticationError:
            logger.error("Authentication failed! Check REDIS_PASSWORD.")
            time.sleep(5)
        except redis.ConnectionError:
            logger.error("Redis connection lost. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    process_worker()
