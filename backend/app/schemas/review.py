from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    target_type: str  # book, store
    target_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    @validator('target_type')
    def validate_target_type(cls, v):
        if v not in ['book', 'store']:
            raise ValueError('Target type must be book or store')
        return v

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    reviewer_id: int
    is_verified: bool
    helpful_count: int
    created_at: datetime
    reviewer: Optional[dict] = None
    
    class Config:
        from_attributes = True

class ReviewListResponse(BaseModel):
    reviews: List[ReviewResponse]
    pagination: dict
