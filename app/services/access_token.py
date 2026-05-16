from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.core.security import SECRET_KEY

def create_access_token(user_id, email):

    life_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"user_id": user_id, "email": email, "exp": int(life_time.timestamp())}

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    
        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None or email is None:
            print("Ошибка: В токене отсутствуют необходимые поля.")
            return None
        
        return {"user_id": user_id, "email": email}

    except jwt.ExpiredSignatureError:
        print("Ошибка: Срок действия токена истек.")
        return None
    except jwt.JWTError:
        print("Ошибка: Неверная подпись или испорченный токен.")
        return None