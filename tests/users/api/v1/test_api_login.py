import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.users.models import User
from tests.factories.user import create_user, DEFAULT_PASSWORD


pytestmark = pytest.mark.asyncio


async def test_login_success(
    async_client: AsyncClient,
    db: AsyncSession,
):
    plain_password = DEFAULT_PASSWORD

    user: User = await create_user(
        db,
        phone_number=f"+38050{uuid.uuid4().int % 10**7:07}",
        hashed_password=get_password_hash(DEFAULT_PASSWORD),  
    )

    assert verify_password(plain_password, user.hashed_password)

    response = await async_client.post(
        "/api/users/login",
        data={
            "username": user.phone_number,
            "password": plain_password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["access_token"]


async def test_login_invalid_password(
    async_client: AsyncClient,
    db: AsyncSession,
):
    plain_password = "wrong_password"

    user: User = await create_user(
        db,
        phone_number="+380501234777",
        hashed_password=get_password_hash(DEFAULT_PASSWORD),  
    )

    response = await async_client.post(
        "/api/users/login",
        data={
            "username": user.phone_number,
            "password": get_password_hash("wrong-password"),
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
