from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.models.user_model import User
from app.api.deps import get_db, require_roles
from app.schemas.user_schema import UserResponse
from app.core.roles import UserRole
from app.tasks.create_file_task import create_report

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    is_active: bool | None = None,
    create_file: Literal["yes", "no"] = "no",
    access_allow = Depends(require_roles([UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    if is_active is not None:
        query = (
            select(User)
            .where(User.is_active == is_active)
        )
    else:
        query = (
            select(User)
        )

    result = await db.execute(query)
    data = result.scalars().all()

    users = [
        {
            "id": user.id, 
            "email": user.email,
            "restaurant_name": user.restaurant_name,
            "full_name": user.full_name,
            "position": user.position,
            "role": user.role,
            "hire_date": user.hire_date.isoformat(),
            "is_active": user.is_active
        }
        for user in data
    ]
    if users: 
        if create_file == "yes":
            create_report.delay(users)
        return users

    raise HTTPException(status_code=404, detail="Пользователи не найдены")