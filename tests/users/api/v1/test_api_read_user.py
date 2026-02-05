import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.users.models import User
from app.users.roles import UserRole
from app.core.security import get_password_hash

from tests.utils.auth import get_auth_headers
from tests.factories.user import create_user, DEFAULT_PASSWORD


pytestmark = pytest.mark.asyncio


async def test_read_user_success(async_client, db):
    user = await create_user(
        db,
        phone_number="+380501234567",
        hashed_password=get_password_hash(DEFAULT_PASSWORD),
    )

    headers = await get_auth_headers(
        async_client,
        phone_number=user.phone_number,
        password=DEFAULT_PASSWORD,
    )

    response = await async_client.get(
        f"/api/users/{user.id}",
        headers=headers,
    )

    assert response.status_code == 200


async def test_read_user_self(
    async_client: AsyncClient,
    db: AsyncSession,
):
    user = await create_user(
        db,
        phone_number="+380503333333",
        hashed_password=get_password_hash(DEFAULT_PASSWORD),
    )

    headers = await get_auth_headers(
        async_client,
        phone_number=user.phone_number,
        password=DEFAULT_PASSWORD,
    )

    response = await async_client.get(
        f"/api/users/{user.id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


async def test_read_user_forbidden(
    async_client: AsyncClient,
    db: AsyncSession,
):
    user = await create_user(
        db,
        phone_number="+380504444444",
        hashed_password=get_password_hash(DEFAULT_PASSWORD),
        role=UserRole.ELECTRICIAN,
    )

    other_user = await create_user(db)

    headers = await get_auth_headers(
        async_client,
        phone_number=user.phone_number,
        password=DEFAULT_PASSWORD,
    )

    response = await async_client.get(
        f"/api/users/{other_user.id}",
        headers=headers,
    )

    assert response.status_code == 403


async def test_read_user_not_found(
    async_client: AsyncClient,
    db: AsyncSession,
):
    admin = await create_user(
        db,
        role=UserRole.ADMIN,
        hashed_password=get_password_hash(DEFAULT_PASSWORD),
    )

    headers = await get_auth_headers(
        async_client,
        phone_number=admin.phone_number,
        password=DEFAULT_PASSWORD,
    )

    response = await async_client.get(
        "/api/users/999999",
        headers=headers,
    )

    assert response.status_code == 404
