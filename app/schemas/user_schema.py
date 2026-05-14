from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
