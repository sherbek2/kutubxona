from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from app.models.favorite import Favorite
from app.models.book import Book
from app.models.store import Store
from typing import List, Tuple

class FavoriteService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_favorites(
        self,
        user_id: int,
        type: str = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Favorite], int]:
        query = select(Favorite).where(Favorite.user_id == user_id)
        
        if type:
            query = query.where(Favorite.item_type == type)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Favorite.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        favorites = result.scalars().all()
        
        return favorites, total
    
    async def add_to_favorites(self, user_id: int, item_type: str, item_id: int):
        # Check if already in favorites
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == item_type,
                    Favorite.item_id == item_id
                )
            )
        )
        existing_favorite = result.scalar_one_or_none()
        
        if existing_favorite:
            return  # Already in favorites
        
        # Validate item exists
        if item_type == "book":
            book_result = await self.db.execute(
                select(Book).where(Book.id == item_id)
            )
            book = book_result.scalar_one_or_none()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
        
        elif item_type == "store":
            store_result = await self.db.execute(
                select(Store).where(Store.id == item_id)
            )
            store = store_result.scalar_one_or_none()
            if not store:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Store not found"
                )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item type"
            )
        
        # Add to favorites
        favorite = Favorite(
            user_id=user_id,
            item_type=item_type,
            item_id=item_id
        )
        
        self.db.add(favorite)
        await self.db.commit()
    
    async def remove_from_favorites(self, user_id: int, item_type: str, item_id: int):
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == item_type,
                    Favorite.item_id == item_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        
        if favorite:
            await self.db.delete(favorite)
            await self.db.commit()
    
    async def is_favorite(self, user_id: int, item_type: str, item_id: int) -> bool:
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == item_type,
                    Favorite.item_id == item_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        return favorite is not None
