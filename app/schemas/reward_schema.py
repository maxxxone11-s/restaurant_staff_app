from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RewardCreate(BaseModel):
    title: str
    description: str
    cost_points: int

class RewardResponse(BaseModel):
    id: int
    title: str
    description: str
    cost_points: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RewardBuyResponse(BaseModel):
    reward: str
    price: int
    balance: int