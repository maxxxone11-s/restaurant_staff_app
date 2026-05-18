from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.shift_model import Shift
from app.schemas.shift_schema import ShiftResponse, ShiftClose

router = APIRouter(prefix="/shifts", tags=["shifts"])

@router.post("/open", response_model=ShiftResponse)
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


@router.post("/close", response_model=ShiftResponse)
async def closed_shift(
    close_data: ShiftClose,
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
    result.revenue = close_data.revenue
    try:
        await db.commit()
        await db.refresh(result)
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=list[ShiftResponse])
async def my_shifts(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Shift)
        .where(Shift.user_id == current_user.id)
    )

    shifts_user = result.scalars().all()
    response = []

    for shift in shifts_user:
        hours_worked = None
        
        if shift.closed_shift is not(None):
            delta = shift.closed_shift - shift.open_shift
            hours_worked = delta.total_seconds() / 3600

        response.append({
            "id": shift.id,
            "user_id": shift.user_id,
            "open_shift": shift.open_shift,
            "closed_shift": shift.closed_shift,
            "revenue": shift.revenue,
            "hours_worked": hours_worked
        })

    return response