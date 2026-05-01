from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewListResponse
from app.services.review_service import ReviewService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
async def create_review(
    review_data: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    review_service = ReviewService(db)
    review = await review_service.create_review(current_user["id"], review_data)
    return ReviewResponse.from_orm(review)

@router.get("/", response_model=ReviewListResponse)
async def get_reviews(
    target_type: str = Query(...),
    target_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    review_service = ReviewService(db)
    reviews, total = await review_service.get_reviews(
        target_type=target_type,
        target_id=target_id,
        skip=skip,
        limit=limit
    )
    
    return ReviewListResponse(
        reviews=[ReviewResponse.from_orm(review) for review in reviews],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    review_service = ReviewService(db)
    review = await review_service.update_review(review_id, current_user["id"], review_data)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or you don't have permission"
        )
    return ReviewResponse.from_orm(review)

@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    review_service = ReviewService(db)
    success = await review_service.delete_review(review_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or you don't have permission"
        )
    return {"message": "Review deleted successfully"}
