from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Literal

from app.api.deps import get_current_user, get_db
from app.models.shift_model import Shift
from app.schemas.shift_schema import ShiftResponse, ShiftResponseClosed, ShiftResponseOpen
from app.services.shift_service import create_shift_response_list
from app.services.iiko import iiko_service
from app.utilities.shifts import get_earn_transaction
from app.core.redis import redis_client

router = APIRouter(prefix="/shifts", tags=["shifts"])

@router.post("/open", response_model=ShiftResponseOpen)
async def open_shift(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_open_shift = await db.execute(
        select(Shift)
        .where(Shift.user_id == current_user.id)
        .where(Shift.closed_shift.is_(None))
    )
    result = is_open_shift.scalar_one_or_none()

    if result:
        raise HTTPException(status_code=400, detail="Смена уже открыта")

    shift = Shift(
            user_id=current_user.id
        )

    try:
        db.add(shift)
        await db.commit()
        await db.refresh(shift)

        return shift
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/close", response_model=ShiftResponseClosed)
async def closed_shift(
    iiko_data = Depends(iiko_service),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_open_shift = await db.execute(
        select(Shift)
        .where(Shift.user_id == current_user.id)
        .where(Shift.closed_shift.is_(None))
    )

    result = is_open_shift.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail="Смена не открыта")

    result.closed_shift = func.now()
    result.revenue = iiko_data.revenue

    get_points = iiko_data.revenue // 100
    current_user.points += get_points

    transaction = get_earn_transaction(current_user.id, get_points)


    try:
        db.add(transaction)
        await db.commit()
        await db.refresh(result)
        await redis_client.delete(
            "leader_points"
        )
        return {
            "revenue": iiko_data.revenue,
            "points": get_points,
            "source": "fake_iiko"
            }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=list[ShiftResponse])
async def my_shifts(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, le=30),
    offset: int = Query(default=0),
    status: Literal["open", "closed"] | None = None,
    order_by: Literal["desc", "asc"] = "desc",
    date_from: datetime | None = None,
    date_to: datetime | None = None
):
    if date_from is not None and date_to is not None:
        query = (
            select(Shift)
            .where(Shift.user_id == current_user.id)
            .where(Shift.open_shift >= date_from) 
            .where(Shift.open_shift <= date_to)
            )
    else:
        query = (
            select(Shift)
            .where(Shift.user_id == current_user.id)
            )

    if order_by == "desc":
        query = query.order_by(Shift.open_shift.desc())
    elif order_by == "asc":
        query = query.order_by(Shift.open_shift.asc())

    if status == "open":
        query = query.where(
            Shift.closed_shift.is_(None)
        )
    elif status == "closed":
        query = query.where(
            Shift.closed_shift.is_not(None)
        )
    
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    shifts_user = result.scalars().all()

    response = create_shift_response_list(shifts_user)
        
    return response