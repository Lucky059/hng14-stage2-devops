# STAGE 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# STAGE 2: Final Production Image
FROM node:18-alpine
WORKDIR /app

# 1. Create the group and user FIRST (Alpine syntax)
# -S creates a system user/group
RUN addgroup -S hnggroup && adduser -S hnguser -G hnggroup

# 2. Copy the files from the builder stage
COPY --from=builder /app /app

# 3. NOW you can change ownership because the user exists
RUN chown -R hnguser:hnguser /app

# 4. Switch to the non-root user
USER hnguser

EXPOSE 3000

# Healthcheck using wget (Alpine doesn't have curl by default)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["npm", "start"]
