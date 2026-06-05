import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, Uuid
from app.models.base import Base

def get_utc_now():
    return datetime.now(timezone.utc)

class Item(Base):
    __tablename__ = "items"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
