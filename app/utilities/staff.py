from app.models.user_model import User

def create_user(data_user):
    response = []

    for user in data_user:
        one_user = {
        "id": user.id,
        "email":user.email,
        "restaurant_name": user.restaurant_name,
        "full_name": user.full_name,
        "points": user.points,
        "position": user.position,
        "role": user.role,
        "hire_date": user.hire_date,
        "is_active": user.is_active
        }

        response.append(one_user)

    return response