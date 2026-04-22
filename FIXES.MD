File: api/.env
Issue: Sensitive environment variables (REDIS_PASSWORD, APP_ENV) were committed to GitHub.
Why it’s a problem: Environment files often contain secrets like passwords or API keys. If they are pushed to GitHub, anyone can see them, which is a serious security risk.
Fix: 
  - Removed api/.env from the repository using `git rm --cached api/.env`.
  - Added api/.env to .gitignore so it will not be committed again.
  - Created api/.env.example with placeholder values (e.g., REDIS_PASSWORD=changeme, APP_ENV=development).
  - Updated code in api/main.py to load values from environment variables at runtime instead of hardcoding.





File: api/main.py
Line: r = redis.Redis(host="localhost", port=6379)
Issue: Redis host and port were hardcoded to "localhost:6379". This breaks containerized deployments because "localhost" points to the API container itself, not the Redis service.
Fix:I updated my code to use environment variables:
    host=os.getenv("REDIS_HOST", "redis")
    port=int(os.getenv("REDIS_PORT", 6379))
    password=os.getenv("REDIS_PASSWORD", None)
Also updated job queue name to use environment variable QUEUE_NAME instead of hardcoding "job".



File: frontend/app.js
Issue:
  API URL was hardcoded to "http://localhost:8000". This breaks containerized deployments because "localhost" points to the frontend container itself, not the API service.

Fix:
  I updated the code to load the API URL from environment variables:
    const API_URL = process.env.API_URL || "http://api:8000";
Impact:
  The frontend can now connect to the API service reliably in both local and containerized environments.



File: frontend/package.json
Issue:
  Package.json was missing metadata and used an older axios version. While dependencies and scripts were correct, the file lacked clarity for reviewers.

Fix:
  I updated package.json to:
    - Add a description and license field.
    - Upgrade axios to the latest stable version.
Impact:
  The frontend dependencies are now up-to-date, and the package.json provides clearer context for collaborators and reviewers.


File: worker/worker.py
Issue:
  r = redis.Redis(host="localhost", port=6379)Redis connection was hardcoded to localhost:6379. This caused failures in containerized deployments because "localhost" pointed to the worker container itself, not the Redis service.

Fix:
  I updated the Redis connection to use environment variables instead of hardcoding:
    host=os.getenv("REDIS_HOST", "redis")
    port=int(os.getenv("REDIS_PORT", 6379))
    password=os.getenv("REDIS_PASSWORD", None)
  I also updated the queue name to use QUEUE_NAME from environment variables instead of hardcoding "job".
Impact:
  The worker can now connect to Redis reliably in both local and containerized environments.



File: api/main.py / docker-compose.yml
Issue:
  API container was marked unhealthy even though Uvicorn started successfully.
  Healthcheck was configured to probe /health, but FastAPI app did not expose this endpoint.

Fix:
  Added a /health route in api/main.py:
    @app.get("/health")
    def health():
        return {"status": "ok"}
  This ensures the Docker healthcheck succeeds.
  Alternatively, the healthcheck block in docker-compose.yml could be removed or pointed to an existing endpoint.

Impact:
  API container now passes healthcheck and remains in a healthy state.
  Dependent services (frontend, worker) can reliably start without failing due to unhealthy dependency.


File: api/main.py

Line 22: The route definition for job creation (@app.post("/jobs"))

Problem:  
The frontend is coded to call /submit when creating a new job, but the API only exposes /jobs. This mismatch means the frontend receives no valid response, so the dashboard shows Submitted: undefined
fix: I added an alias route /submit that calls the same logic as /jobs


File: api/main.py
Line: 10
Problem: Redis client returned bytes by default, which can cause issues when reading job status.
Fix: Added decode_responses=True to redis.Redis() so values are returned as strings.

Worker Service
File: worker/worker.py

Line(s): Redis client initialization (top of file)

Issue:  
Redis client was incorrectly initialized with hardcoded "REDIS_HOST" string and malformed syntax. The code had duplicated port argument and stray parentheses, causing runtime errors and preventing the worker from connecting to Redis.

Fix:  
Replaced with proper environment variable usage and corrected syntax. Added decode_responses=True for cleaner string handli

File: worker/worker.py

Line(s): Redis client initialization (top of file)

Issue:

The Redis client was incorrectly initialized with broken syntax: parentheses closed too early, duplicated port argument, and mis‑indented lines.

This caused IndentationError: unexpected indent and prevented the worker container from starting.

Fix:

Rewrote the Redis client initialization block to use proper Python syntax and environment variables.

Added decode_responses=True so job IDs and statuses are returned as strings without manual decoding.



# Lint Fixes for main.py

- Added 2 blank lines before each top-level function (`E302`).
- Added 2 blank lines after each function (`E305`).
- Removed trailing blank line at end of file (`W391`).





## lint fixes for worker.py
- Added 2 blank lines before `process_job` function (`E302`).
- Added 2 blank lines after `process_job` before `while True` loop (`E305`).
- Removed trailing blank line at end of file (`W391`).

# Lint Fixes Summary

## api/main.py
- Added two blank lines before each top-level function (`E302`).
- Added two blank lines after each function definition (`E305`).
- Removed trailing blank line at end of file (`W391`).

## worker/worker.py
- Added two blank lines before the `process_job` function (`E302`).
- Added two blank lines after the `process_job` function before the `while True` loop (`E305`).
- Removed trailing blank line at end of file (`W391`).
- Removed trailing whitespace on line 24 (`W291`).

## frontend (ESLint)
- Fixed CI workflow path: changed ESLint target from `frontend/src` to `frontend` since no `src` folder exists.
- Added new `eslint.config.js` file for ESLint v10 compatibility (flat config system).
- **Updated `package.json` devDependencies:**
  - Added `eslint` (`^10.2.1`) to enable linting.
  - Added `@eslint/js` (`^10.2.1`) to provide recommended ESLint rules.
- Created a `lint` npm script (`npm run lint`) to run ESLint on `frontend`, `views`, and `app.js`.
- Updated GitHub Actions workflow to run `npx eslint frontend views app.js`.

## Outcome
- Python files (`api/main.py` and `worker/worker.py`) now pass `flake8` with no errors.
- Frontend JavaScript files now lint successfully with ESLint v10 using the new config and dependencies.
- CI/CD pipeline lint stage should now complete without errors.

