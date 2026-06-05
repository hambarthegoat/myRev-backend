from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.schemas.base import SuccessResponse
from app.utils.pagination import PaginatedData, Pagination
from app.services.sale_service import SaleService

router = APIRouter()

@router.post("", response_model=SuccessResponse[SaleResponse])
async def create_sale(sale_in: SaleCreate, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.create_sale(db, sale_in)
    return SuccessResponse(data=SaleResponse.model_validate(sale))

@router.get("", response_model=SuccessResponse[PaginatedData[SaleResponse]])
async def get_sales(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    sales, total = await SaleService.get_sales(db, page, size, start_date, end_date)
    data = PaginatedData(
        data=[SaleResponse.model_validate(s) for s in sales],
        pagination=Pagination(page=page, size=size, total=total)
    )
    return SuccessResponse(data=data)

@router.get("/{sale_id}", response_model=SuccessResponse[SaleResponse])
async def get_sale(sale_id: UUID, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.get_sale(db, sale_id)
    return SuccessResponse(data=SaleResponse.model_validate(sale))

@router.delete("/{sale_id}", response_model=SuccessResponse[dict])
async def delete_sale(sale_id: UUID, db: AsyncSession = Depends(get_db)):
    await SaleService.delete_sale(db, sale_id)
    return SuccessResponse(message="Sale deleted successfully", data={})
