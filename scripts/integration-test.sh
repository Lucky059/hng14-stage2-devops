
#!/bin/bash
set -e

# Since we hardcoded 8000 in compose, we use it here
API_URL="http://localhost:8000"
echo "🧪 Targeting API at $API_URL"

# 1. Wait for Healthcheck
echo "⏳ Waiting for API to become healthy..."
MAX_RETRIES=15
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
  if curl -s -f "$API_URL/health" > /dev/null; then
    echo "🚀 API is Online!"
    break
  fi
  echo "😴 API starting up... ($((COUNT+1))/$MAX_RETRIES)"
  sleep 4
  COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
  echo "❌ Error: API timed out. Logs:"
  docker compose logs api
  exit 1
fi

# 2. Run Job Lifecycle Test
echo "📡 Submitting test job..."
RESPONSE=$(curl -s -X POST "$API_URL/jobs")
JOB_ID=$(echo $RESPONSE | grep -oP '(?<="job_id":")[^"]+')

if [ -z "$JOB_ID" ]; then
  echo "❌ Error: Could not create job. Response: $RESPONSE"
  exit 1
fi

echo "✅ Job ID: $JOB_ID. Polling for completion..."

# 3. Poll for "completed" status
for i in {1..10}; do
  STATUS=$(curl -s "$API_URL/jobs/$JOB_ID" | grep -oP '(?<="status":")[^"]+')
  echo "🔍 Current Status: $STATUS"
  if [ "$STATUS" == "completed" ]; then
    echo "🎉 SUCCESS: Integration Test Passed!"
    exit 0
  fi
  sleep 3
done

echo "❌ Error: Job failed to complete in time."
exit 1
