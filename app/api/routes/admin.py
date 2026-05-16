from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_roles
from app.models.user_model import User
from app.api.deps import get_db, get_current_user
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    if require_roles("admin"):
        result = await db.execute(select(User))

        data = result.scalars().all()

        return data
