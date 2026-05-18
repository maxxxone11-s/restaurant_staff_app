from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles, get_db
from app.models.shift_model import Shift

router = APIRouter(prefix="/manager", tags=["manager"])

@router.get("/revenue")
async def get_all_revenue(
    current_user = Depends(require_roles(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(func.sum(Shift.revenue))
        .where(Shift.revenue.is_not(None))
    )

    total_revenue = result.scalar_one_or_none()

    return {"total_revenue": total_revenue}

@router.get("/top_waiter")
async def get_top_revenue_waiter(
    current_user = Depends(require_roles(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Shift.user_id, func.sum(Shift.revenue))
        .where(Shift.revenue.is_not(None))
        .group_by(Shift.user_id)
        .order_by(func.sum(Shift.revenue).desc())
    )

    top_waiters = result.all()

    return top_waiters
