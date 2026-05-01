from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.book import Book
from app.models.store import Store
from app.models.category import Category
from typing import List, Tuple, Optional

class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def search(
        self,
        query: str,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[float] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List, int]:
        results = []
        total = 0
        
        search_term = f"%{query}%"
        
        # Search books
        if type is None or type == "book":
            books_query = select(Book).where(
                and_(
                    Book.status == "active",
                    or_(
                        Book.title.ilike(search_term),
                        Book.author.ilike(search_term),
                        Book.description.ilike(search_term)
                    )
                )
            )
            
            if category_id:
                books_query = books_query.where(Book.category_id == category_id)
            
            books_result = await self.db.execute(books_query)
            books = books_result.scalars().all()
            
            for book in books:
                book.search_type = "book"
                results.append(book)
            
            total += len(books)
        
        # Search stores
        if type is None or type == "store":
            stores_query = select(Store).where(
                and_(
                    Store.status == "active",
                    or_(
                        Store.name.ilike(search_term),
                        Store.description.ilike(search_term),
                        Store.address.ilike(search_term)
                    )
                )
            )
            
            stores_result = await self.db.execute(stores_query)
            stores = stores_result.scalars().all()
            
            for store in stores:
                store.search_type = "store"
                results.append(store)
            
            total += len(stores)
        
        # Sort by relevance (simple implementation)
        results.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply pagination
        paginated_results = results[skip:skip + limit]
        
        return paginated_results, total
    
    async def get_suggestions(
        self,
        query: str,
        type: Optional[str] = None,
        limit: int = 10
    ) -> List[str]:
        suggestions = []
        search_term = f"%{query}%"
        
        # Get book titles
        if type is None or type == "book":
            books_result = await self.db.execute(
                select(Book.title).where(
                    and_(
                        Book.status == "active",
                        Book.title.ilike(search_term)
                    )
                ).limit(limit)
            )
            book_titles = books_result.scalars().all()
            suggestions.extend(book_titles)
        
        # Get store names
        if type is None or type == "store":
            stores_result = await self.db.execute(
                select(Store.name).where(
                    and_(
                        Store.status == "active",
                        Store.name.ilike(search_term)
                    )
                ).limit(limit)
            )
            store_names = stores_result.scalars().all()
            suggestions.extend(store_names)
        
        # Get author names
        if type is None or type == "book":
            authors_result = await self.db.execute(
                select(Book.author).where(
                    and_(
                        Book.status == "active",
                        Book.author.ilike(search_term)
                    )
                ).distinct().limit(limit)
            )
            author_names = authors_result.scalars().all()
            suggestions.extend(author_names)
        
        # Remove duplicates and limit
        suggestions = list(set(suggestions))[:limit]
        
        return suggestions
    
    async def get_popular_searches(
        self,
        type: Optional[str] = None,
        limit: int = 10
    ) -> List[str]:
        # This would typically be implemented with a search analytics table
        # For now, return some popular categories
        popular_terms = [
            "Alkimyogar",
            "O'tgan kunlar",
            "Rich Dad Poor Dad",
            "Shaytanat",
            "Dasturlash",
            "Romantika",
            "Tarix",
            "Bolalar adabiyoti",
            "Ilmiy-fantastika",
            "Detektiv"
        ]
        
        return popular_terms[:limit]
