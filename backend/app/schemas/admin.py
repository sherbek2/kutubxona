from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AdminStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_books: int
    active_books: int
    total_stores: int
    active_stores: int
    total_reviews: int
    total_messages: int
    total_reports: int

class UserManagementResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    is_active: bool
    is_blocked: bool
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None

class BookManagementResponse(BaseModel):
    id: int
    title: str
    author: str
    type: str
    price: Optional[int] = None
    status: str
    seller_id: int
    created_at: datetime
    seller: Optional[dict] = None
