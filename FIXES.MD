
Fix.md – CI/CD & Codebase Improvements
Sensitive Files
Problem: api/.env with secrets (REDIS_PASSWORD, APP_ENV) was committed.

Fix:

Removed with git rm --cached api/.env.

Added api/.env to .gitignore.

Created api/.env.example with placeholders (e.g., REDIS_PASSWORD=changeme).

Updated code to load values from environment variables at runtime.

Redis Configuration
Problem: Redis host/port hardcoded to localhost:6379 in api/main.py and worker/worker.py.

Impact: Containers could not connect to Redis service.

Fix:

Use environment variables:

python
host=os.getenv("REDIS_HOST", "redis")
port=int(os.getenv("REDIS_PORT", 6379))
password=os.getenv("REDIS_PASSWORD", None)
r = redis.Redis(host=host, port=port, password=password, decode_responses=True)
Added QUEUE_NAME env variable instead of hardcoding "job".

Added decode_responses=True so Redis returns strings.

API Healthcheck
Problem: API container marked unhealthy because /health endpoint was missing.

Fix: Added FastAPI route:

python
@app.get("/health")
def health():
    return {"status": "ok"}
API Route Mismatch
Problem: Frontend called /submit but API only exposed /jobs.

Fix: Added /submit alias route pointing to job creation logic.

Frontend Configuration
Problem: API URL hardcoded to http://localhost:8000 in frontend/app.js.

Impact: Frontend couldn’t reach API in containers.

Fix:

javascript
const API_URL = process.env.API_URL || "http://api:8000";
Frontend Package.json & ESLint
Problems:

Missing metadata, outdated axios.

ESLint misconfigured (old env key, missing devDependencies).

Fixes:

Added description and license fields.

Upgraded axios to latest stable.

Migrated to ESLint v10 flat config (eslint.config.js).

Defined Node.js globals via languageOptions.globals.

Added lint script: "lint": "eslint frontend/app.js".

Updated CI workflow to run npm ci && npm run lint.

Worker Service
Problems:

Redis client initialization had broken syntax (duplicated port, stray parentheses).

Caused runtime errors and container startup failures.

Fixes:

Rewrote initialization block with proper env variables and syntax.

Added decode_responses=True.

Corrected indentation and removed stray whitespace.

Linting
Python (flake8):

Added blank lines before/after functions (E302/E305).

Removed trailing blank lines (W391) and whitespace (W291).

Frontend (ESLint):

Scoped linting to frontend/**/*.js and frontend/app.js.

Disabled no-console, downgraded no-unused-vars to warnings.

CI workflow corrected to lint actual paths.

Outcome
Secrets removed from repo and replaced with .env.example.

Redis connections now work in containerized deployments.

API healthcheck passes, dependent services start reliably.

Frontend connects to API via environment variable.

Package.json updated, ESLint configured correctly, CI lint stage passes.

Worker service runs without syntax errors.

All Python and JS files pass lint checks.

CI/CD pipeline stable and secure.
