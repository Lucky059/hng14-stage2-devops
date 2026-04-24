#!/bin/bash
set -e

# 1. Dynamically find the port Docker assigned to the API
echo "🔍 Detecting API Port..."
API_PORT=$(docker compose port api 8000 | cut -d: -f2)

if [ -z "$API_PORT" ]; then
  echo "❌ Error: Could not find mapping for API port 8000. Is the container running?"
  docker compose ps
  exit 1
fi

API_URL="http://localhost:$API_PORT"
echo "✅ API found at $API_URL"

# 2. Wait for the API to return a 200 OK on the health endpoint
echo "⏳ Waiting for API to be ready..."
MAX_RETRIES=10
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
  if curl -s -f "$API_URL/health" > /dev/null; then
    echo "🚀 API is UP!"
    break
  fi
  echo "😴 API not ready yet, retrying in 3s... ($((COUNT+1))/$MAX_RETRIES)"
  sleep 3
  COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
  echo "❌ Error: API failed to become healthy in time."
  docker compose logs api
  exit 1
fi

# 3. Run the Lifecycle Test
echo "🧪 Starting Job Lifecycle Test..."
RESPONSE=$(curl -s -X POST "$API_URL/jobs")
JOB_ID=$(echo $RESPONSE | grep -oP '(?<="job_id":")[^"]+')

if [ -z "$JOB_ID" ]; then
  echo "❌ Error: Failed to create job. Response: $RESPONSE"
  exit 1
fi

echo "✅ Job Created: $JOB_ID"

# 4. Poll for Completion
for i in {1..10}; do
  STATUS_RESP=$(curl -s "$API_URL/jobs/$JOB_ID")
  STATUS=$(echo $STATUS_RESP | grep -oP '(?<="status":")[^"]+')
  echo "⏳ Status: $STATUS"
  
  if [ "$STATUS" == "completed" ]; then
    echo "🎉 SUCCESS: Job lifecycle complete!"
    exit 0
  fi
  sleep 3
done

echo "❌ Error: Job timed out."
exit 1
