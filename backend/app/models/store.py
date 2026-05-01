from sqlalchemy import Column, String, Integer, DECIMAL, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Store(BaseModel):
    __tablename__ = "stores"
    
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)  # bookstore, library, reading_cafe, etc.
    description = Column(Text, nullable=False)
    address = Column(String(300), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    website = Column(String(200))
    facebook = Column(String(100))
    instagram = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="active")  # active, inactive, suspended
    is_verified = Column(Boolean, default=False)
    rating = Column(DECIMAL(3, 2), default=0.00)
    total_reviews = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    books_count = Column(Integer, default=0)
    
    # Relationships
    owner = relationship("User", back_populates="stores")
    opening_hours = relationship("StoreOpeningHours", back_populates="store")
    features = relationship("StoreFeature", back_populates="store")
    images = relationship("StoreImage", back_populates="store")
    store_books = relationship("StoreBook", back_populates="store")
    reviews = relationship("Review", back_populates="store")

class StoreOpeningHours(BaseModel):
    __tablename__ = "store_opening_hours"
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    day_of_week = Column(String(10), nullable=False)  # monday, tuesday, etc.
    open_time = Column(String(5))  # HH:MM
    close_time = Column(String(5))  # HH:MM
    is_closed = Column(Boolean, default=False)
    
    # Relationships
    store = relationship("Store", back_populates="opening_hours")

class StoreFeature(BaseModel):
    __tablename__ = "store_features"
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    feature_name = Column(String(50), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="features")

class StoreImage(BaseModel):
    __tablename__ = "store_images"
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(200))
    sort_order = Column(Integer, default=0)
    
    # Relationships
    store = relationship("Store", back_populates="images")

class StoreBook(BaseModel):
    __tablename__ = "store_books"
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=1)
    isbn = Column(String(20))
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    
    # Relationships
    store = relationship("Store", back_populates="store_books")
    category = relationship("Category")
