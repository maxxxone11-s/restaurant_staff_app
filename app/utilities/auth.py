from app.core.security import hash_password
from app.models.user_model import User
from app.core.roles import UserRole

def create_user(user_data):
    user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            position=user_data.position,
            restaurant_name=user_data.restaurant_name,
            role=UserRole.WAITER.value,
            hashed_password=hash_password(user_data.password)
        )
    
    return user