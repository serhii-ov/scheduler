import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.roles import UserRole
from app.users.service import delete_user
from app.users.exceptions import PermissionDenied
from app.users.crud import get_user_by_id


pytestmark=pytest.mark.asyncio


async def test_delete_user_owner_can_delete_self(
    db: AsyncSession,
    user_factory,
):
    user = await user_factory(role=UserRole.ELECTRICIAN)

    await delete_user(
        db=db,
        target_user=user,
        current_user=user,
    )

    deleted = await get_user_by_id(db, user.id)
    assert deleted is None


async def test_delete_user_admin_can_delete_others(
    db: AsyncSession,
    user_factory,
):
    admin = await user_factory(role=UserRole.ADMIN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    await delete_user(
        db=db,
        target_user=target,
        current_user=admin,
    )

    deleted = await get_user_by_id(db, target.id)
    assert deleted is None


async def test_delete_user_electrician_cannot_delete_others(
    db: AsyncSession,
    user_factory,
):
    electrician = await user_factory(role=UserRole.ELECTRICIAN)
    target = await user_factory(role=UserRole.ELECTRICIAN)

    with pytest.raises(PermissionDenied):
        await delete_user(
            db=db,
            target_user=target,
            current_user=electrician,
        )

    still_exists = await get_user_by_id(db, target.id)
    assert still_exists is not None
