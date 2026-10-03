FROM node:22-slim

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends openssl \
  && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json ./
COPY to-do-list/backend/package.json ./to-do-list/backend/package.json
COPY to-do-list/frontend/package.json ./to-do-list/frontend/package.json

# Do not run npm lifecycle scripts in the image. This prevents the root
# `prepare` script from installing Lefthook hooks during the Docker build.
RUN npm ci --ignore-scripts

COPY to-do-list/backend ./to-do-list/backend

WORKDIR /app/to-do-list/backend
RUN npx prisma generate --schema src/prisma/schema.prisma
RUN npm run build

# The application only needs read access to its build and dependencies at
# runtime. Keep the runtime process away from root privileges.
USER node

EXPOSE 3000
CMD ["sh", "-c", "npx prisma db push --schema src/prisma/schema.prisma && npm run start"]
