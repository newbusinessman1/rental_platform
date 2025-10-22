# Rental Platform (Final Project)

Бэкенд на Django + DRF: объявления, поиск/фильтры, JWT, бронирования, отзывы, популярные и статистика.

## Quick start (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/seed.json   # опционально
python manage.py runserver


JWT

POST /api/token/ → {username, password}

POST /api/token/refresh/
Header: Authorization: Bearer <access>

Endpoints

GET/POST /api/listings/ (filters: location, price, rooms, housing_type, is_active; search: title, description; ordering: price, created_at)

GET /api/listings/{id}/ (инкремент views)

GET/POST /api/bookings/ (JWT)

GET/POST /api/reviews/ (JWT)

GET /api/popular-listings/

GET /api/search-stats/

Docker
docker compose up --build


---

# 6) Быстрые команды для запуска

```bash
# 1) Установить зависимости и окружение
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 2) Миграции + суперюзер + демо-данные
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/seed.json   # опционально

# 3) Старт
python manage.py runserver