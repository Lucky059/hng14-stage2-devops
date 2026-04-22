# Use official Node.js image
FROM node:18-alpine

WORKDIR /app

# Copy package.json and lockfile
COPY package.json package-lock.json* ./

# Install dependencies (use ci if lockfile exists, otherwise install)
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --omit=dev; fi

# Copy application code
COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["npm", "start"]



