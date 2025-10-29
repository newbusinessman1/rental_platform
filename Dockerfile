# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Системные зависимости для mysqlclient / Pillow и т.п.
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Кладём проект
COPY . /app/

# По умолчанию команда задаётся в compose (command:)