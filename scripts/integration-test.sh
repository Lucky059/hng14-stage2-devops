#!/bin/bash
set -e

echo "Checking API Health..."
MAX_RETRIES=10
URL="http://localhost:8000/health"

# Use curl with built-in retry logic to handle "Empty reply from server" (Code 56)
# --retry: number of retries
# --retry-delay: seconds between retries
# --retry-all-errors: retries on 56, 52, etc.
STATUS=$(curl --retry $MAX_RETRIES --retry-delay 5 --retry-all-errors -s -o /dev/null -w "%{http_code}" "$URL")

if [ "$STATUS" -eq 200 ]; then
  echo "API is Healthy! (Status: $STATUS)"
  exit 0
else
  echo "API failed healthcheck with status: $STATUS"
  # Log the last few lines of the API to see why it's failing
  docker compose -p hng_test logs api | tail -n 20
  exit 1
fi

