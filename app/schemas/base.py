from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: T

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[Any] = None
