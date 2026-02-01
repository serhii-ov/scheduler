import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.users.service import update_user
from app.users.schemas import UserUpdate
from app.users.models import User
from app.users.roles import UserRole
from app.users.exceptions import PermissionDenied


pytestmark=pytest.mark.asyncio


async def test_update_user_owner_can_update_self(
    db: AsyncSession,
    user_factory,
):
    user = await user_factory(role=UserRole.ELECTRICIAN)
    user_in = UserUpdate(name="Updated Name")

    updated = await update_user(
        db=db,
        target_user=user,
        current_user=user,
        user_in=user_in,
    )

    assert updated.id == user.id
    assert updated.name == "Updated Name"


async def test_update_user_admin_can_update_others(
    db: AsyncSession,
    user_factory,
):
    admin = await user_factory(role=UserRole.ADMIN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    user_in = UserUpdate(is_active=False)

    updated = await update_user(
        db=db,
        target_user=target,
        current_user=admin,
        user_in=user_in,
    )

    assert updated.is_active is False


async def test_update_user_engineer_can_update_others(
    db: AsyncSession,
    user_factory,
):
    engineer = await user_factory(role=UserRole.ENGINEER)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    user_in = UserUpdate(name="Engineer Updated")

    updated = await update_user(
        db=db,
        target_user=target,
        current_user=engineer,
        user_in=user_in,
    )

    assert updated.name == "Engineer Updated"


async def test_update_user_electrician_cannot_update_others(
    db: AsyncSession,
    user_factory,
):
    electrician = await user_factory(role=UserRole.ELECTRICIAN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    user_in = UserUpdate(name="Should Not Work")

    with pytest.raises(PermissionDenied):
        await update_user(
            db=db,
            target_user=target,
            current_user=electrician,
            user_in=user_in,
        )
