from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class Pagination(BaseModel):
    page: int
    size: int
    total: int

class PaginatedData(BaseModel, Generic[T]):
    data: List[T]
    pagination: Pagination
