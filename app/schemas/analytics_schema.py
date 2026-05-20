from pydantic import BaseModel

class RevenueResponse(BaseModel):
    total_revenue: int

class TopWaitersResponse(BaseModel):
    full_name: str
    total_revenue: int

