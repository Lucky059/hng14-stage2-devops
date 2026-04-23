# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim
WORKDIR /app
# Requirement: Named non-root user
RUN useradd -m hnguser
COPY --from=builder /root/.local /home/hnguser/.local
COPY . .
RUN chown -R hnguser:hnguser /app
USER hnguser
ENV PATH=/home/hnguser/.local/bin:$PATH
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "main.py"]
