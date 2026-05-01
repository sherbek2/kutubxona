from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.admin import AdminStatsResponse, UserManagementResponse, BookManagementResponse
from app.services.admin_service import AdminService
from app.core.security import get_current_user, require_admin

router = APIRouter()

@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    stats = await admin_service.get_platform_stats()
    return AdminStatsResponse.from_orm(stats)

@router.get("/users", response_model=List[UserManagementResponse])
async def get_users_for_management(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    users = await admin_service.get_users_for_management(skip, limit, status, search)
    return [UserManagementResponse.from_orm(user) for user in users]

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    new_status: str,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    await admin_service.update_user_status(user_id, new_status)
    return {"message": "User status updated successfully"}

@router.get("/books", response_model=List[BookManagementResponse])
async def get_books_for_management(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    books = await admin_service.get_books_for_management(skip, limit, status, search)
    return [BookManagementResponse.from_orm(book) for book in books]

@router.put("/books/{book_id}/status")
async def update_book_status(
    book_id: int,
    new_status: str,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    await admin_service.update_book_status(book_id, new_status)
    return {"message": "Book status updated successfully"}

@router.get("/reports", response_model=List[dict])
async def get_reports_for_review(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    admin_service = AdminService(db)
    reports = await admin_service.get_reports_for_review(skip, limit, status)
    return reports
