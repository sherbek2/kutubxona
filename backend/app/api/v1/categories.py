from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.category import CategoryResponse, CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    category_service = CategoryService(db)
    categories = await category_service.get_all_categories()
    return [CategoryResponse.from_orm(cat) for cat in categories]

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    category_service = CategoryService(db)
    category = await category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return CategoryResponse.from_orm(category)

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    category_service = CategoryService(db)
    category = await category_service.create_category(category_data)
    return CategoryResponse.from_orm(category)
