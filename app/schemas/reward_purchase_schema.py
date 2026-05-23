from pydantic import BaseModel
from datetime import datetime

class RewardPurchaseHistoryResponse(BaseModel):
    title: str
    cost_points: int
    purchased_at: datetime