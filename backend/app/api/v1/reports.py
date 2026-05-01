from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.report import ReportCreate, ReportResponse
from app.services.report_service import ReportService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    report_service = ReportService(db)
    report = await report_service.create_report(current_user["id"], report_data)
    return ReportResponse.from_orm(report)

@router.get("/my-reports", response_model=List[ReportResponse])
async def get_my_reports(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    report_service = ReportService(db)
    reports = await report_service.get_user_reports(current_user["id"])
    return [ReportResponse.from_orm(report) for report in reports]
