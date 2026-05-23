from app.models.transactions_model import PointTransaction
from app.models.reward_purchase_model import RewardPurchase

def get_spend_transaction(user_id, cost_points, title):
    transaction = PointTransaction(
        user_id=user_id,
        amount=-cost_points,
        type="spend",
        description=f"Покупка: {title}"
    )

    return transaction

def get_purchase(user_id, rew_id, cost_points):
    purchase = RewardPurchase(
        user_id=user_id,
        reward_id=rew_id,
        cost_points=cost_points
    )

    return purchase