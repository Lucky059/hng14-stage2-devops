# hng14-stage2-devops
# Multi‑Service DevOps Project

## Overview
This project demonstrates a containerized application stack with four services:
- **API** – Python backend with job creation and health endpoints
- **Worker** – Background processor consuming jobs from Redis
- **Frontend** – React dashboard with health monitoring
- **Redis** – In‑memory store with optional password authentication

The stack is orchestrated with **Docker Compose** and integrated into a **GitHub Actions CI/CD pipeline**.

## Features
- CI/CD pipeline with linting, testing, image builds, and deployment
- Container security scanning using **Trivy**
- Integration tests with Docker Compose healthchecks
- Support for Blue‑Green Deployment strategies on AWS
- Linux server hardening practices applied to infrastructure

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/OWNER/REPO.git
   cd REPO
Create .env files or export environment variables:

bash
REDIS_PASSWORD=yourpassword
API_URL=http://localhost:8000
Start services:

bash
docker compose up --build
CI/CD
Linting: flake8, eslint, hadolint

Testing: pytest with coverage reports

Build: Docker images pushed to GHCR

Security: Trivy scans fail on CRITICAL vulnerabilities

Integration: Docker Compose stack with healthchecks

Deployment: Blue‑Green strategy supported for AWS

Secrets Required
GHCR_PAT – GitHub PAT with Packages: write

REDIS_PASSWORD – Redis password (optional; blank runs without auth)

Health Endpoints
API: http://localhost:8000/health

Frontend: http://localhost:3000/health

Redis: redis-cli ping (with or without password)
