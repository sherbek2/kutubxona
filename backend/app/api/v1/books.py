from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookListResponse, BookUpdate
from app.services.book_service import BookService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=BookResponse)
async def create_book(
    book_data: BookCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    book = await book_service.create_book(current_user["id"], book_data)
    return BookResponse.from_orm(book)

@router.get("/", response_model=BookListResponse)
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radius: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    books, total = await book_service.get_books(
        skip=skip,
        limit=limit,
        category_id=category_id,
        type=type,
        search=search,
        lat=lat,
        lng=lng,
        radius=radius
    )
    
    return BookListResponse(
        books=[BookResponse.from_orm(book) for book in books],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return BookResponse.from_orm(book)

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    book = await book_service.update_book(book_id, current_user["id"], book_data)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission"
        )
    return BookResponse.from_orm(book)

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    success = await book_service.delete_book(book_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found or you don't have permission"
        )
    return {"message": "Book deleted successfully"}

@router.post("/{book_id}/like")
async def like_book(
    book_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    await book_service.like_book(book_id, current_user["id"])
    return {"message": "Book liked successfully"}

@router.delete("/{book_id}/like")
async def unlike_book(
    book_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    await book_service.unlike_book(book_id, current_user["id"])
    return {"message": "Book unliked successfully"}
