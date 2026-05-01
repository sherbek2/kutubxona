from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MapItemResponse(BaseModel):
    id: int
    type: str  # book, store
    title: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    address: Optional[str] = None
    price: Optional[int] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    distance: Optional[float] = None
    
    class Config:
        from_attributes = True

class MapSearchResponse(BaseModel):
    items: List[MapItemResponse]
    center: dict
    radius: float
