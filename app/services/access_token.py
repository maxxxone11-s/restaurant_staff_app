from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core.database import settings

def create_access_token(user_id, email):

    life_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"user_id": user_id, "email": email, "exp": int(life_time.timestamp())}

    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")

    return token

