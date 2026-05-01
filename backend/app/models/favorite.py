from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Favorite(BaseModel):
    __tablename__ = "favorites"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_type = Column(String(20), nullable=False)  # book, store
    item_id = Column(Integer, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    book = relationship("Book", back_populates="favorites")
    store = relationship("Store", back_populates="favorites")
