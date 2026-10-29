# Multi-Stage Production Dockerfile for Dalal Machinery Platform
# Stage 1: Build & Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

RUN apk add --no-cache libc6-compat

COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

# Stage 2: Hardened Production Image
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=5000

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create non-root system group and user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 dalal

# Copy production dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./

# Copy application code
COPY admin ./admin
COPY superadmin ./superadmin
COPY dev ./dev
COPY new ./new
COPY server ./server
COPY uploads ./uploads

# Ensure permissions for data and uploads directories
RUN mkdir -p /app/server/data /app/uploads && \
    chown -R dalal:nodejs /app/server/data /app/uploads /app

USER dalal

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:5000/api/health || exit 1

CMD ["node", "server/server.js"]
