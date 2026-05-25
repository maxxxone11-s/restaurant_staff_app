import pytest

from app.models.reward_model import Reward
from app.models.reward_purchase_model import RewardPurchase
from app.models.shift_model import Shift
from app.models.transactions_model import PointTransaction
from app.models.user_model import User

from app.core.base import Base
from tests.db import engine

@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)