from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    restaurant_name: str
    position: str

class UserResponse(BaseModel):
    id: int
    email: str
    restaurant_name: str
    full_name: str
    points: int
    position: str
    role: str
    hire_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    position: str | None = None
    role: str | None = None
    restaurant_name: str | None = None
    is_active: bool | None = None