import pytest
from app.users.crud import get_user_by_id


pytestmark = pytest.mark.asyncio


async def test_get_user_by_id_found(db, user_factory):
    user = await user_factory(
        name="Jack",
        phone_number="+380501234567",
    )

    result = await get_user_by_id(db, user.id)

    assert result is not None
    assert result.id == user.id
    

async def test_get_user_by_id_not_found(db):
    result = await get_user_by_id(db, 9999)  

    assert result is None


async def test_admin_user(user_factory):
    admin = await user_factory(role="admin", is_active=False)

    assert admin.role == "admin"
    assert not admin.is_active
