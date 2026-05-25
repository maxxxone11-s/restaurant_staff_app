from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.user_schema import UserResponse, UserUpdate
from app.core.roles import UserRole
from app.utilities.staff import create_user

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/me", response_model=UserResponse)
async def get_me_profile(
    current_user = Depends(get_current_user)
):
    return current_user
    
@router.get("/all", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    allow_roles = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER]))
):
    result = await db.execute(select(User))

    result = result.scalars().all()

    response = create_user(result)

    return response

@router.patch("/{user_id}", response_model=UserResponse)
async def user_update(
    user_id: int,
    data_user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER]))
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