# --- STAGE 1: Builder ---
# We use a build stage to install compilers and dev tools
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies required for building some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies to a specific prefix
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/usr/local -r requirements.txt


# --- STAGE 2: Runtime ---
# This is the lean image that actually ships to production
FROM python:3.11-slim

WORKDIR /app

# 1. Install runtime essentials (curl is required for the HEALTHCHECK)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Requirement: Run as a non-root user
RUN adduser --disabled-password --gecos '' hnguser

# 3. Copy only the installed Python packages from the builder
COPY --from=builder /usr/local /usr/local
# 4. Copy the application code
COPY . .

# 5. Requirement: Ensure the non-root user owns the application files
RUN chown -R hnguser:hnguser /app

# 6. Environment variables
# Prevents Python from writing .pyc files and ensures logs are flushed immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ensure the installed binaries are in the PATH
ENV PATH="/usr/local/bin:$PATH"

# Switch to the non-root user
USER hnguser

# The API listens on port 8000
EXPOSE 8000

# 7. Requirement: Working HEALTHCHECK
# It checks the /health endpoint we verified in your main.py
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 8. Execution Command
# We use main:app because the code is copied directly into /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
