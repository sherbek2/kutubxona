from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"
    
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_type = Column(String(20), nullable=False)  # book, store
    target_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String(1000))
    is_verified = Column(Boolean, default=False)  # admin tomonidan tasdiqlangan
    helpful_count = Column(Integer, default=0)
    
    # Relationships
    reviewer = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    store = relationship("Store", back_populates="reviews")
