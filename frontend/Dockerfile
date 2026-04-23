# STAGE 1: Build
FROM node:20-bookworm-slim AS builder

WORKDIR /app

# Use npm ci for faster, more reliable builds (Hadolint preference)
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


# STAGE 2: Production
FROM nginx:1.25.3-bookworm

LABEL maintainer="Ukweku Lucky"

# Prepare Nginx folders for non-root execution
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/nginx/html

# Copy build assets with proper ownership
COPY --from=builder --chown=nginx:nginx /app/dist . 

USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]




