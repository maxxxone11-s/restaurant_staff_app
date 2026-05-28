from fastapi import Request, HTTPException, Depends

from app.core.redis import redis_client

async def login_rate_limit(request: Request):
    ip = request.client.host # .client.host - IP адрес клиента
    key = f"login_rate_limit:{ip}"

    current_count = await redis_client.incr(key)

    if current_count == 1:
        await redis_client.expire(key, 60)

    if current_count > 5:
        raise HTTPException(status_code=429, detail="Лимит превышен, попробуйте позже")
