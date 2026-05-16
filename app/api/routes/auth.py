from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.user_schema import UserCreate, UserResponse
from app.api.deps import get_db
from app.models.user_model import User
from app.core.security import hash_password, verify_password, decode_token
from app.services.access_token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role, "full_name": current_user.full_name}