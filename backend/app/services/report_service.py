from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from app.models.report import Report
from app.models.book import Book
from app.models.store import Store
from app.models.user import User
from app.schemas.report import ReportCreate
from typing import List

class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_report(self, user_id: int, report_data: ReportCreate) -> Report:
        # Validate target exists
        if report_data.target_type == "book":
            book_result = await self.db.execute(
                select(Book).where(Book.id == report_data.target_id)
            )
            book = book_result.scalar_one_or_none()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
        
        elif report_data.target_type == "store":
            store_result = await self.db.execute(
                select(Store).where(Store.id == report_data.target_id)
            )
            store = store_result.scalar_one_or_none()
            if not store:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Store not found"
                )
        
        elif report_data.target_type == "user":
            user_result = await self.db.execute(
                select(User).where(User.id == report_data.target_id)
            )
            user = user_result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid target type"
            )
        
        # Check if user already reported this item
        existing_result = await self.db.execute(
            select(Report).where(
                and_(
                    Report.reporter_id == user_id,
                    Report.target_type == report_data.target_type,
                    Report.target_id == report_data.target_id
                )
            )
        )
        existing_report = existing_result.scalar_one_or_none()
        
        if existing_report:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reported this item"
            )
        
        # Create report
        db_report = Report(
            reporter_id=user_id,
            target_type=report_data.target_type,
            target_id=report_data.target_id,
            reason=report_data.reason,
            description=report_data.description
        )
        
        self.db.add(db_report)
        await self.db.commit()
        await self.db.refresh(db_report)
        
        return db_report
    
    async def get_user_reports(self, user_id: int) -> List[Report]:
        result = await self.db.execute(
            select(Report).where(Report.reporter_id == user_id)
            .order_by(Report.created_at.desc())
        )
        reports = result.scalars().all()
        return reports
