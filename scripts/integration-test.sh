#!/bin/bash
set -e

echo "🔍 Detecting API Port..."

# Strategy 1: Docker Compose Port command
API_PORT=$(docker compose port api 8000 | awk -F: '{print $NF}')

# Strategy 2: Fallback to Docker Inspect if Strategy 1 fails
if [ -z "$API_PORT" ] || [ "$API_PORT" == "0" ]; then
    echo "⚠️ Strategy 1 failed, trying Strategy 2..."
    CONTAINER_ID=$(docker compose ps -q api)
    API_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "8000/tcp") 0).HostPort}}' "$CONTAINER_ID")
fi

if [ -z "$API_PORT" ] || [ "$API_PORT" == "0" ]; then
    echo "❌ Error: Could not detect API port. Printing container status:"
    docker compose ps
    docker compose logs api
    exit 1
fi

API_URL="http://localhost:$API_PORT"
echo "✅ API successfully detected at $API_URL"

# ... (rest of your wait-for-it and test logic)
