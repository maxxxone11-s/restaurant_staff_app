from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:010SS@localhost:5432/restaurant_table"
engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

