from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Date
from app.models.base import Base


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tanggal = Column(Date, nullable=False)
    bulan = Column(Integer, nullable=False)
    nama_item = Column(String(255), nullable=False)
    kategori = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    harga_satuan = Column(Integer, nullable=False)
    total_harga = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=get_utc_now)
