from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models.store import Store, StoreOpeningHours, StoreFeature, StoreImage, StoreBook
from app.models.favorite import Favorite
from app.schemas.store import StoreCreate, StoreUpdate
from typing import List, Tuple, Optional

class StoreService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_store(self, user_id: int, store_data: StoreCreate) -> Store:
        # Create store
        db_store = Store(
            name=store_data.name,
            category=store_data.category,
            description=store_data.description,
            address=store_data.address,
            latitude=store_data.latitude,
            longitude=store_data.longitude,
            phone=store_data.phone,
            email=store_data.email,
            website=store_data.website,
            facebook=store_data.facebook,
            instagram=store_data.instagram,
            owner_id=user_id
        )
        
        self.db.add(db_store)
        await self.db.commit()
        await self.db.refresh(db_store)
        
        # Add opening hours if provided
        if store_data.opening_hours:
            for hour_data in store_data.opening_hours:
                opening_hour = StoreOpeningHours(
                    store_id=db_store.id,
                    day_of_week=hour_data["day_of_week"],
                    open_time=hour_data.get("open_time"),
                    close_time=hour_data.get("close_time"),
                    is_closed=hour_data.get("is_closed", False)
                )
                self.db.add(opening_hour)
        
        # Add features if provided
        if store_data.features:
            for feature_name in store_data.features:
                feature = StoreFeature(
                    store_id=db_store.id,
                    feature_name=feature_name
                )
                self.db.add(feature)
        
        # Add images if provided
        if store_data.images:
            for i, image_url in enumerate(store_data.images):
                store_image = StoreImage(
                    store_id=db_store.id,
                    image_url=image_url,
                    sort_order=i
                )
                self.db.add(store_image)
        
        await self.db.commit()
        return db_store
    
    async def get_stores(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[float] = None
    ) -> Tuple[List[Store], int]:
        query = select(Store).where(Store.status == "active")
        
        # Apply filters
        if category:
            query = query.where(Store.category == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Store.name.ilike(search_term),
                    Store.description.ilike(search_term),
                    Store.address.ilike(search_term)
                )
            )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(Store.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        stores = result.scalars().all()
        
        return stores, total
    
    async def get_store_by_id(self, store_id: int) -> Store:
        result = await self.db.execute(
            select(Store)
            .options(
                selectinload(Store.opening_hours),
                selectinload(Store.features),
                selectinload(Store.images)
            )
            .where(Store.id == store_id)
        )
        store = result.scalar_one_or_none()
        return store
    
    async def update_store(self, store_id: int, user_id: int, store_data: StoreUpdate) -> Store:
        store = await self.get_store_by_id(store_id)
        
        if not store or store.owner_id != user_id:
            return None
        
        # Update only provided fields
        update_data = store_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(store, field, value)
        
        await self.db.commit()
        await self.db.refresh(store)
        return store
    
    async def delete_store(self, store_id: int, user_id: int) -> bool:
        store = await self.get_store_by_id(store_id)
        
        if not store or store.owner_id != user_id:
            return False
        
        store.status = "inactive"
        await self.db.commit()
        return True
    
    async def follow_store(self, store_id: int, user_id: int):
        # Check if already following
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == "store",
                    Favorite.item_id == store_id
                )
            )
        )
        existing_favorite = result.scalar_one_or_none()
        
        if not existing_favorite:
            favorite = Favorite(
                user_id=user_id,
                item_type="store",
                item_id=store_id
            )
            self.db.add(favorite)
            
            # Increment followers count
            store = await self.get_store_by_id(store_id)
            if store:
                store.followers_count += 1
            
            await self.db.commit()
    
    async def unfollow_store(self, store_id: int, user_id: int):
        result = await self.db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.item_type == "store",
                    Favorite.item_id == store_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        
        if favorite:
            await self.db.delete(favorite)
            
            # Decrement followers count
            store = await self.get_store_by_id(store_id)
            if store and store.followers_count > 0:
                store.followers_count -= 1
            
            await self.db.commit()
