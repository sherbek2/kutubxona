from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    item_type: str
    item_id: int
    created_at: datetime
    item: Optional[dict] = None
    
    class Config:
        from_attributes = True

class FavoriteListResponse(BaseModel):
    favorites: List[FavoriteResponse]
    pagination: dict
