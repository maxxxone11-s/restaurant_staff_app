from app.utilities.shifts import get_earn_transaction

def test_get_earn_transaction():
    transaction = get_earn_transaction(
        4,
        400
    )

    assert transaction.user_id == 4
    assert transaction.amount == 400
    assert transaction.type == "earn"
    assert transaction.description == "Смена была закрыта через fake_iiko"