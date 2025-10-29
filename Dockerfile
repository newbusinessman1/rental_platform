# Dockerfile
FROM python:3.12-slim

# Системные утилиты (по минимуму)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала зависимости — чтобы кешировались
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь проект
COPY . .

# ВАЖНО: укажем модуль настроек (если требуется)
ENV DJANGO_SETTINGS_MODULE=rental_platform.settings
ENV PYTHONUNBUFFERED=1

# Запуск
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]