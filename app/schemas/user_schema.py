from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

