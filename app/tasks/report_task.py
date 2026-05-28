import time

from app.core.celery_app import restaurant_application
from app.core.logger import logger

@restaurant_application.task
def process_shift_closed(user_id, revenue, earned_points):
    time.sleep(5)

    logger.info(
        f"Shift processed: user_id={user_id}"
    )

    return {
        "user_id": user_id,
        "revenue": revenue,
        "earned_points": earned_points,
        "status": "processed"
    }