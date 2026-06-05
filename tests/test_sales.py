import pytest
from httpx import AsyncClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_sale(client: AsyncClient):
    item_res = await client.post(
        f"{settings.API_V1_STR}/items",
        json={"name": "Penghapus", "sku": "PNG001", "price": 2000.0}
    )
    item_id = item_res.json()["data"]["id"]

    sale_res = await client.post(
        f"{settings.API_V1_STR}/sales",
        json={
            "item_id": item_id,
            "quantity": 5,
            "sale_date": "2026-06-05"
        }
    )
    assert sale_res.status_code == 200
    data = sale_res.json()
    assert data["success"] is True
    assert data["data"]["quantity"] == 5
    assert data["data"]["unit_price"] == 2000.0
    assert data["data"]["total_price"] == 10000.0

@pytest.mark.asyncio
async def test_get_sales(client: AsyncClient):
    res = await client.get(f"{settings.API_V1_STR}/sales")
    assert res.status_code == 200
    assert res.json()["success"] is True
