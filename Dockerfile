# Используем базовый образ
FROM ubuntu:20.04

# Установка необходимых пакетов
RUN apk add --no-cache curl unzip
EXPOSE 443

# Установка Xray
RUN mkdir -p /etc/xray && \
    curl -L -o /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip

RUN apt install git -y
RUN git clone https://github.com/saliei/XrayRealityScript.git
RUN cd XrayRealityScript && ./reality.sh


