from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    @staticmethod
    async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
        result = await db.execute(select(Item).filter(Item.sku == item_in.sku))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="SKU already exists")
            
        item = Item(**item_in.model_dump())
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def get_items(db: AsyncSession, page: int, size: int) -> tuple[list[Item], int]:
        offset = (page - 1) * size
        result = await db.execute(select(Item).offset(offset).limit(size))
        items = result.scalars().all()
        
        total_result = await db.execute(select(func.count(Item.id)))
        total = total_result.scalar() or 0
        
        return list(items), total

    @staticmethod
    async def get_item(db: AsyncSession, item_id: UUID) -> Item:
        result = await db.execute(select(Item).filter(Item.id == item_id))
        item = result.scalars().first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @staticmethod
    async def update_item(db: AsyncSession, item_id: UUID, item_in: ItemUpdate) -> Item:
        item = await ItemService.get_item(db, item_id)
        
        for field, value in item_in.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
            
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_item(db: AsyncSession, item_id: UUID) -> None:
        item = await ItemService.get_item(db, item_id)
        await db.delete(item)
        await db.commit()
