# https://github.com/vercel/next.js/blob/canary/examples/with-docker/Dockerfile
# https://www.nicovak.com/posts/nextjs-docker-multistage

FROM node:16-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production --silent

FROM node:16-alpine AS builder
WORKDIR /app
ARG NEXT_PUBLIC_API_HOST
ENV NEXT_PUBLIC_API_HOST=${NEXT_PUBLIC_API_HOST}
COPY --from=deps /app ./
COPY src/ ./src
COPY public/ ./public
COPY next.config.js/ ./next.config.js
COPY jsconfig.json ./jsconfig.json
RUN npm run build

FROM node:16
WORKDIR /app
ENV NODE_ENV=production

# copy everything except src/,  jsconfig.json and package-lock.json
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/.next ./.next

HEALTHCHECK CMD curl --fail http://localhost:80 || exit 1

CMD ["npm", "run", "start"]
