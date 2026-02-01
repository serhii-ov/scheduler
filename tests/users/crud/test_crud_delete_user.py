import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.users.models import User
from app.users.crud import delete_user


@pytest.mark.asyncio
async def test_delete_user(db: AsyncSession, user_factory):
    # Create a user in the DB

    phone_number = f"+38050{uuid.uuid4().int % 10**7:07}"

    user = await user_factory(
        phone_number=phone_number,
        role="electrician"
    )
    
    # Make sure the user exists
    result = await db.execute(select(User).where(User.id == user.id))
    assert result.scalar_one_or_none() is not None

    # Delete the user
    await delete_user(db, user=user)
    await db.commit()

    # Verify the user is gone
    result = await db.execute(select(User).where(User.id == user.id))
    assert result.scalar_one_or_none() is None
