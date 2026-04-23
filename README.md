📋 Prerequisites
Before starting, ensure the following are installed on your machine:

Git (to clone the repository)

Docker (latest stable version)

Docker Compose (v2 or higher, usually bundled with Docker Desktop)

Node.js & npm (for frontend development, optional if only running containers)

Python 3.10+ (for local API/worker testing outside containers, optional)
Setup Instructions
1. Clone the repository
bash
git clone https://github.com/OWNER/REPO.git
cd REPO
2. Create environment files
Each service expects environment variables. Create .env files with placeholder values:

api/.env

env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=changeme
APP_ENV=development
QUEUE_NAME=job
worker/.env

env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=changeme
QUEUE_NAME=job
frontend/.env

env
API_URL=http://api:8000
Note: Never commit .env files with real secrets. Use .env.example for placeholders.

3. Build and start the stack
bash
docker compose up --build
This will:

Build images for api, worker, and frontend

Start redis from the official image

Run all services on a shared network

4. Verify healthchecks
API: http://localhost:8000/health (localhost in Bing) → should return {"status":"ok"}

Frontend: http://localhost:3000/health (localhost in Bing) → should return {"status":"ok"}

Redis:

bash
docker exec -it <redis-container-id> redis-cli ping
→ should return PONG

✅ Successful Startup Looks Like
docker compose ps shows all services running and healthy.

Visiting http://localhost:3000 loads the frontend dashboard.

Submitting a job in the frontend shows it processed by the worker and stored in Redis.

Logs (docker compose logs -f) show API receiving requests, worker processing jobs, and frontend serving pages without errors.
