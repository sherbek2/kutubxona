from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.notification import NotificationResponse, NotificationListResponse
from app.services.notification_service import NotificationService
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    notifications, total = await notification_service.get_user_notifications(
        current_user["id"], skip, limit, unread_only
    )
    
    return NotificationListResponse(
        notifications=[NotificationResponse.from_orm(notif) for notif in notifications],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    await notification_service.mark_as_read(notification_id, current_user["id"])
    return {"message": "Notification marked as read"}

@router.put("/read-all")
async def mark_all_notifications_as_read(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    await notification_service.mark_all_as_read(current_user["id"])
    return {"message": "All notifications marked as read"}

@router.get("/unread-count")
async def get_unread_count(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    count = await notification_service.get_unread_count(current_user["id"])
    return {"unread_count": count}
