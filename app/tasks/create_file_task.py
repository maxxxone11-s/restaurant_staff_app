from datetime import date
import json

from app.core.celery_app import restaurant_application
from app.core.logger import logger

@restaurant_application.task
def create_report(users):

    logger.info(
        f"Create report date: {date.today()}"
    )
    with open(f"/app/reports/report_{date.today()}.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)