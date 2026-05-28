from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.api.deps import get_db, get_current_user
from app.models.transactions_model import PointTransaction
from app.schemas.points_schema import PointsHistoryResponse
from app.core.redis import redis_client

router = APIRouter(prefix="/points", tags=["points"])

@router.get("/my", response_model=list[PointsHistoryResponse])
async def get_history_points(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    cached_data = await redis_client.get(f"user_points:{current_user.id}")

    if cached_data:
        return json.loads(cached_data)

    result = await db.execute(
        select(PointTransaction)
        .where(PointTransaction.user_id == current_user.id)
        .order_by((PointTransaction.created_at.desc()))
    )

    result = result.scalars().all()
    data = [
        {
            "id": item.id,
            "amount": item.amount,
            "type": item.type,
            "description": item.description,
            "created_at": item.created_at.isoformat()

        }
        for item in result
    ]

    if data:
        await redis_client.set(
            f"user_points:{current_user.id}",
            json.dumps(data),
            ex=18000
        )
        return data
    
    raise HTTPException(status_code=404, detail="На вашем аккаунте еще не было транзакций")