# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Ensure uvicorn is in your requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim
WORKDIR /app

# FIX 1: Install curl so the HEALTHCHECK actually works
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m hnguser
COPY --from=builder /root/.local /home/hnguser/.local
COPY . .
RUN chown -R hnguser:hnguser /app

USER hnguser
ENV PATH=/home/hnguser/.local/bin:$PATH
EXPOSE 8000

# The healthcheck now has curl available to it
HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1

# FIX 2: Use uvicorn to serve the app on all interfaces (0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
