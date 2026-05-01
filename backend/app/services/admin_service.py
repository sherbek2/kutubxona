from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from app.models.user import User
from app.models.book import Book
from app.models.store import Store
from app.models.report import Report
from typing import List, Dict, Any

class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_platform_stats(self) -> Dict[str, Any]:
        # Get user stats
        users_result = await self.db.execute(
            select(
                func.count(User.id).label("total_users"),
                func.sum(func.case([(User.is_active == True, 1)], else_=0)).label("active_users")
            )
        )
        user_stats = users_result.first()
        
        # Get book stats
        books_result = await self.db.execute(
            select(
                func.count(Book.id).label("total_books"),
                func.sum(func.case([(Book.status == "active", 1)], else_=0)).label("active_books")
            )
        )
        book_stats = books_result.first()
        
        # Get store stats
        stores_result = await self.db.execute(
            select(
                func.count(Store.id).label("total_stores"),
                func.sum(func.case([(Store.status == "active", 1)], else_=0)).label("active_stores")
            )
        )
        store_stats = stores_result.first()
        
        # Get other stats
        reviews_result = await self.db.execute(select(func.count()).select_from(select(1).where(Book.id > 0).subquery()))
        total_reviews = reviews_result.scalar() or 0
        
        messages_result = await self.db.execute(select(func.count()).select_from(select(1).where(Book.id > 0).subquery()))
        total_messages = messages_result.scalar() or 0
        
        reports_result = await self.db.execute(select(func.count(Report.id)))
        total_reports = reports_result.scalar() or 0
        
        return {
            "total_users": user_stats.total_users or 0,
            "active_users": user_stats.active_users or 0,
            "total_books": book_stats.total_books or 0,
            "active_books": book_stats.active_books or 0,
            "total_stores": store_stats.total_stores or 0,
            "active_stores": store_stats.active_stores or 0,
            "total_reviews": total_reviews,
            "total_messages": total_messages,
            "total_reports": total_reports
        }
    
    async def get_users_for_management(
        self,
        skip: int = 0,
        limit: int = 50,
        status: str = None,
        search: str = None
    ) -> List[User]:
        query = select(User)
        
        if status == "active":
            query = query.where(User.is_active == True)
        elif status == "inactive":
            query = query.where(User.is_active == False)
        elif status == "blocked":
            query = query.where(User.is_blocked == True)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone.ilike(search_term)
                )
            )
        
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return users
    
    async def update_user_status(self, user_id: int, new_status: str):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise Exception("User not found")
        
        if new_status == "active":
            user.is_active = True
            user.is_blocked = False
        elif new_status == "inactive":
            user.is_active = False
            user.is_blocked = False
        elif new_status == "blocked":
            user.is_active = False
            user.is_blocked = True
        
        await self.db.commit()
    
    async def get_books_for_management(
        self,
        skip: int = 0,
        limit: int = 50,
        status: str = None,
        search: str = None
    ) -> List[Book]:
        query = select(Book).options(selectinload(Book.seller))
        
        if status:
            query = query.where(Book.status == status)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term)
                )
            )
        
        query = query.order_by(Book.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        books = result.scalars().all()
        
        return books
    
    async def update_book_status(self, book_id: int, new_status: str):
        result = await self.db.execute(
            select(Book).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        
        if not book:
            raise Exception("Book not found")
        
        book.status = new_status
        await self.db.commit()
    
    async def get_reports_for_review(
        self,
        skip: int = 0,
        limit: int = 50,
        status: str = None
    ) -> List[Dict[str, Any]]:
        query = select(Report).options(
            selectinload(Report.reporter)
        )
        
        if status:
            query = query.where(Report.status == status)
        
        query = query.order_by(Report.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        reports = result.scalars().all()
        
        report_list = []
        for report in reports:
            report_dict = {
                "id": report.id,
                "reporter": {
                    "id": report.reporter.id,
                    "name": f"{report.reporter.first_name} {report.reporter.last_name}",
                    "email": report.reporter.email
                },
                "target_type": report.target_type,
                "target_id": report.target_id,
                "reason": report.reason,
                "description": report.description,
                "status": report.status,
                "created_at": report.created_at
            }
            report_list.append(report_dict)
        
        return report_list
