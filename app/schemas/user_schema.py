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
    full_name: str
    role: str
    hire_date: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

