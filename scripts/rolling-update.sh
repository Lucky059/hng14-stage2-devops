
#!/bin/bash
set -e

echo "🚀 Starting Rolling Update..."

# 1. Start the services (if not running)
docker compose up -d

# 2. Scale API to 2 instances. 
# Because we didn't bind to a specific host port, this will not fail.
docker compose up -d --scale api=2 --no-recreate

echo "⏳ Waiting for new instance to stabilize..."
sleep 15

# 3. Scale back to 1. 
# Docker Compose intelligently removes the oldest container first.
docker compose up -d --scale api=1 --no-recreate

echo "✅ Rolling Update Completed Successfully!"
