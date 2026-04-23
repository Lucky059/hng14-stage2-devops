# --- STAGE 1: Builder ---
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:12.2.0-3 python3-dev=3.11.2-1+b1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- STAGE 2: Runtime ---
FROM python:3.11-slim
WORKDIR /app
RUN adduser --disabled-password --gecos '' hnguser
COPY --from=builder /install /usr/local
COPY . .
RUN chown -R hnguser:hnguser /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

USER hnguser

# Healthcheck for a worker: Verify the script is in the process list
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD pgrep -f "python worker.py" || exit 1

CMD ["python", "worker.py"]


