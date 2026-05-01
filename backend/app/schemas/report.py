from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ReportBase(BaseModel):
    target_type: str  # book, store, user
    target_id: int
    reason: str
    description: Optional[str] = None

class ReportCreate(ReportBase):
    @validator('target_type')
    def validate_target_type(cls, v):
        if v not in ['book', 'store', 'user']:
            raise ValueError('Target type must be book, store, or user')
        return v

class ReportResponse(ReportBase):
    id: int
    reporter_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
