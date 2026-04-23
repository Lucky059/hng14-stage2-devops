FROM nginx:1.25.3-bookworm

LABEL maintainer="Ukweku Lucky"

# Security: Prepare Nginx folders for non-root execution
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# Hadolint requires pinning curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/nginx/html

# Copy all static files directly to the nginx html directory
# Use --chown to ensure the 'nginx' user owns the files
COPY --chown=nginx:nginx . .

# Switch to non-root user
USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]




