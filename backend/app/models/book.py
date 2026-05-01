from sqlalchemy import Column, String, Integer, DECIMAL, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Book(BaseModel):
    __tablename__ = "books"
    
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    language = Column(String(50), nullable=False)
    year = Column(Integer)
    pages = Column(Integer)
    isbn = Column(String(20))
    condition = Column(String(20), default="new")
    type = Column(String(20), nullable=False)  # sell, free, rent
    price = Column(Integer)
    rent_price = Column(Integer)
    rent_duration = Column(String(20))
    location = Column(String(200))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="active")
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    contact_count = Column(Integer, default=0)
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    seller = relationship("User", back_populates="books")
    category = relationship("Category")
    images = relationship("BookImage", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    favorites = relationship("Favorite", back_populates="book")

class BookImage(BaseModel):
    __tablename__ = "book_images"
    
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(200))
    sort_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    
    # Relationships
    book = relationship("Book", back_populates="images")
