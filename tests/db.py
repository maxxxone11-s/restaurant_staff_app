from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.database import settings


engine = create_async_engine(
    settings.test_database_url,
    echo=True,
    poolclass=NullPool
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db_for_testing():
    async with AsyncSessionLocal() as session:
        yield session
