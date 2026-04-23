#!/bin/bash
set -e

API_URL="http://localhost:8000"
echo "🧪 Running End-to-End Job Lifecycle Test..."

# 1. Post a Job
RESPONSE=$(curl -s -X POST "$API_URL/jobs")
JOB_ID=$(echo $RESPONSE | grep -oP '(?<="job_id":")[^"]+')

if [ -z "$JOB_ID" ]; then
  echo "❌ Error: Could not retrieve Job ID"
  exit 1
fi

echo "✅ Job Created: $JOB_ID"

# 2. Poll for Completion
MAX_RETRIES=10
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
  STATUS=$(curl -s "$API_URL/jobs/$JOB_ID" | grep -oP '(?<="status":")[^"]+')
  echo "⏳ Status: $STATUS ($((COUNT+1))/$MAX_RETRIES)"
  
  if [ "$STATUS" == "completed" ]; then
    echo "🎉 Success: Job finished processing!"
    exit 0
  fi
  
  sleep 5
  COUNT=$((COUNT+1))
done

echo "❌ Failure: Job did not complete in time"
exit 1
