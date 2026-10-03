FROM node:22-slim AS build

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl \
  && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json ./
COPY to-do-list/backend/package.json ./to-do-list/backend/package.json
COPY to-do-list/frontend/package.json ./to-do-list/frontend/package.json

RUN npm ci --ignore-scripts

COPY to-do-list/backend ./to-do-list/backend

WORKDIR /app/to-do-list/backend

RUN npx prisma generate --schema src/prisma/schema.prisma
RUN npm run build
RUN npm prune --omit=dev


FROM node:22-slim AS runtime

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl \
  && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/to-do-list/backend/node_modules ./to-do-list/backend/node_modules
COPY --from=build /app/to-do-list/backend/package.json ./to-do-list/backend/package.json
COPY --from=build /app/to-do-list/backend/dist ./to-do-list/backend/dist

WORKDIR /app/to-do-list/backend

USER node

EXPOSE 3000

CMD ["node", "dist/index.js"]
