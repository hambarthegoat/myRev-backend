import pytest
from httpx import AsyncClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_daily_report(client: AsyncClient):
    item_res = await client.post(
        f"{settings.API_V1_STR}/items",
        json={"name": "Penggaris", "sku": "PGR001", "price": 4000.0}
    )
    item_id = item_res.json()["data"]["id"]

    await client.post(
        f"{settings.API_V1_STR}/sales",
        json={"item_id": item_id, "quantity": 10, "sale_date": "2026-01-10"}
    )
    
    res = await client.get(f"{settings.API_V1_STR}/reports/daily?date=2026-01-10")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_transactions"] == 1
    assert data["total_quantity"] == 10
    assert data["total_revenue"] == 40000.0

@pytest.mark.asyncio
async def test_monthly_report(client: AsyncClient):
    item_res = await client.post(
        f"{settings.API_V1_STR}/items",
        json={"name": "Penggaris2", "sku": "PGR002", "price": 4000.0}
    )
    item_id = item_res.json()["data"]["id"]

    await client.post(
        f"{settings.API_V1_STR}/sales",
        json={"item_id": item_id, "quantity": 10, "sale_date": "2026-01-10"}
    )
    
    res = await client.get(f"{settings.API_V1_STR}/reports/monthly?year=2026&month=1")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_transactions"] == 1

@pytest.mark.asyncio
async def test_top_items(client: AsyncClient):
    res = await client.get(f"{settings.API_V1_STR}/reports/top-items")
    assert res.status_code == 200
    assert isinstance(res.json()["data"]["data"], list)
