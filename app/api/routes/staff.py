from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.user_schema import UserResponse, UserUpdate

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/me", response_model=UserResponse)
async def get_me_profile(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(
        select(User)
        .where(User.id == current_user.id)
    )

    result = result.scalar_one_or_none()

    try:
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка в данных: {e}")
    
@router.get("/all", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles(["admin", "manager"]))
):
    result = await db.execute(select(User))

    result = result.scalars().all()

    response = []

    for user in result:
        one_user = {
        "id": user.id,
        "email":user.email,
        "restaurant_name": user.restaurant_name,
        "full_name": user.full_name,
        "position": user.position,
        "role": user.role,
        "hire_date": user.hire_date,
        "is_active": user.is_active
        }

        response.append(one_user)

    return response

@router.patch("/{user_id}", response_model=UserResponse)
async def user_update(
    user_id: int,
    data_user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles(["admin", "manager"]))
):
    update_data = data_user_update.model_dump(
        exclude_unset=True
    )

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    target_user = result.scalar_one_or_none()

    if target_user:
        for field, value in update_data.items():
            setattr(target_user, field, value)

        await db.commit()
        await db.refresh(target_user)

        return target_user
    
    raise HTTPException(status_code=404, detail="Пользователь не найден")