from pydantic import BaseModel
from datetime import datetime

class ShiftClose(BaseModel):
    revenue: int

class ShiftResponse(BaseModel):
    id: int
    user_id: int
    open_shift: datetime
    closed_shift: datetime | None
    hours_worked: float | None
    revenue: int | None

class ShiftResponseOpen(BaseModel):
    id: int
    user_id: int
    open_shift: datetime
    closed_shift: datetime | None
    revenue: int | None

class ShiftResponseClosed(BaseModel):
    revenue: int
    points: int
    source: str