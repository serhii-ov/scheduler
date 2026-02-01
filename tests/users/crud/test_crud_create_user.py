import uuid
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.crud import create_user
from app.users.models import User
from app.users.roles import UserRole


@pytest.mark.asyncio
async def test_create_user_persisted(db: AsyncSession):

    phone_number = f"+38050{uuid.uuid4().int % 10**7:07}"

    user = await create_user(
        db,
        name="Test User",
        phone_number=phone_number,
        email="test@example.com",
        role=UserRole.ELECTRICIAN,
        is_active=True,
        hashed_password="hashed-password",
    )

    # flush() guarantees id exists
    assert user.id is not None

    # verify persisted
    result = await db.execute(
        select(User).where(User.id == user.id)
    )
    db_user = result.scalar_one()

    assert db_user.name == "Test User"
    assert db_user.phone_number == phone_number
    assert db_user.email == "test@example.com"
    assert db_user.role == UserRole.ELECTRICIAN
    assert db_user.is_active is True
    assert db_user.hashed_password == "hashed-password"
