import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.crud import authenticate_user
from app.users.roles import UserRole
from app.core.security import get_password_hash


pytestmark = pytest.mark.asyncio


async def test_authenticate_user_success(
    db: AsyncSession,
    user_factory,
):
    password = "super-secret"

    user = await user_factory(
        phone_number="+380502222222",
        hashed_password=get_password_hash(password),
        role=UserRole.ADMIN,
    )

    authenticated = await authenticate_user(
        db,
        phone_number=user.phone_number,
        password=password,
    )

    assert authenticated is not None
    assert authenticated.id == user.id
    assert authenticated.phone_number == user.phone_number


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(
    db: AsyncSession,
    user_factory,
):
    password = "correct-password"

    user = await user_factory(
        phone_number="+380501111111",
        hashed_password=get_password_hash(password),
        role=UserRole.ELECTRICIAN,
    )

    authenticated = await authenticate_user(
        db,
        phone_number=user.phone_number,
        password="wrong-password",
    )

    assert authenticated is None
 

@pytest.mark.asyncio
async def test_authenticate_user_nonexistent_phone(db: AsyncSession):
    user = await authenticate_user(
        db,
        phone_number="+380500000000",
        password="whatever",
    )

    assert user is None
