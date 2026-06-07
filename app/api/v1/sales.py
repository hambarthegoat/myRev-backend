from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Response
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


@router.get("/categories", response_model=List[str])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await SaleService.get_categories(db)


@router.post("", response_model=SaleResponse)
async def create_sale(sale_in: SaleCreate, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.create_sale(db, sale_in)
    return SaleResponse.model_validate(sale)


@router.get("", response_model=List[SaleResponse])
async def get_sales(
    response: Response,
    bulan: Optional[int] = Query(None),
    kategori: Optional[str] = Query(None),
    tanggal_dari: Optional[date] = Query(None),
    tanggal_sampai: Optional[date] = Query(None),
    nama_item: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    sales, total = await SaleService.get_sales(
        db,
        bulan=bulan,
        kategori=kategori,
        tanggal_dari=tanggal_dari,
        tanggal_sampai=tanggal_sampai,
        nama_item=nama_item,
        limit=limit,
        page=page,
        page_size=page_size,
    )
    response.headers["X-Total-Count"] = str(total)
    if page is not None:
        size = page_size or 20
        response.headers["X-Page"] = str(page)
        response.headers["X-Page-Size"] = str(size)
        response.headers["X-Total-Pages"] = str((total + size - 1) // size if size else 0)
    return [SaleResponse.model_validate(s) for s in sales]


@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(sale_id: int, sale_in: SaleUpdate, db: AsyncSession = Depends(get_db)):
    sale = await SaleService.update_sale(db, sale_id, sale_in)
    return SaleResponse.model_validate(sale)


@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    await SaleService.delete_sale(db, sale_id)
    return {"success": True}
