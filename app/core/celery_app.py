from celery import Celery

from app.core.database import settings

restaurant_application = Celery(
    "restaurant_app",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.report_task",
        "app.tasks.create_file_task"
        ]
)

restaurant_application.autodiscover_tasks(
    ["app.tasks"]
)