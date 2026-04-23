# --- STAGE 1: Build ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install --quiet
COPY . .
RUN npm run build

# --- STAGE 2: Runtime ---
FROM alpine:3.19
WORKDIR /app

# Install 'serve' and nodejs (pinned)
RUN apk add --no-cache nodejs=20.15.1-r0 npm=10.8.0-r0 && \
    npm install -g serve@14.2.3

# Copy build artifacts and set permissions
COPY --from=build /app/build ./build
RUN adduser -D hnguser && chown -R hnguser:hnguser /app

USER hnguser
EXPOSE 3000

# Healthcheck: Verify port 3000 is accepting connections
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD nc -z localhost 3000 || exit 1

CMD ["serve", "-s", "build", "-l", "3000"]




