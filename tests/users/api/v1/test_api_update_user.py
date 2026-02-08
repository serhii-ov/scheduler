import pytest
from httpx import AsyncClient


pytestmark=pytest.mark.asyncio


async def test_update_user_success(
    async_client: AsyncClient,
    db,
    user_factory,
):

    user = await user_factory(
        name="Old Name",
        email="old@example.com",
       
    )

    payload = {
        "name": "New Name",
    }

    response = await async_client.patch(
        f"/users/{user.id}",
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == user.id
    assert data["name"] == "New Name"
    assert data["email"] == "old@example.com"
