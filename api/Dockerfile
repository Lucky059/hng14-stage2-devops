# STAGE 1: Builder
FROM python:3.11-slim-bookworm AS builder

# Required for Hadolint DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app

# Pinning with wildcards satisfies DL3008 while allowing for security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:12.2.* \
    python3-dev=3.11.2-* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# STAGE 2: Final Production
FROM python:3.11-slim-bookworm

LABEL maintainer="Ukweku Lucky"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/hng_user/.local/bin:$PATH"

# Security: Non-root user
RUN groupadd -r hng_group && useradd -r -g hng_group -m hng_user

WORKDIR /app

# Install runtime curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY --chown=hng_user:hng_group . .

USER hng_user

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
