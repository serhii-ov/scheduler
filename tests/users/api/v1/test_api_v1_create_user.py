import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.users.models import User
from app.main import app


pytestmark=pytest.mark.asyncio


async def test_create_user_success(async_client: AsyncClient, db):
    payload = {
        "name": "John Doe",
        "phone_number": "+380501234567",
        "email": "john@example.com",
        "password": "secret123",
    }

    response = await async_client.post("/api/users/", json=payload)

    resp = await async_client.get("/openapi.json")
    paths = resp.json()["paths"].keys()
    print(paths)


    assert response.status_code == 200

    data = response.json()
    assert data["phone_number"] == "+380501234567"
    assert data["email"] == "john@example.com"
    assert "id" in data
    assert "password" not in data  # response_model works ✅

    # 🔍 verify DB commit really happened
    result = await db.execute(
        select(User).where(User.phone_number == "+380501234567")
    )
    user = result.scalar_one()

    assert user.name == "John Doe"


async def test_create_user_duplicate_phone(async_client: AsyncClient):
    payload = {
        "name": "John",
        "phone_number": "+380501111111",
        "email": "john1@example.com",
        "password": "secret123",
        "role": "ADMIN",
        "is_active": True,
    }

    await async_client.post("/users/", json=payload)

    response = await async_client.post("/users/", json=payload)

    assert response.status_code == 404
