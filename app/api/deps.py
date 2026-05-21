from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.models.user_model import User
from app.core.security import decode_token
from app.core.database import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    user = decode_token(token)

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user["user_id"]

    user_in_db = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    current_user = user_in_db.scalar_one_or_none()

    if current_user:
        return current_user
    
    raise HTTPException(status_code=404, detail="Пользователь не найден")

def require_roles(allowed_roles):
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user.role in allowed_roles:
            return current_user
        else:
            raise HTTPException(status_code=404, detail="Нет доступа")
        
    return role_checker