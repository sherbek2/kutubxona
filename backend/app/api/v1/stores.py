from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.store import StoreCreate, StoreResponse, StoreListResponse, StoreUpdate
from app.services.store_service import StoreService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=StoreResponse)
async def create_store(
    store_data: StoreCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    store = await store_service.create_store(current_user["id"], store_data)
    return StoreResponse.from_orm(store)

@router.get("/", response_model=StoreListResponse)
async def get_stores(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radius: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    stores, total = await store_service.get_stores(
        skip=skip,
        limit=limit,
        category=category,
        search=search,
        lat=lat,
        lng=lng,
        radius=radius
    )
    
    return StoreListResponse(
        stores=[StoreResponse.from_orm(store) for store in stores],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.get("/{store_id}", response_model=StoreResponse)
async def get_store_by_id(
    store_id: int,
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    store = await store_service.get_store_by_id(store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    return StoreResponse.from_orm(store)

@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    store = await store_service.update_store(store_id, current_user["id"], store_data)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found or you don't have permission"
        )
    return StoreResponse.from_orm(store)

@router.delete("/{store_id}")
async def delete_store(
    store_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    success = await store_service.delete_store(store_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found or you don't have permission"
        )
    return {"message": "Store deleted successfully"}

@router.post("/{store_id}/follow")
async def follow_store(
    store_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    await store_service.follow_store(store_id, current_user["id"])
    return {"message": "Store followed successfully"}

@router.delete("/{store_id}/follow")
async def unfollow_store(
    store_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    store_service = StoreService(db)
    await store_service.unfollow_store(store_id, current_user["id"])
    return {"message": "Store unfollowed successfully"}
