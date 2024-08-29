# Используем базовый образ
FROM ubuntu:20.04

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

# Установка Xray
RUN mkdir -p /etc/xray && \
    curl -L -o /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip

# Клонирование репозитория и запуск скрипта
RUN git clone https://github.com/saliei/XrayRealityScript.git && \
    cd XrayRealityScript && \
    ./reality.sh

# Открытие порта
EXPOSE 443
