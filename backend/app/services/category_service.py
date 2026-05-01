from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.category import Category
from app.schemas.category import CategoryCreate
from typing import List

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_categories(self) -> List[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.is_active == True)
            .order_by(Category.sort_order, Category.name)
        )
        categories = result.scalars().all()
        return categories
    
    async def get_category_by_id(self, category_id: int) -> Category:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        category = result.scalar_one_or_none()
        return category
    
    async def create_category(self, category_data: CategoryCreate) -> Category:
        # Check if slug already exists
        result = await self.db.execute(
            select(Category).where(Category.slug == category_data.slug)
        )
        existing_category = result.scalar_one_or_none()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists"
            )
        
        db_category = Category(
            name=category_data.name,
            slug=category_data.slug,
            description=category_data.description,
            icon=category_data.icon,
            parent_id=category_data.parent_id,
            sort_order=category_data.sort_order
        )
        
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        
        return db_category
