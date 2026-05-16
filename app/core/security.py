from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException, Depends
from dotenv import load_dotenv
import os

from app.api.deps import get_current_user
from app.core.roles import UserRole

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Ошибка: В токене отсутствуют необходимые поля.")
            
        return {"user_id": user_id, "email": email}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Ошибка: Срок действия токена истек.")
    
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Ошибка: Неверная подпись или испорченный токен.")
    

async def require_roles(
    user_role,
    current_user = Depends(get_current_user)
):
    if current_user.role != user_role:
        raise HTTPException(status_code=403, detail="Forbidden")