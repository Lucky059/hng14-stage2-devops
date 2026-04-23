# --- STAGE 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/usr/local -r requirements.txt


# --- STAGE 2: Runtime ---
FROM python:3.11-slim

WORKDIR /app

# 1. Install procps for reliable process checking
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 2. Create non-root user (Requirement #3)
RUN adduser --disabled-password --gecos '' hnguser

# 3. Copy only necessary files from builder
COPY --from=builder /usr/local /usr/local
COPY . .

# 4. Set permissions
RUN chown -R hnguser:hnguser /app

# 5. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

USER hnguser

# 6. HEALTHCHECK (Requirement #2)
# We use grep -v grep to ignore the grep process itself
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ps aux | grep "python worker.py" | grep -v grep || exit 1

# 7. Start the worker
CMD ["python", "worker.py"]


