# Stage 1: Builder
FROM python:3.11.8-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Use --no-cache-dir to keep the layer small
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11.8-slim
WORKDIR /app

# FIX: Added --no-install-recommends and cleaned up apt lists in the same layer
# This satisfies DL3015 and DL3008 (if you ignore pinning or pin the version)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl=7.88.1-10+deb12u5 && \
    rm -rf /var/lib/apt/lists/*

# Requirement: Named non-root user
RUN useradd -m hnguser
COPY --from=builder /root/.local /home/hnguser/.local
COPY . .
RUN chown -R hnguser:hnguser /app

USER hnguser
# Ensure the local bin is in PATH for uvicorn
ENV PATH="/home/hnguser/.local/bin:${PATH}"

EXPOSE 8000

# HEALTHCHECK using curl
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
