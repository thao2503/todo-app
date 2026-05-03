# syntax=docker/dockerfile:1
# Build from repo root: docker build -f frontend/Dockerfile frontend
# Or from frontend/: docker build .

FROM node:20-alpine AS build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

# Vite inlines these at build time (see src/axios.js, store/authStore.js, main.js).
ARG VITE_API_ENDPOINT
ARG VITE_GOOGLE_CLIENT_ID
ARG VITE_GA_MEASUREMENT_ID
ENV VITE_API_ENDPOINT=$VITE_API_ENDPOINT \
    VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID \
    VITE_GA_MEASUREMENT_ID=$VITE_GA_MEASUREMENT_ID

RUN yarn build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
