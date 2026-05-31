Restaurant Staff App

Backend-сервис для управления персоналом ресторана.

Проект разработан на FastAPI и позволяет управлять сотрудниками, сменами, системой баллов и наградами.

Возможности

Авторизация и аутентификация

* Регистрация сотрудников
* JWT авторизация
* Получение данных текущего пользователя
* Разграничение прав доступа по ролям

Роли пользователей

* ADMIN
* MANAGER
* STAFF

Управление сменами

* Открытие смены
* Закрытие смены
* Начисление баллов за выручку
* История смен

Система баллов

* Начисление баллов сотрудникам
* История транзакций
* Таблица лидеров

Награды

* Создание наград
* Покупка наград за баллы
* История покупок

Redis

Используется для:

* Кэширования данных
* Rate limiting авторизации
* Celery broker
* Celery result backend

Celery

Используется для фоновых задач:

* Генерация отчетов по сотрудникам
* Выполнение длительных операций вне HTTP-запроса

Monitoring

* Health check endpoint
* Application logging

Testing

* Pytest
* Отдельная тестовая база данных
* GitHub Actions CI

⸻

Технологии

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy Async
* Alembic
* Redis
* Celery
* Nginx
* Docker Compose
* Pytest
* GitHub Actions

⸻

Структура проекта

app/

* api/
* core/
* models/
* schemas/
* services/
* tasks/
* utilities/

tests/

* test_api.py
* utilities.py
* conftest.py

⸻

Переменные окружения

Создайте файл .env

SECRET_KEY=your_secret_key

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/restaurant_db

TEST_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/test_restaurant_db

REDIS_URL=redis://localhost:6379

⸻

Запуск проекта

Сборка контейнеров:

docker compose build

Запуск:

docker compose up

Документация Swagger:

http://localhost/docs

⸻

Запуск тестов

pytest

⸻

CI

При каждом Push и Pull Request автоматически запускаются:

* PostgreSQL
* Redis
* Pytest

GitHub Actions проверяет корректность работы проекта перед слиянием изменений.

⸻

Будущие улучшения

* Экспорт отчетов в Excel
* Email уведомления
* RabbitMQ интеграция
* Расширенная аналитика сотрудников