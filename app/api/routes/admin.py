from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.api.deps import get_db, require_roles
from app.schemas.user_schema import UserResponse
from app.core.roles import UserRole

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    current_user = Depends(require_roles([UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    data = result.scalars().all()
    if data: 
        return data

    raise HTTPException(status_code=404, detail="Пользователи не найдены")