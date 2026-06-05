from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, extract, desc
from app.models.sale import Sale
from app.models.item import Item
from app.schemas.report import DailyReportResponse, MonthlyReportResponse, TopItem

class ReportService:
    @staticmethod
    async def get_daily_report(db: AsyncSession, report_date: date) -> DailyReportResponse:
        result = await db.execute(
            select(
                func.count(Sale.id),
                func.coalesce(func.sum(Sale.quantity), 0),
                func.coalesce(func.sum(Sale.total_price), 0)
            ).filter(Sale.sale_date == report_date)
        )
        row = result.fetchone()
        
        return DailyReportResponse(
            date=report_date.isoformat(),
            total_transactions=row[0] or 0,
            total_quantity=row[1] or 0,
            total_revenue=row[2] or 0.0
        )

    @staticmethod
    async def get_monthly_report(db: AsyncSession, year: int, month: int) -> MonthlyReportResponse:
        result = await db.execute(
            select(
                func.count(Sale.id),
                func.coalesce(func.sum(Sale.quantity), 0),
                func.coalesce(func.sum(Sale.total_price), 0)
            ).filter(
                extract('year', Sale.sale_date) == year,
                extract('month', Sale.sale_date) == month
            )
        )
        row = result.fetchone()
        
        return MonthlyReportResponse(
            year=year,
            month=month,
            total_transactions=row[0] or 0,
            total_quantity=row[1] or 0,
            total_revenue=row[2] or 0.0
        )

    @staticmethod
    async def get_top_items(db: AsyncSession, limit: int = 10) -> list[TopItem]:
        result = await db.execute(
            select(
                Item.name,
                func.coalesce(func.sum(Sale.quantity), 0).label('total_qty')
            )
            .join(Sale, Sale.item_id == Item.id)
            .group_by(Item.name)
            .order_by(desc('total_qty'))
            .limit(limit)
        )
        
        rows = result.fetchall()
        return [TopItem(item_name=row[0], quantity_sold=row[1]) for row in rows]
