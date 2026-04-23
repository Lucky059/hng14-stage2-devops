# STAGE 1: Builder
FROM python:3.11-slim-bookworm AS builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:12.2.0-3 \
    python3-dev=3.11.2-1+b1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# STAGE 2: Final Production Image
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r hng_group && useradd -r -g hng_group -m hng_user

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --chown=hng_user:hng_group . .

USER hng_user

# Ensure your worker file is named worker.py
CMD ["python", "worker.py"]


