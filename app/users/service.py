from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.phone_normalizer import normalize_phone
from app.core.security import get_password_hash
from app.users.exceptions import UserAlreadyExistsError
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate
from app.users.authorization import (
    require_owner_or_permission,
    has_permission,
)
from app.users.permissions import Permission
from app.users import crud


async def create_user(
        db: AsyncSession,
        user_in: UserCreate,
    ) -> User:

    normalized_phone = normalize_phone(user_in.phone_number)
    hashed_password = get_password_hash(user_in.password)

    try:
        user = await crud.create_user(
            db,
            name=user_in.name,
            phone_number=normalized_phone,
            email=user_in.email,
            role=user_in.role,
            is_active=user_in.is_active,
            hashed_password=hashed_password,
        )
    except IntegrityError:
        raise UserAlreadyExistsError(
            "User with this phone number already exists"
        )

    return user



async def read_user(
        *,
        db: AsyncSession,
        target_user: User,
        current_user: User,
    ) -> User:
    """
    ✔ Owner can read themselves
    ✔ Admin / Engineer can read others
    ✔ Electrician only reads self
    """
    require_owner_or_permission(
        current_user=current_user,
        target_user=target_user,
        permission=Permission.USER_READ,
    )

    return target_user


async def update_user(
        db: AsyncSession,
        *,
        target_user: User,
        current_user: User,
        user_in: UserUpdate,
    ) -> User:
    """
    ✔ Owner can update themselves
    ✔ Admin / Engineer can update others
    ✔ Electrician only updates self
    """
    require_owner_or_permission(
        current_user=current_user,
        target_user=target_user,
        permission=Permission.USER_UPDATE,
    )

    try:
        await crud.update_user(
            user=target_user,
            user_in=user_in,
        )

        await db.commit()
        await db.refresh(target_user)
        return target_user

    except IntegrityError:
        await db.rollback()
        raise


async def delete_user(
        db: AsyncSession,
        *,
        target_user: User,
        current_user: User,
    ) -> None:
    
    require_owner_or_permission(
        current_user=current_user,
        target_user=target_user,
        permission=Permission.USER_DELETE,
    )

    await crud.delete_user(
            db=db,
            user=target_user,
        )
        


async def list_users(
        db: AsyncSession,
        current_user: User,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:
    """
    List users with RBAC:
    - Admin / other roles with USER_LIST permission can see all users
    - Others can only see themselves
    """
    if has_permission(current_user, Permission.USER_LIST):
        return await crud.get_users(db, skip=skip, limit=limit)
    else:
        # Regular users see only themselves
        return [current_user]
