
# STAGE 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# If you have a build script, run it here:
# RUN npm run build 

# STAGE 2: Final
FROM node:18-alpine
WORKDIR /app
# Fixes fe_named_nonroot_user
RUN addgroup -S hnggroup && adduser -S hnguser -G hnggroup
USER hnguser

# Fixes fe_multi_stage - Copying from builder stage
COPY --from=builder /app /app

EXPOSE 3000
# Fixes fe_healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["npm", "start"]

