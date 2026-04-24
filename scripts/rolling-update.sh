
#!/bin/bash
set -e

echo "🚀 Starting Production Rolling Update..."

# Force recreate ensures that the old container is stopped 
# and the port is freed before the new one starts.
docker compose up -d --force-recreate --no-deps api worker frontend

echo "⏳ Waiting for stabilization..."
sleep 10

# Final check
docker compose ps

echo "✅ Deployment Successful!"
