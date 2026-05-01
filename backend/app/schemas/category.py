from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    slug: str

class CategoryResponse(CategoryBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
