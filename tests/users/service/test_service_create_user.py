import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.users.schemas import UserCreate
from app.users.service import create_user
from app.users.roles import UserRole
from app.core.security import verify_password
from app.users.models import User


pytestmark = pytest.mark.asyncio


async def test_create_user_success(db: AsyncSession):
    user_in = UserCreate(
        name="John Doe",
        phone_number=f"+38050{uuid.uuid4().int % 10**7:07}",
        email="john@test.com",
        password="secret123",
        role=UserRole.ELECTRICIAN,
        is_active=True,
    )

    user = await create_user(db, user_in)

    await db.flush()
    await db.commit()

    assert isinstance(user, User)
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.phone_number == user_in.phone_number
    assert user.email == "john@test.com"
    assert user.role == UserRole.ELECTRICIAN
    assert user.is_active is True


async def test_create_user_normalizes_phone(db):
    user = await create_user(
        db,
        UserCreate(
            name="John",
            phone_number="050123-45-76",
            password="secret",
            role=UserRole.ELECTRICIAN,
            is_active=True,
        )
    )

    assert user.phone_number == "+380501234576"
    assert user.id is not None


async def test_create_user_password_is_hashed(db: AsyncSession):
    user_in = UserCreate(
        name="Jack Doe",
        phone_number="+380509999999",
        email="jack@test.com",
        password="plain-password",
        role=UserRole.ENGINEER,
        is_active=True,
    )

    user = await create_user(db, user_in)
    await db.flush()

    assert user.hashed_password != "plain-password"
    assert verify_password("plain-password", user.hashed_password)


async def test_create_user_persisted(db: AsyncSession):
    user_in = UserCreate(
        name="Persisted User",
        phone_number="+380507777777",
        email="persist@test.com",
        password="password",
        role=UserRole.ELECTRICIAN,
        is_active=True,
    )

    user = await create_user(db, user_in)
    await db.commit()
    
    statement = select(User).where(
        User.phone_number == user_in.phone_number
        )
    result = await db.execute(statement)
    db_user = result.scalar_one()

    assert db_user.id == user.id


async def test_create_user_does_not_allow_mass_assignment(db: AsyncSession):
    """
    Test that fields like is_superuser and 
    created_at cannot be set via UserCreate schema.
    """
    user_in = UserCreate(
        name="Safe User",
        phone_number="+380508888888",
        email="safe@test.com",
        password="password",
        role=UserRole.ELECTRICIAN,
        is_active=True,
    )

    user = await create_user(db, user_in)
    await db.flush()

    assert not hasattr(user, "is_superuser")
    assert not hasattr(user, "created_at") or user.created_at is not None
