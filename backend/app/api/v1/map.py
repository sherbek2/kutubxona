from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.map import MapItemResponse, MapSearchResponse
from app.services.map_service import MapService

router = APIRouter()

@router.get("/items", response_model=MapSearchResponse)
async def get_map_items(
    lat: float = Query(...),
    lng: float = Query(...),
    radius: float = Query(..., ge=0.1, le=100),
    type: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    map_service = MapService(db)
    items = await map_service.get_nearby_items(
        lat=lat,
        lng=lng,
        radius=radius,
        type=type,
        category_id=category_id,
        search=search
    )
    
    return MapSearchResponse(
        items=[MapItemResponse.from_orm(item) for item in items],
        center={"lat": lat, "lng": lng},
        radius=radius
    )

@router.get("/books/{book_id}/location")
async def get_book_location(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    map_service = MapService(db)
    location = await map_service.get_book_location(book_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return location

@router.get("/stores/{store_id}/location")
async def get_store_location(
    store_id: int,
    db: AsyncSession = Depends(get_db)
):
    map_service = MapService(db)
    location = await map_service.get_store_location(store_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    return location
