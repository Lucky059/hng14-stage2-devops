# --- STAGE 1: Build ---
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .

# --- STAGE 2: Runtime ---
FROM node:20-alpine
WORKDIR /app

# Requirement: Non-root user
RUN adduser -D hnguser
# Install curl for the HEALTHCHECK
RUN apk add --no-cache curl

COPY --from=builder /app /app
RUN chown -R hnguser:hnguser /app

USER hnguser
EXPOSE 3000

# Requirement: Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# BUG FIX: Ensure this points to app.js, not server.js
CMD ["node", "app.js"]




