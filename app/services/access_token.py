from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(user_id, email):

    life_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"user_id": user_id, "email": email, "exp": int(life_time.timestamp())}

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

