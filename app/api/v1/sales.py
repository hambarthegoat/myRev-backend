from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.sale import SaleCreate, SaleUpdate, SaleResponse
from app.services.sale_service import SaleService

router = APIRouter()


@router.get("/analytics")
async def get_analytics(
    tahun: int = Query(...),
    bulan: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await SaleService.get_analytics(db, tahun=tahun, bulan=bulan)


@router.post("", response_model=SaleResponse)
async def create_sale(sale_in: SaleCreate, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.create_sale(db, sale_in)
    return SaleResponse.model_validate(sale)


@router.get("", response_model=List[SaleResponse])
async def get_sales(
    bulan: Optional[int] = Query(None),
    kategori: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    sales = await SaleService.get_sales(db, bulan=bulan, kategori=kategori, limit=limit)
    return [SaleResponse.model_validate(s) for s in sales]


@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(sale_id: int, sale_in: SaleUpdate, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.update_sale(db, sale_id, sale_in)
    return SaleResponse.model_validate(sale)


@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    await SaleService.delete_sale(db, sale_id)
    return {"success": True}
