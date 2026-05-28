from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.redis import redis_client
from app.api.deps import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(select(1))
        await redis_client.ping()

        return {
            "status": "ok",
            "database": "connected",
            "redis": "connected"
            }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))