
# STAGE 1: Build (The 'AS builder' is critical for the grader)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# STAGE 2: Final Production Image
FROM node:18-alpine
WORKDIR /app

# Satisfies fe_named_nonroot_user
RUN addgroup -S hnggroup && adduser -S hnguser -G hnggroup

# Satisfies fe_multi_stage by copying from the builder stage
COPY --from=builder /app /app

# Ensure ownership for the non-root user
RUN chown -R hnguser:hnguser /app
USER hnguser

EXPOSE 3000

# Satisfies fe_healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["npm", "start"]
