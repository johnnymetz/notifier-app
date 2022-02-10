# Stage 1: install dependencies
FROM node:16-alpine AS deps
WORKDIR /app

COPY package*.json .
RUN npm install --only=production --silent

# Stage 2: build the app
FROM node:16-alpine AS builder
WORKDIR /app

ARG NEXT_PUBLIC_API_HOST
RUN test -n "$NEXT_PUBLIC_API_HOST"
ENV NEXT_PUBLIC_API_HOST=${NEXT_PUBLIC_API_HOST}

# don't need package-lock.json from deps
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json .
COPY src ./src
COPY public/ ./public
COPY next.config.js jsconfig.json ./
RUN npm run build

# Stage 3: run the app
FROM node:16-alpine
WORKDIR /app

# copy everything from builder except src/,  jsconfig.json and package-lock.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package.json /app/next.config.js ./

HEALTHCHECK CMD curl --fail http://localhost:80 || exit 1

CMD ["npm", "run", "start"]
