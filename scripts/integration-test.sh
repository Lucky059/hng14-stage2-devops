#!/bin/bash

# Do NOT use 'set -e' here because we want to handle 
# connection failures manually in our loop.

echo "🚀 Starting API Healthcheck Probe..."

URL="http://localhost:8000/health"
MAX_RETRIES=15
COUNT=0

while [ $COUNT -lt $MAX_RETRIES ]; do
  # Use curl to get the status code. 
  # If the connection is refused, it will return '000'.
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")

  if [ "$STATUS" -eq 200 ]; then
    echo "✅ [SUCCESS] API is Healthy and responding with 200 OK!"
    exit 0
  fi

  echo "⏳ [WAITING] API is not ready yet (Status: $STATUS). Retrying in 5s... ($((COUNT+1))/$MAX_RETRIES)"
  
  sleep 5
  COUNT=$((COUNT+1))
done

echo "❌ [FAILURE] API failed to become healthy after $MAX_RETRIES attempts."

# Diagnostic: Check if the container is even running
echo "--- Docker Container Status ---"
docker ps -a | grep api || echo "API container not found!"

# Diagnostic: Show the last few lines of the API logs to see why it's failing
echo "--- API Container Logs ---"
docker logs hng-api-server --tail 20 || echo "Could not fetch logs."

exit 1
