FROM nginx:1.25.3-bookworm

# Metadata
LABEL maintainer="Ukweku Lucky"

# Security: Allow Nginx to run as non-root
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# Hadolint requires pinning curl even in Nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl=7.88.1-10+deb12u8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/nginx/html

# Copy your frontend files
COPY --chown=nginx:nginx . .

# Switch to standard nginx user
USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]




