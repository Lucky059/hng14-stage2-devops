# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm install --production

# Copy application code
COPY . .

# Expose frontend port
EXPOSE 3000

# Add a lightweight healthcheck using wget (already available in Alpine)
# Make sure your app.js has a /health endpoint that returns 200 OK
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Start the frontend service
CMD ["npm", "start"]


