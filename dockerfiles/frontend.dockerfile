FROM node:22-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./
COPY to-do-list/backend/package.json ./to-do-list/backend/package.json
COPY to-do-list/frontend/package.json ./to-do-list/frontend/package.json

RUN npm ci --ignore-scripts

COPY to-do-list/frontend ./to-do-list/frontend

WORKDIR /app/to-do-list/frontend
ARG VITE_API_URL=http://localhost:3000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginxinc/nginx-unprivileged:alpine
COPY --from=build /app/to-do-list/frontend/dist /usr/share/nginx/html
COPY dockerfiles/frontend.nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
