from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.search import SearchResponse, SearchSuggestionResponse
from app.services.search_service import SearchService

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    type: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    radius: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    results, total = await search_service.search(
        query=q,
        type=type,
        category_id=category_id,
        lat=lat,
        lng=lng,
        radius=radius,
        skip=skip,
        limit=limit
    )
    
    return SearchResponse(
        query=q,
        results=[SearchResponse.from_orm(result) for result in results],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    )

@router.get("/suggestions", response_model=SearchSuggestionResponse)
async def get_search_suggestions(
    q: str = Query(..., min_length=1),
    type: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    suggestions = await search_service.get_suggestions(q, type, limit)
    
    return SearchSuggestionResponse(
        query=q,
        suggestions=suggestions
    )

@router.get("/popular")
async def get_popular_searches(
    type: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    popular = await search_service.get_popular_searches(type, limit)
    
    return {"popular_searches": popular}
