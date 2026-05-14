import asyncio

from app.core.database import engine
from app.core.base import Base
from app.models.user_model import User

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_async(Base.metadata.create_all)
        print("Таблицы созданы!")

asyncio.run(create_tables())