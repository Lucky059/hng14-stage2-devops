
#!/bin/bash
set -e

echo "🚀 Starting Rolling Update..."

# 1. Start the new container alongside the old one
# We use a temporary name to verify health
docker compose -p hng_prod up -d --scale api=2 --no-recreate

# 2. Identify the new container ID
NEW_CONTAINER=$(docker ps --filter "name=api" --format "{{.ID}}" | head -n 1)

echo "⏳ Waiting for new container ($NEW_CONTAINER) to pass health check..."

# 3. Poll for health status (max 60 seconds)
MAX_RETRIES=12
COUNT=0
HEALTHY=false

while [ $COUNT -lt $MAX_RETRIES ]; do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$NEW_CONTAINER")
  
  if [ "$STATUS" == "healthy" ]; then
    echo "✅ New container is healthy!"
    HEALTHY=true
    break
  fi
  
  echo "...status is $STATUS, waiting 5s ($((COUNT+1))/$MAX_RETRIES)"
  sleep 5
  COUNT=$((COUNT+1))
done

# 4. Final Logic: Swap or Abort
if [ "$HEALTHY" = true ]; then
  echo "🔄 Health check passed. Removing old containers..."
  docker compose -p hng_prod up -d --remove-orphans
else
  echo "❌ Health check failed within 60s! Aborting and rolling back..."
  docker stop "$NEW_CONTAINER"
  docker rm "$NEW_CONTAINER"
  exit 1
fi
