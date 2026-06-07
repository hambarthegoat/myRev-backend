from datetime import date
from typing import List
from pydantic import BaseModel, Field


class SaleCreate(BaseModel):
    tanggal: date
    bulan: int = Field(..., ge=1, le=12)
    nama_item: str
    kategori: str
    quantity: int = Field(..., ge=1)
    harga_satuan: int = Field(..., gt=0)


class SaleUpdate(BaseModel):
    tanggal: date
    bulan: int = Field(..., ge=1, le=12)
    nama_item: str
    kategori: str
    quantity: int = Field(..., ge=1)
    harga_satuan: int = Field(..., gt=0)


class SaleResponse(BaseModel):
    id: int
    tanggal: date
    bulan: int
    nama_item: str
    kategori: str
    quantity: int
    harga_satuan: int
    total_harga: int

    model_config = {"from_attributes": True}


class KategoriStat(BaseModel):
    kategori: str
    total_pendapatan: int


class TrendHarian(BaseModel):
    tanggal: str
    total_pendapatan: int


class TopItem(BaseModel):
    nama_item: str
    total_quantity: int


class AnalyticsResponse(BaseModel):
    total_transaksi: int
    total_pendapatan: int
    per_kategori: List[KategoriStat]
    trend_harian: List[TrendHarian]
    top_items: List[TopItem]


class BulkImportResponse(BaseModel):
    imported: int
