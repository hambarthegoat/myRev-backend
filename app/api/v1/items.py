from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.base import SuccessResponse
from app.utils.pagination import PaginatedData, Pagination
from app.services.item_service import ItemService

router = APIRouter()

@router.post("", response_model=SuccessResponse[ItemResponse])
async def create_item(item_in: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = await ItemService.create_item(db, item_in)
    return SuccessResponse(data=ItemResponse.model_validate(item))

@router.get("", response_model=SuccessResponse[PaginatedData[ItemResponse]])
async def get_items(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    items, total = await ItemService.get_items(db, page, size)
    data = PaginatedData(
        data=[ItemResponse.model_validate(i) for i in items],
        pagination=Pagination(page=page, size=size, total=total)
    )
    return SuccessResponse(data=data)

@router.get("/{item_id}", response_model=SuccessResponse[ItemResponse])
async def get_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    item = await ItemService.get_item(db, item_id)
    return SuccessResponse(data=ItemResponse.model_validate(item))

@router.put("/{item_id}", response_model=SuccessResponse[dict])
async def update_item(item_id: UUID, item_in: ItemUpdate, db: AsyncSession = Depends(get_db)):
    await ItemService.update_item(db, item_id, item_in)
    return SuccessResponse(message="Item updated successfully", data={})

@router.delete("/{item_id}", response_model=SuccessResponse[dict])
async def delete_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    await ItemService.delete_item(db, item_id)
    return SuccessResponse(message="Item deleted successfully", data={})
