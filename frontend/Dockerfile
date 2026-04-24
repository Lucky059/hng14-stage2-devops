# STAGE 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# STAGE 2: Final Production Image
FROM node:18-alpine
WORKDIR /app

# 1. Create a group and a user with the SAME name to avoid confusion
# -D ensures the user is created without a password
RUN addgroup -S hnguser && adduser -S hnguser -G hnguser

# 2. Copy the files from the builder stage
COPY --from=builder /app /app

# 3. Use hnguser:hnguser (User:Group)
RUN chown -R hnguser:hnguser /app

# 4. Switch to the non-root user
USER hnguser

EXPOSE 3000

# Alpine uses wget for healthchecks
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["npm", "start"]
