# --- STAGE 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies with specific versions
# Note: Version numbers can vary, but these are stable for Debian Bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:12.2.0-3 \
    python3-dev=3.11.2-1+b1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/usr/local -r requirements.txt


# --- STAGE 2: Runtime ---
FROM python:3.11-slim

WORKDIR /app

# 1. Install runtime essentials (curl version pinned)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u8 \
    && apt-get clean \
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
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

# Switch to the non-root user
USER hnguser

# The API listens on port 8000
EXPOSE 8000

# 7. Requirement: Working HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 8. Execution Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
