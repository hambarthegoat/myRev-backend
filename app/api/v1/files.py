from typing import Optional
from fastapi import APIRouter, Depends, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.services.sale_service import SaleService

router = APIRouter()

EXPORT_MEDIA_TYPES = {
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
}


@router.post("/import")
async def import_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    count = await SaleService.bulk_import(db, content, file.filename or "")
    return {"imported": count}


@router.get("/export")
async def export_file(
    format: str = Query("xlsx", pattern="^(xlsx|csv)$"),
    bulan: Optional[int] = Query(None),
    kategori: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    content = await SaleService.export_sales(db, fmt=format, bulan=bulan, kategori=kategori)
    filename = f"sales_export.{format}"
    return StreamingResponse(
        iter([content]),
        media_type=EXPORT_MEDIA_TYPES[format],
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
