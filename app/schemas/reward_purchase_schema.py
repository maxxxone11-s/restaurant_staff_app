from pydantic import BaseModel
from datetime import datetime

class RewardPurchaseResponse(BaseModel):
    id: int
    user_id: int
    reward_id: int
    cost_points: int
    purchased_at: datetime