from pydantic import BaseModel
from datetime import datetime

class PointsHistoryResponse(BaseModel):
    id: int
    amount: int
    type: str
    description: str
    created_at: datetime