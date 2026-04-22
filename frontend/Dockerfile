# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and lockfile
COPY package.json package-lock.json* ./

# Install only production dependencies (reproducible, faster)
RUN npm ci --omit=dev

# Copy application code
COPY . .

# Expose frontend port
EXPOSE 3000

# Healthcheck to verify the app responds
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Start the frontend service
CMD ["npm", "start"]



