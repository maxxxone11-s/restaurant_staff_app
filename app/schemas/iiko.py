from pydantic import BaseModel

class IikoRequest(BaseModel):
    revenue: int