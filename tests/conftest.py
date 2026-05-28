import pytest
from fastapi.testclient import TestClient

from app.models.reward_model import Reward
from app.models.reward_purchase_model import RewardPurchase
from app.models.shift_model import Shift
from app.models.transactions_model import PointTransaction
from app.models.user_model import User

from app.core.base import Base
from tests.db import engine
from app.main import app
from app.api.deps import get_db
from tests.db import get_db_for_testing
from app.core.rate_limit import login_rate_limit

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = get_db_for_testing
    app.dependency_overrides[login_rate_limit] = fake_rate_limit

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

async def fake_rate_limit():
    return None


# @pytest.fixture(autouse=True)
# async def cleanup_redis():
#     yield
#     await redis_client.flushdb()