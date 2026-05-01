from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    category_id: Optional[int] = None
    language: str
    year: Optional[int] = None
    pages: Optional[int] = None
    isbn: Optional[str] = None
    condition: str = "new"
    type: str  # sell, free, rent
    price: Optional[int] = None
    rent_price: Optional[int] = None
    rent_duration: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BookCreate(BookBase):
    images: Optional[List[str]] = []
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['sell', 'free', 'rent']:
            raise ValueError('Type must be sell, free, or rent')
        return v
    
    @validator('price')
    def validate_price(cls, v, values):
        if values.get('type') == 'sell' and (not v or v <= 0):
            raise ValueError('Price is required for sell type')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None

class BookResponse(BookBase):
    id: int
    seller_id: int
    status: str
    is_featured: bool
    view_count: int
    like_count: int
    contact_count: int
    created_at: datetime
    updated_at: datetime
    seller: Optional[dict] = None
    category: Optional[dict] = None
    images: List[str] = []
    distance: Optional[float] = None
    
    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    books: List[BookResponse]
    pagination: dict
