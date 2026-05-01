from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from app.models.user import User
from app.models.book import Book
from app.models.store import Store
from app.schemas.user import UserUpdate, UserStats

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id)
        
        # Update only provided fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user_stats(self, user_id: int) -> UserStats:
        # Get total books count
        books_result = await self.db.execute(
            select(func.count(Book.id)).where(Book.seller_id == user_id)
        )
        total_books = books_result.scalar() or 0
        
        # Get active books count
        active_books_result = await self.db.execute(
            select(func.count(Book.id)).where(
                Book.seller_id == user_id,
                Book.status == "active"
            )
        )
        active_books = active_books_result.scalar() or 0
        
        # Get total stores count
        stores_result = await self.db.execute(
            select(func.count(Store.id)).where(Store.owner_id == user_id)
        )
        total_stores = stores_result.scalar() or 0
        
        # Get followers count (this would need to be implemented)
        followers = 0
        
        return UserStats(
            total_books=total_books,
            active_books=active_books,
            total_stores=total_stores,
            followers=followers
        )
