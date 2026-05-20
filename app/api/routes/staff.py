from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.user_schema import UserResponse

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

    response = {
        "id": result.id,
        "email":result.email,
        "restaurant_name": result.restaurant_name,
        "full_name": result.full_name,
        "position": result.position,
        "role": result.role,
        "hire_date": result.hire_date,
        "is_active": result.is_active
    }

    try:
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка в данных: {e}")
    
@router.get("/all", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles["admin", "manager"])
):
    result = await db.execute(select(User))

    result = result.scalars().all()

    response = []

    for user in result:
        user = {
        "id": result.id,
        "email":result.email,
        "restaurant_name": result.restaurant_name,
        "full_name": result.full_name,
        "position": result.position,
        "role": result.role,
        "hire_date": result.hire_date,
        "is_active": result.is_active
        }

        response.append(user)
        
    return response
