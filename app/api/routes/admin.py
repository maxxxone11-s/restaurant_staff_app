from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.api.deps import get_db, require_roles
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    current_user = Depends(require_roles(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    data = result.scalars().all()
    
    return data
