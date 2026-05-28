def create_data_for_my(data):
    result = [
        {
            "id": item.id,
            "amount": item.amount,
            "type": item.type,
            "description": item.description,
            "created_at": item.created_at.isoformat()

        }
        for item in data
    ]

    return result