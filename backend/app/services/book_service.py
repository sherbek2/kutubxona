from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models.book import Book, BookImage
from app.models.favorite import Favorite
from app.schemas.book import BookCreate, BookUpdate
from typing import List, Tuple, Optional
import math

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_book(self, user_id: int, book_data: BookCreate) -> Book:
        # Create book
        db_book = Book(
            title=book_data.title,
            author=book_data.author,
            description=book_data.description,
            category_id=book_data.category_id,
            language=book_data.language,
            year=book_data.year,
            pages=book_data.pages,
            isbn=book_data.isbn,
            condition=book_data.condition,
            type=book_data.type,
            price=book_data.price,
            rent_price=book_data.rent_price,
            rent_duration=book_data.rent_duration,
            location=book_data.location,
            latitude=book_data.latitude,
            longitude=book_data.longitude,
            seller_id=user_id
        )
        
        self.db.add(db_book)
        await self.db.commit()
        await self.db.refresh(db_book)
        
        # Add images if provided
        if book_data.images:
            for i, image_url in enumerate(book_data.images):
                book_image = BookImage(
                    book_id=db_book.id,
                    image_url=image_url,
                    sort_order=i,
                    is_primary=(i == 0)
                )
                self.db.add(book_image)
            
            await self.db.commit()
        
        return db_book
    
    async def get_books(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[float] = None
    ) -> Tuple[List[Book], int]:
        query = select(Book).where(Book.status == "active")
        
        # Apply filters
        if category_id:
            query = query.where(Book.category_id == category_id)
        
        if type:
            query = query.where(Book.type == type)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term),
                    Book.description.ilike(search_term)
                )
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Book.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        books = result.scalars().all()
        
        return books, total
    
    async def get_book_by_id(self, book_id: int) -> Book:
        result = await self.db.execute(
            select(Book)
            .options(selectinload(Book.images))
            .where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        return book
    
    async def update_book(self, book_id: int, user_id: int, book_data: BookUpdate) -> Book:
        book = await self.get_book_by_id(book_id)
        
        if not book or book.seller_id != user_id:
            return None
        
        # Update only provided fields
        update_data = book_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        
        await self.db.commit()
        await self.db.refresh(book)
        return book
    
    async def delete_book(self, book_id: int, user_id: int) -> bool:
        book = await self.get_book_by_id(book_id)
        
        if not book or book.seller_id != user_id:
            return False
        
        book.status = "deleted"
        await self.db.commit()
        return True
    
    async def like_book(self, book_id: int, user_id: int):
        # Check if already liked
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == "book",
                    Favorite.item_id == book_id
                )
            )
        )
        existing_favorite = result.scalar_one_or_none()
        
        if not existing_favorite:
            favorite = Favorite(
                user_id=user_id,
                item_type="book",
                item_id=book_id
            )
            self.db.add(favorite)
            
            # Increment like count
            book = await self.get_book_by_id(book_id)
            if book:
                book.like_count += 1
            
            await self.db.commit()
    
    async def unlike_book(self, book_id: int, user_id: int):
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == "book",
                    Favorite.item_id == book_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        
        if favorite:
            await self.db.delete(favorite)
            
            # Decrement like count
            book = await self.get_book_by_id(book_id)
            if book and book.like_count > 0:
                book.like_count -= 1
            
            await self.db.commit()
