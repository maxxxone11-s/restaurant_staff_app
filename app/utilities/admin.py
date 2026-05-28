def create_users_list(data):
    users = [
        {
            "id": user.id, 
            "email": user.email,
            "restaurant_name": user.restaurant_name,
            "full_name": user.full_name,
            "position": user.position,
            "role": user.role,
            "hire_date": user.hire_date.isoformat(),
            "is_active": user.is_active
        }
        for user in data
    ]

    return users