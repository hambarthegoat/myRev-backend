import io
from datetime import date
from typing import Optional
import pandas as pd
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import extract
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleUpdate


class SaleService:
    @staticmethod
    async def create_sale(db: AsyncSession, sale_in: SaleCreate) -> Sale:
        sale = Sale(
            tanggal=sale_in.tanggal,
            bulan=sale_in.bulan,
            nama_item=sale_in.nama_item,
            kategori=sale_in.kategori,
            quantity=sale_in.quantity,
            harga_satuan=sale_in.harga_satuan,
            total_harga=sale_in.harga_satuan * sale_in.quantity,
        )
        db.add(sale)
        await db.commit()
        await db.refresh(sale)
        return sale

    @staticmethod
    async def get_sales(
        db: AsyncSession,
        bulan: Optional[int] = None,
        kategori: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[Sale]:
        query = select(Sale)
        if bulan:
            query = query.where(Sale.bulan == bulan)
        if kategori:
            query = query.where(Sale.kategori == kategori)
        query = query.order_by(Sale.tanggal.desc(), Sale.id.desc())
        if limit:
            query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_sale(db: AsyncSession, sale_id: int) -> Sale:
        result = await db.execute(select(Sale).where(Sale.id == sale_id))
        sale = result.scalars().first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return sale

    @staticmethod
    async def update_sale(db: AsyncSession, sale_id: int, sale_in: SaleUpdate) -> Sale:
        sale = await SaleService.get_sale(db, sale_id)
        sale.tanggal = sale_in.tanggal
        sale.bulan = sale_in.bulan
        sale.nama_item = sale_in.nama_item
        sale.kategori = sale_in.kategori
        sale.quantity = sale_in.quantity
        sale.harga_satuan = sale_in.harga_satuan
        sale.total_harga = sale_in.harga_satuan * sale_in.quantity
        await db.commit()
        await db.refresh(sale)
        return sale

    @staticmethod
    async def delete_sale(db: AsyncSession, sale_id: int) -> None:
        sale = await SaleService.get_sale(db, sale_id)
        await db.delete(sale)
        await db.commit()

    @staticmethod
    async def get_analytics(
        db: AsyncSession, tahun: int, bulan: Optional[int] = None
    ) -> dict:
        query = select(Sale).where(extract("year", Sale.tanggal) == tahun)
        if bulan:
            query = query.where(Sale.bulan == bulan)
        result = await db.execute(query)
        sales = result.scalars().all()

        if not sales:
            return {
                "total_transaksi": 0,
                "total_pendapatan": 0,
                "per_kategori": [],
                "trend_harian": [],
                "top_items": [],
            }

        total_transaksi = len(sales)
        total_pendapatan = sum(s.total_harga for s in sales)

        kat_map: dict[str, int] = {}
        for s in sales:
            kat_map[s.kategori] = kat_map.get(s.kategori, 0) + s.total_harga
        per_kategori = [{"kategori": k, "total_pendapatan": v} for k, v in kat_map.items()]

        trend_map: dict[str, int] = {}
        for s in sales:
            k = str(s.tanggal)
            trend_map[k] = trend_map.get(k, 0) + s.total_harga
        trend_harian = [
            {"tanggal": k, "total_pendapatan": v}
            for k, v in sorted(trend_map.items())
        ]

        item_map: dict[str, int] = {}
        for s in sales:
            item_map[s.nama_item] = item_map.get(s.nama_item, 0) + s.quantity
        top_items = sorted(
            [{"nama_item": k, "total_quantity": v} for k, v in item_map.items()],
            key=lambda x: x["total_quantity"],
            reverse=True,
        )

        return {
            "total_transaksi": total_transaksi,
            "total_pendapatan": total_pendapatan,
            "per_kategori": per_kategori,
            "trend_harian": trend_harian,
            "top_items": top_items,
        }

    @staticmethod
    async def export_sales(
        db: AsyncSession,
        fmt: str = "xlsx",
        bulan: Optional[int] = None,
        kategori: Optional[str] = None,
    ) -> bytes:
        sales = await SaleService.get_sales(db, bulan=bulan, kategori=kategori)

        df = pd.DataFrame(
            [
                {
                    "tanggal": s.tanggal,
                    "bulan": s.bulan,
                    "nama_item": s.nama_item,
                    "kategori": s.kategori,
                    "quantity": s.quantity,
                    "harga_satuan": s.harga_satuan,
                    "total_harga": s.total_harga,
                }
                for s in sales
            ],
            columns=["tanggal", "bulan", "nama_item", "kategori", "quantity", "harga_satuan", "total_harga"],
        )

        if fmt == "csv":
            return df.to_csv(index=False).encode("utf-8")

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sales")
        return buffer.getvalue()

    @staticmethod
    async def bulk_import(
        db: AsyncSession, file_content: bytes, filename: str
    ) -> int:
        if filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            df = pd.read_csv(io.BytesIO(file_content))

        df.columns = df.columns.str.lower()

        required = {"tanggal", "bulan", "nama_item", "kategori", "quantity", "harga_satuan"}
        missing = required - set(df.columns)
        if missing:
            raise HTTPException(
                status_code=400, detail=f"Kolom tidak lengkap: {', '.join(sorted(missing))}"
            )

        count = 0
        for _, row in df.iterrows():
            raw_tanggal = row["tanggal"]
            if isinstance(raw_tanggal, date):
                tanggal = raw_tanggal
            else:
                tanggal = pd.to_datetime(raw_tanggal).date()

            qty = int(row["quantity"])
            harga = int(row["harga_satuan"])
            sale = Sale(
                tanggal=tanggal,
                bulan=int(row["bulan"]),
                nama_item=str(row["nama_item"]),
                kategori=str(row["kategori"]),
                quantity=qty,
                harga_satuan=harga,
                total_harga=qty * harga,
            )
            db.add(sale)
            count += 1

        await db.commit()
        return count
