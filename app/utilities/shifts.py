from app.models.transactions_model import PointTransaction

def get_earn_transaction(user_id, get_points):
    transaction = PointTransaction(
        user_id=user_id,
        amount=get_points,
        type="earn",
        description="Смена была закрыта через fake_iiko"
    )

    return transaction