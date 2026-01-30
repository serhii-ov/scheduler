import pytest
from app.users.crud import get_user_by_phone


pytestmark = pytest.mark.asyncio


async def test_get_user_by_id_found(db, user_factory):
    user = await user_factory(
        name="Jack",
        phone_number="+380501234567",
    )

    result = await get_user_by_phone(db, user.phone_number)

    assert result is not None
    assert result.phone_number == user.phone_number
    

async def test_get_user_by_id_not_found(db):
    result = await get_user_by_phone(db, "+380509999999")  

    assert result is None
