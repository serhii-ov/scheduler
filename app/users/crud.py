"""
✔ Service controls transaction boundaries
(no commits/rollbacks in CRUD)
✔ Rollback is centralized
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate
from app.users.roles import UserRole
from app.core.security import (
                                verify_password, 
                            )


async def create_user(
    db: AsyncSession,
    *,
    name: str,
    phone_number: str,
    email: str | None,
    role: UserRole,
    is_active: bool,
    hashed_password: str,
) -> User:
    user = User(
        name=name,
        phone_number=phone_number,
        email=email,
        role=role,
        is_active=is_active,
        hashed_password=hashed_password,
    )

    db.add(user)
    await db.flush()  # ensures user.id exists

    return user



async def get_user_by_phone(
        db: AsyncSession,
        phone_number: str,
    ) -> User | None:
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()


async def authenticate_user(
        db: AsyncSession,
        phone_number: str,
        password: str,
    ) -> User | None:
    user = await get_user_by_phone(db, phone_number)
    if not user:
        return None
    if not verify_password(
            password, user.hashed_password,
        ):
        return None
    return user


async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_users(
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:
    result = await db.execute(
        select(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def update_user(
        *,
        user: User,
        user_in: UserUpdate,
    ) -> User:
    data = user_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(user, field, value)

    return user


async def delete_user(
        db: AsyncSession,
        *,
        user: User,
    ) -> None:
    
    await db.delete(user)
