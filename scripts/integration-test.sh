
#!/bin/bash
set -e

echo "Checking API Health..."
URL="http://localhost:8000/health"
MAX_RETRIES=15
COUNT=0

while [ $COUNT -lt $MAX_RETRIES ]; do
  # Use -s (silent) and -w (output status code)
  # We use || true to prevent the script from exiting on a connection failure (Exit 7)
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")

  if [ "$STATUS" -eq 200 ]; then
    echo "✅ API is Healthy! (Status: $STATUS)"
    exit 0
  fi

  echo "⏳ Waiting for API... (Current Status: $STATUS) - Attempt $((COUNT+1))/$MAX_RETRIES"
  sleep 5
  COUNT=$((COUNT+1))
done

echo "❌ API failed healthcheck after $MAX_RETRIES attempts"
# Dump logs so we can see why it never started
docker compose -p hng_test logs api
exit 1
