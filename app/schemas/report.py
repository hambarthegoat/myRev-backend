from typing import List
from pydantic import BaseModel

class DailyReportResponse(BaseModel):
    date: str
    total_transactions: int
    total_quantity: int
    total_revenue: float

class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    total_transactions: int
    total_quantity: int
    total_revenue: float

class TopItem(BaseModel):
    item_name: str
    quantity_sold: int

class BestSellingResponse(BaseModel):
    data: List[TopItem]
