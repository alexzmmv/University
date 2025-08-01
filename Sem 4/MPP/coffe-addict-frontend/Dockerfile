FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . ./

# Build the application
ENV CI=true
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Accept API_BASE_URL as a build argument
ARG API_BASE_URL="http://localhost:8000/"
ENV API_BASE_URL=$API_BASE_URL

RUN echo "Building with API_BASE_URL: $API_BASE_URL"
RUN npm run build

# Debug: List the contents of .next directory to verify standalone build
RUN ls -la .next/ || echo "No .next directory found"
RUN ls -la .next/standalone/ || echo "No standalone directory found"

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED=1

# Pass API_BASE_URL from builder to runner
ARG API_BASE_URL
ENV API_BASE_URL=$API_BASE_URL

# Create a non-root user and give them ownership of the app directory
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs && \
    chown -R nextjs:nodejs /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["node", "server.js"]
