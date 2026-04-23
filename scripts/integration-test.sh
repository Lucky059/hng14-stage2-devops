#!/bin/bash
set -e

API_URL="http://localhost:8000"

echo "🧪 Starting Job Lifecycle Integration Test..."

# 1. Submit a job via the API
RESPONSE=$(curl -s -X POST "$API_URL/jobs")
JOB_ID=$(echo $RESPONSE | jq -r '.job_id')

if [ "$JOB_ID" == "null" ]; then
  echo "❌ Failed to submit job"
  exit 1
fi

echo "✅ Job submitted! ID: $JOB_ID"

# 2. Poll until status is 'completed'
MAX_ATTEMPTS=20
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS_RES=$(curl -s "$API_URL/jobs/$JOB_ID")
  STATUS=$(echo $STATUS_RES | jq -r '.status')
  
  echo "⏳ Current Job Status: $STATUS"
  
  if [ "$STATUS" == "completed" ]; then
    echo "🎉 Integration Test Passed: Job reached completed state!"
    exit 0
  fi
  
  sleep 3
  ATTEMPT=$((ATTEMPT+1))
done

echo "❌ Integration Test Failed: Job timed out"
exit 1
