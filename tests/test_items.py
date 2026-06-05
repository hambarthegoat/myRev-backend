import pytest
from httpx import AsyncClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post(
        f"{settings.API_V1_STR}/items",
        json={"name": "Pensil 2B", "sku": "PEN001", "price": 3000.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Pensil 2B"
    assert data["data"]["sku"] == "PEN001"
    assert "id" in data["data"]

@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    await client.post(
        f"{settings.API_V1_STR}/items",
        json={"name": "Buku Tulis", "sku": "BUK001", "price": 5000.0}
    )
    
    response = await client.get(f"{settings.API_V1_STR}/items")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["data"]) >= 1
    assert data["data"]["pagination"]["total"] >= 1
