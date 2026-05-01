from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.favorite import FavoriteResponse, FavoriteListResponse
from app.services.favorite_service import FavoriteService
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=FavoriteListResponse)
async def get_favorites(
    type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite_service = FavoriteService(db)
    favorites, total = await favorite_service.get_user_favorites(
        current_user["id"], type, skip, limit
    )
    
    return FavoriteListResponse(
        favorites=[FavoriteResponse.from_orm(fav) for fav in favorites],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.post("/{item_type}/{item_id}")
async def add_to_favorites(
    item_type: str,
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite_service = FavoriteService(db)
    await favorite_service.add_to_favorites(current_user["id"], item_type, item_id)
    return {"message": "Added to favorites successfully"}

@router.delete("/{item_type}/{item_id}")
async def remove_from_favorites(
    item_type: str,
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite_service = FavoriteService(db)
    await favorite_service.remove_from_favorites(current_user["id"], item_type, item_id)
    return {"message": "Removed from favorites successfully"}

@router.get("/check/{item_type}/{item_id}")
async def check_is_favorite(
    item_type: str,
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite_service = FavoriteService(db)
    is_favorite = await favorite_service.is_favorite(current_user["id"], item_type, item_id)
    return {"is_favorite": is_favorite}
