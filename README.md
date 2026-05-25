# Restaurant Staff App

Backend-сервис для управления персоналом ресторана: смены сотрудников, роли, выручка, начисление баллов, магазин наград и аналитика.

Система позволяет сотрудникам открывать и закрывать смены, получать баллы за выручку, тратить их в reward shop, а менеджерам и администраторам — смотреть аналитику по выручке, топ официантов и leaderboard по баллам.

Проект также включает fake iiko/keeper integration: при закрытии смены выручка имитируется как будто она пришла из внешней ресторанной системы.

---

## Основные возможности

- Регистрация и авторизация пользователей через JWT
- Role-based access control: admin / manager / waiter
- Профиль сотрудника: ресторан, должность, дата найма, статус активности
- Открытие и закрытие смен
- Fake iiko/keeper integration для получения revenue
- Начисление points за выручку
- История движения баллов
- Reward shop для покупки наград за points
- История покупок наград
- Аналитика по общей выручке
- Топ официантов по revenue
- Leaderboard сотрудников по points
- Фильтрация, сортировка и pagination для смен
- Async SQLAlchemy + PostgreSQL
- Alembic migrations
- Pytest tests с отдельной test database
- Docker support

---

## Architecture

Проект разделён на несколько слоёв:

- `api/routes` — FastAPI endpoints
- `models` — SQLAlchemy ORM models
- `schemas` — Pydantic request/response schemas
- `services` — бизнес-логика и интеграции
- `utilities` — вспомогательные функции
- `tests` — unit и API tests

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- Pydantic
- JWT / OAuth2PasswordBearer
- Pytest
- Docker
- Docker Compose

---

## Run with Docker

Build and run containers:

```bash
docker compose up --build


Apply migrations:
docker compose exec app alembic upgrade head

API docs:
http://localhost:8000/docs

Run tests
pytest
Тесты используют отдельную тестовую БД и dependency_overrides FastAPI