from sqlalchemy import Column, String, Integer
from app.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500))
    icon = Column(String(50))
    parent_id = Column(Integer)
    sort_order = Column(Integer, default=0)
    is_active = Column(String(20), default=True)
