import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.service import read_user
from app.users.models import User
from app.users.permissions import Permission
from app.users.roles import UserRole
from app.users.exceptions import PermissionDenied


pytestmark = pytest.mark.asyncio


async def test_read_user_owner_can_read_self(db: AsyncSession, user_factory):
    user = await user_factory(role=UserRole.ELECTRICIAN)

    result = await read_user(
        db=db,
        target_user=user,
        current_user=user,
    )

    assert result.id == user.id


async def test_read_user_admin_can_read_others(db: AsyncSession, user_factory):
    admin = await user_factory(role=UserRole.ADMIN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    result = await read_user(
        db=db,
        target_user=target,
        current_user=admin,
    )

    assert result.id == target.id


async def test_read_user_admin_can_read_others(db: AsyncSession, user_factory):
    admin = await user_factory(role=UserRole.ADMIN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    result = await read_user(
        db=db,
        target_user=target,
        current_user=admin,
    )

    assert result.id == target.id

async def test_read_user_electrician_cannot_read_others(db: AsyncSession, user_factory):
    electrician = await user_factory(role=UserRole.ELECTRICIAN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    with pytest.raises(PermissionDenied):
        await read_user(
            db=db,
            target_user=target,
            current_user=electrician,
        )
        