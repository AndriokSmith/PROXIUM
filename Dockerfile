# Используем базовый образ
FROM alpine:latest

# Установка необходимых пакетов
RUN apk add --no-cache curl bash

# Установка Xray
RUN mkdir -p /etc/xray && \
    curl -L -o /usr/local/bin/xray https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    chmod +x /usr/local/bin/xray

# Создание конфигурационного файла
COPY config.json /etc/xray/config.json

EXPOSE 443

# Генерация UUID и запуск Xray
CMD ["sh", "-c", "xray uuid > /etc/xray/uuid.txt && xray run -c /etc/xray/config.json"]
