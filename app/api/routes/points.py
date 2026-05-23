from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.transactions_model import PointTransaction
from app.schemas.points_schema import PointsHistoryResponse

router = APIRouter(prefix="/points", tags=["points"])

@router.get("/my", response_model=list[PointsHistoryResponse])
async def get_history_points(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PointTransaction)
        .where(PointTransaction.user_id == current_user.id)
        .order_by((PointTransaction.created_at.desc()))
    )

    result = result.scalars().all()

    if result:
        return result
    
    raise HTTPException(status_code=404, detail="На вашем аккаунте еще не было транзакций")