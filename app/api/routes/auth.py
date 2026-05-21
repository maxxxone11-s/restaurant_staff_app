from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.api.deps import get_db, get_current_user
from app.models.user_model import User
from app.core.security import hash_password, verify_password
from app.services.access_token import create_access_token
from app.core.roles import UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        position=user_data.position,
        restaurant_name=user_data.restaurant_name,
        role=UserRole.WAITER.value,
        hashed_password=hash_password(user_data.password)
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Пользователь с таким email уже существует.{str(e)}")

    return user

@router.post("/login")
async def login_user(
    user_data_login: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    email = user_data_login.email
    password = user_data_login.password

    result = await db.execute(
        select(User)
        .where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    is_password_valid = verify_password(password, user.hashed_password)

    if is_password_valid:
        access_token = create_access_token(user.id, user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=404, detail="Password don't correct")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user