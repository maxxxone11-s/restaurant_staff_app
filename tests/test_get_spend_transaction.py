from app.utilities.rewards import get_spend_transaction
from app.models.user_model import User
from app.models.reward_model import Reward
from app.models.shift_model import Shift

def test_get_spend_transaction():
    transaction = get_spend_transaction(
        1,
        300,
        "burger"
    )

    assert transaction.user_id == 1
    assert transaction.amount == -300
    assert transaction.type == "spend"
    assert transaction.description == "Покупка: burger"