import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Date, Uuid
from sqlalchemy.orm import relationship
from app.models.base import Base

def get_utc_now():
    return datetime.now(timezone.utc)

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(Uuid(as_uuid=True), ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    sale_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=get_utc_now)

    item = relationship("Item")
