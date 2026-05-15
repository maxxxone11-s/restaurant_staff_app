from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.user_schema import UserCreate, UserResponse
from app.api.deps import get_db
from app.models.user_model import User
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        role="user",
        hashed_password=hash_password(user_data.password)
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")

    return user

@router.post("/login")
async def login_user(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .where(email == User.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    verify_password = verify_password(password, user.hashed_password)

    if verify_password:
        return create_access_token()

    raise HTTPException(status_code=404, detail="Password don't correct")
    
def create_access_token():
    return {"Login": "successful"}

def decode_token():
    pass