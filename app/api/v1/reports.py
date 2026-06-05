from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.report import DailyReportResponse, MonthlyReportResponse, BestSellingResponse
from app.schemas.base import SuccessResponse
from app.services.report_service import ReportService

router = APIRouter()

@router.get("/daily", response_model=SuccessResponse[DailyReportResponse])
async def get_daily_report(
    date: date = Query(...), 
    db: AsyncSession = Depends(get_db)
):
    report = await ReportService.get_daily_report(db, date)
    return SuccessResponse(data=report)

@router.get("/monthly", response_model=SuccessResponse[MonthlyReportResponse])
async def get_monthly_report(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db)
):
    report = await ReportService.get_monthly_report(db, year, month)
    return SuccessResponse(data=report)

@router.get("/top-items", response_model=SuccessResponse[BestSellingResponse])
async def get_top_items(
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    top_items = await ReportService.get_top_items(db, limit)
    return SuccessResponse(data=BestSellingResponse(data=top_items))
