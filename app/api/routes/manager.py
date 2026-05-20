from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles, get_db
from app.models.shift_model import Shift
from app.models.user_model import User
from app.schemas.analytics_schema import RevenueResponse, TopWaitersResponse

router = APIRouter(prefix="/manager", tags=["manager"])

@router.get("/revenue", response_model=RevenueResponse)
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

@router.get("/top_waiters", response_model=list[TopWaitersResponse])
async def get_name_top_waiter(
    current_user = Depends(require_roles(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            User.full_name,
            func.sum(Shift.revenue).label("total_revenue")
        )
        .join(Shift, Shift.user_id == User.id)
        .where(Shift.revenue.is_not(None))
        .group_by(User.full_name)
        .order_by(func.sum(Shift.revenue).desc())
    )

    # data = []

    top_waiters = result.mappings().all()

    # for name, total in top_waiters:
    #     data.append({"full_name": name, "total_revenue": total})

    return top_waiters