from fastapi import Depends, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.api.deps import require_roles, get_db
from app.models.shift_model import Shift
from app.models.user_model import User
from app.schemas.analytics_schema import RevenueResponse, TopWaitersResponse
from app.core.roles import UserRole
from app.core.redis import redis_client

router = APIRouter(prefix="/manager", tags=["manager"])

@router.get("/revenue", response_model=RevenueResponse)
async def get_all_revenue(
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER])),
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
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER])),
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

    top_waiters = result.mappings().all()

    return top_waiters

@router.get("/leader_points")
async def leader_points(
    access_allow = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER])),
    db: AsyncSession = Depends(get_db)
):
    cached_data = await redis_client.get("leader_points")

    if cached_data:
        return json.loads(cached_data)
    
    result = await db.execute(
        select(User.full_name, User.points)
        .order_by(User.points.desc())
    )

    data = [dict(item._mapping) for item in result]

    await redis_client.set(
        "leader_points",
        json.dumps(data),
        ex=60
    )

    return data