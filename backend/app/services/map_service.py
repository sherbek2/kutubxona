from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.book import Book
from app.models.store import Store
from typing import List, Optional
import math

class MapService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in kilometers"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    async def get_nearby_items(
        self,
        lat: float,
        lng: float,
        radius: float,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List:
        items = []
        
        # Get nearby books
        if type is None or type == "book":
            books_query = select(Book).where(
                and_(
                    Book.status == "active",
                    Book.latitude.isnot(None),
                    Book.longitude.isnot(None)
                )
            )
            
            if category_id:
                books_query = books_query.where(Book.category_id == category_id)
            
            if search:
                search_term = f"%{search}%"
                books_query = books_query.where(
                    or_(
                        Book.title.ilike(search_term),
                        Book.author.ilike(search_term)
                    )
                )
            
            books_result = await self.db.execute(books_query)
            books = books_result.scalars().all()
            
            for book in books:
                distance = self.calculate_distance(lat, lng, book.latitude, book.longitude)
                if distance <= radius:
                    book.distance = distance
                    items.append(book)
        
        # Get nearby stores
        if type is None or type == "store":
            stores_query = select(Store).where(
                and_(
                    Store.status == "active",
                    Store.latitude.isnot(None),
                    Store.longitude.isnot(None)
                )
            )
            
            if search:
                search_term = f"%{search}%"
                stores_query = stores_query.where(
                    or_(
                        Store.name.ilike(search_term),
                        Store.description.ilike(search_term)
                    )
                )
            
            stores_result = await self.db.execute(stores_query)
            stores = stores_result.scalars().all()
            
            for store in stores:
                distance = self.calculate_distance(lat, lng, store.latitude, store.longitude)
                if distance <= radius:
                    store.distance = distance
                    items.append(store)
        
        # Sort by distance
        items.sort(key=lambda x: x.distance)
        
        return items
    
    async def get_book_location(self, book_id: int) -> Optional[dict]:
        result = await self.db.execute(
            select(Book).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        
        if not book or not book.latitude or not book.longitude:
            return None
        
        return {
            "latitude": float(book.latitude),
            "longitude": float(book.longitude),
            "address": book.location,
            "title": book.title,
            "author": book.author
        }
    
    async def get_store_location(self, store_id: int) -> Optional[dict]:
        result = await self.db.execute(
            select(Store).where(Store.id == store_id)
        )
        store = result.scalar_one_or_none()
        
        if not store or not store.latitude or not store.longitude:
            return None
        
        return {
            "latitude": float(store.latitude),
            "longitude": float(store.longitude),
            "address": store.address,
            "name": store.name,
            "category": store.category
        }
