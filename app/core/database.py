from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    test_database_url: str
    redis_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()

engine = create_async_engine(
    settings.database_url,
    echo=True
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

