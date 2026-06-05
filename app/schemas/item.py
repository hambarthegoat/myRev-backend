from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., description="Name of the item")
    price: float = Field(..., gt=0, description="Price must be greater than 0")

class ItemCreate(ItemBase):
    sku: str = Field(..., description="Unique SKU code")

class ItemUpdate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: UUID
    sku: str
    created_at: datetime
    
    model_config = {"from_attributes": True}
