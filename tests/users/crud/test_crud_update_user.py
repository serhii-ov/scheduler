import pytest
from app.users.models import User
from app.users.schemas import UserUpdate
from app.users.crud import update_user
from app.users.models import UserRole


@pytest.mark.asyncio
async def test_update_user_updates_fields():
    # Create a mock user
    user = User(
        id=1,
        name="Old Name",
        phone_number="+380501111111",
        email="old@test.com",
        role=UserRole.ELECTRICIAN,
        is_active=True,
        hashed_password="old_hash"
    )

    # Fields to update
    user_in = UserUpdate(
        name="New Name",
        email="new@test.com",
        is_active=False
    )

    # Perform update
    updated_user = await update_user(user=user, user_in=user_in)

    # Assert that only provided fields changed
    assert updated_user.name == "New Name"
    assert updated_user.email == "new@test.com"
    assert updated_user.is_active is False

    # Assert that untouched fields remain the same
    assert updated_user.phone_number == "+380501111111"
    assert updated_user.role == UserRole.ELECTRICIAN
    assert updated_user.hashed_password == "old_hash"
