# Объявление аргумента STAGE
ARG STAGE

# Сборочный этап для dev
FROM node:18-alpine AS dev
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install --loglevel=warn && \
    npm --version && \
    node --version

# Копируем остальные файлы
COPY . .

CMD ["npm", "run", "dev"]

# Сборочный этап для production
FROM node:18-alpine AS build
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install --loglevel=warn

# Копируем остальные файлы и собираем проект
COPY . .
RUN npm run build

# Финальный образ для production
FROM nginx:stable-alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Выбор этапа сборки
FROM ${STAGE} AS final