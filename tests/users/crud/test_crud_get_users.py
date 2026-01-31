import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.users.crud import get_users
from app.users.models import User
from app.users.roles import UserRole


pytestmark = pytest.mark.asyncio


async def test_get_users_empty(db: AsyncSession):
    await db.execute(delete(User))
    await db.commit()
    
    users = await get_users(db)

    assert users == []


async def test_get_users_limit(
    db: AsyncSession,
    user_factory,
):
    for i in range(5):
        await user_factory(
            phone_number=f"+38050100000{i+2}",
            role=UserRole.ELECTRICIAN,
        )

    users = await get_users(db, limit=2)

    assert len(users) == 2
    assert users[0].phone_number == "+380501000002"
    assert users[1].phone_number == "+380501000003"
    

async def test_get_users_skip(
    db: AsyncSession,
    user_factory,
):
    users_created = []
    for i in range(5):
        user = await user_factory(
            phone_number=f"+38050200000{i}",
            role=UserRole.ADMIN,
        )
        users_created.append(user)

    users = await get_users(db, skip=2)

    assert len(users) == 3
    assert users[0].id == users_created[2].id



@pytest.mark.asyncio
async def test_get_users_skip(
    db: AsyncSession,
    user_factory,
):
    
    await db.execute(delete(User))
    db.commit()

    users_created = []
    for i in range(5):
        user = await user_factory(
            phone_number=f"+38050200000{i}",
            role=UserRole.ADMIN,
        )
        users_created.append(user)

    users = await get_users(db, skip=2)

    assert len(users) == 3
    assert users[0].id == users_created[2].id



