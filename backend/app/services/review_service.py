from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from app.models.review import Review
from app.models.book import Book
from app.models.store import Store
from app.schemas.review import ReviewCreate, ReviewUpdate
from typing import List, Tuple

class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_review(self, user_id: int, review_data: ReviewCreate) -> Review:
        # Check if user already reviewed this item
        result = await self.db.execute(
            select(Review).where(
                and_(
                    Review.reviewer_id == user_id,
                    Review.target_type == review_data.target_type,
                    Review.target_id == review_data.target_id
                )
            )
        )
        existing_review = result.scalar_one_or_none()
        
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this item"
            )
        
        # Create review
        db_review = Review(
            reviewer_id=user_id,
            target_type=review_data.target_type,
            target_id=review_data.target_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        
        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)
        
        # Update target rating
        await self._update_target_rating(review_data.target_type, review_data.target_id)
        
        return db_review
    
    async def get_reviews(
        self,
        target_type: str,
        target_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Review], int]:
        query = select(Review).where(
            and_(
                Review.target_type == target_type,
                Review.target_id == target_id
            )
        )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Review.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        reviews = result.scalars().all()
        
        return reviews, total
    
    async def update_review(self, review_id: int, user_id: int, review_data: ReviewUpdate) -> Review:
        result = await self.db.execute(
            select(Review).where(
                and_(
                    Review.id == review_id,
                    Review.reviewer_id == user_id
                )
            )
        )
        review = result.scalar_one_or_none()
        
        if not review:
            return None
        
        # Update only provided fields
        update_data = review_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(review, field, value)
        
        await self.db.commit()
        await self.db.refresh(review)
        
        # Update target rating
        await self._update_target_rating(review.target_type, review.target_id)
        
        return review
    
    async def delete_review(self, review_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(Review).where(
                and_(
                    Review.id == review_id,
                    Review.reviewer_id == user_id
                )
            )
        )
        review = result.scalar_one_or_none()
        
        if not review:
            return False
        
        target_type = review.target_type
        target_id = review.target_id
        
        await self.db.delete(review)
        await self.db.commit()
        
        # Update target rating
        await self._update_target_rating(target_type, target_id)
        
        return True
    
    async def _update_target_rating(self, target_type: str, target_id: int):
        # Calculate new average rating
        result = await self.db.execute(
            select(func.avg(Review.rating), func.count(Review.id)).where(
                and_(
                    Review.target_type == target_type,
                    Review.target_id == target_id
                )
            )
        )
        avg_rating, count = result.first()
        
        if target_type == "book":
            book_result = await self.db.execute(
                select(Book).where(Book.id == target_id)
            )
            book = book_result.scalar_one_or_none()
            if book:
                book.rating = float(avg_rating) if avg_rating else 0.0
                book.total_reviews = int(count) if count else 0
                await self.db.commit()
        
        elif target_type == "store":
            store_result = await self.db.execute(
                select(Store).where(Store.id == target_id)
            )
            store = store_result.scalar_one_or_none()
            if store:
                store.rating = float(avg_rating) if avg_rating else 0.0
                store.total_reviews = int(count) if count else 0
                await self.db.commit()
