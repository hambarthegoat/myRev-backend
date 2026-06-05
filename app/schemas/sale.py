from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field

class SaleCreate(BaseModel):
    item_id: UUID
    quantity: int = Field(..., gt=0)
    sale_date: date

class SaleResponse(BaseModel):
    id: UUID
    item_id: UUID
    quantity: int
    unit_price: float
    total_price: float
    sale_date: date

    model_config = {"from_attributes": True}
