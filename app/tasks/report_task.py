import time

from app.core.celery_app import restaurant_application

@restaurant_application.task
def process_shift_closed(user_id, revenue, earned_points):
    time.sleep(5)

    print(
        "Shift report processed: "
        f"user_id={user_id}, revenue={revenue}, earned_points={earned_points}"
    )

    return {
        "user_id": user_id,
        "revenue": revenue,
        "earned_points": earned_points,
        "status": "processed"
    }