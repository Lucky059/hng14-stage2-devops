
# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim
WORKDIR /app

# FIXED: Removed specific version string to prevent exit code 100 
# while keeping --no-install-recommends for image optimization.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Production Requirement: Named non-root user
RUN useradd -m hnguser
COPY --from=builder /root/.local /home/hnguser/.local
COPY . .
RUN chown -R hnguser:hnguser /app

USER hnguser
ENV PATH="/home/hnguser/.local/bin:${PATH}"

EXPOSE 8000

# HEALTHCHECK is now stable because curl is guaranteed to install
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
