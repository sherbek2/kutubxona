from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class StoreBase(BaseModel):
    name: str
    category: str
    description: str
    address: str
    latitude: float
    longitude: float
    phone: str
    email: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None

class StoreCreate(StoreBase):
    opening_hours: Optional[List[dict]] = []
    features: Optional[List[str]] = []
    images: Optional[List[str]] = []

class StoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None

class StoreResponse(StoreBase):
    id: int
    owner_id: int
    status: str
    is_verified: bool
    rating: float
    total_reviews: int
    followers_count: int
    books_count: int
    created_at: datetime
    owner: Optional[dict] = None
    opening_hours: List[dict] = []
    features: List[str] = []
    images: List[str] = []
    distance: Optional[float] = None
    
    class Config:
        from_attributes = True

class StoreListResponse(BaseModel):
    stores: List[StoreResponse]
    pagination: dict
