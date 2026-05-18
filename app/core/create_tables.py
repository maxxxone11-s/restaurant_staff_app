import asyncio

from app.core.database import engine
from app.core.base import Base
from app.models.user_model import User
from app.models.shift_model import Shift

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())