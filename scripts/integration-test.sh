#!/bin/bash
set -e
echo "Checking API Health..."
MAX_RETRIES=5
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
  if [ $STATUS -eq 200 ]; then
    echo "API is Healthy!"
    exit 0
  fi
  echo "Waiting for API... ($STATUS)"
  sleep 10
  COUNT=$((COUNT+1))
done
echo "API failed healthcheck"
exit 1
