FROM nginx:1.25.3-bookworm

# Metadata
LABEL maintainer="Ukweku Lucky"

# Security: Allow Nginx to run as non-root by adjusting permissions
# This ensures the nginx user can write to necessary directories
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# Hadolint requires pinning curl. 
# Using wildcard '*' to avoid "Version not found" errors during security updates.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/nginx/html

# Copy your frontend files and set ownership to the nginx user
COPY --chown=nginx:nginx . .

# Switch to the non-root nginx user
USER nginx

# Standard web port
EXPOSE 80

# Healthcheck to verify the frontend is up
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]




