import uuid

from typing import Any
from app.users.models import User


DEFAULT_PASSWORD_HASH = "hashed_password"


def unique_email():
    return f"user-{uuid.uuid4()}@example.com"


async def create_user(
    db,
    **overrides: Any,
) -> User:
    """
    Async factory for User model.
    """

    data = {
        "name": "Test User",
        "phone_number": f"+38050{uuid.uuid4().int % 10**7:07}",
        "email": unique_email(),
        "role": "electrician",
        "is_active": True,
        "hashed_password": DEFAULT_PASSWORD_HASH,
    }

    data.update(overrides)

    user = User(**data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
