from pydantic import BaseModel
from datetime import datetime

class RewardCreate(BaseModel):
    title: str
    description: str
    cost_points: int

class RewardResponse(BaseModel):
    id: int
    title: str
    description: str
    cost_points: str
    is_active: bool
    created_at: datetime