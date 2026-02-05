from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_db
from app.users import crud
from app.users.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/users/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
    ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_id(db, user_id=int(user_id))
    if not user or not user.is_active:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
    ) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


# def require_roles(*allowed_roles: UserRole):
#     async def role_checker(
#         current_user: User = Depends(get_current_user),
#     ) -> User:
#         if current_user.role not in allowed_roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Not enough permissions",
#             )
#         return current_user

#     return role_checker


