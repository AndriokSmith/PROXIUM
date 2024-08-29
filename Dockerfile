# Используем базовый образ
FROM alpine:latest

# Установка необходимых пакетов
RUN apk add --no-cache curl unzip

# Установка Xray
RUN mkdir -p /etc/xray && \
    curl -L -o /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip

# Создание конфигурационного файла
COPY config.json /etc/xray/config.json

# Указание порта, который будет слушать контейнер
EXPOSE 443

# Запуск Xray
CMD ["xray", "run"]
