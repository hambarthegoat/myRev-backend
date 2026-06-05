from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.sale import Sale
from app.schemas.sale import SaleCreate
from app.services.item_service import ItemService

class SaleService:
    @staticmethod
    async def create_sale(db: AsyncSession, sale_in: SaleCreate) -> Sale:
        item = await ItemService.get_item(db, sale_in.item_id)
        
        unit_price = item.price
        total_price = unit_price * sale_in.quantity
        
        sale = Sale(
            item_id=sale_in.item_id,
            quantity=sale_in.quantity,
            unit_price=unit_price,
            total_price=total_price,
            sale_date=sale_in.sale_date
        )
        db.add(sale)
        await db.commit()
        await db.refresh(sale)
        return sale

    @staticmethod
    async def get_sales(
        db: AsyncSession, 
        page: int, 
        size: int, 
        start_date: Optional[date] = None, 
        end_date: Optional[date] = None
    ) -> tuple[list[Sale], int]:
        query = select(Sale)
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
            
        total_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar() or 0
        
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        result = await db.execute(query)
        sales = result.scalars().all()
        
        return list(sales), total

    @staticmethod
    async def get_sale(db: AsyncSession, sale_id: UUID) -> Sale:
        result = await db.execute(select(Sale).filter(Sale.id == sale_id))
        sale = result.scalars().first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return sale

    @staticmethod
    async def delete_sale(db: AsyncSession, sale_id: UUID) -> None:
        sale = await SaleService.get_sale(db, sale_id)
        await db.delete(sale)
        await db.commit()
