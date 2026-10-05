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


FROM node:22-slim AS runtime

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/to-do-list/backend \
  && chown node:node /app/to-do-list/backend

USER node

COPY --chown=node:node to-do-list/backend/package.json ./to-do-list/backend/package.json
WORKDIR /app/to-do-list/backend
RUN npm install --omit=dev --ignore-scripts --no-package-lock \
  && npm cache clean --force

COPY --from=build --chown=node:node /app/to-do-list/backend/dist /app/to-do-list/backend/dist
COPY --from=build --chown=node:node /app/to-do-list/backend/src/prisma /app/to-do-list/backend/src/prisma
RUN npx prisma generate --schema src/prisma/schema.prisma

EXPOSE 3000

CMD ["sh", "-c", "npm run db:migrate && npm run start"]
