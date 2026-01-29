"""
What you can add next (recommended)

Unique validation before insert
Email OR phone validation at schema level
Authentication (JWT)
Role-based permissions
Soft-delete only (audit-friendly)


"""

from fastapi import (
    APIRouter, Depends, HTTPException, status, Query,
    )
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from app.users import crud
from app.users.schemas import (
    UserCreate, UserRead, UserUpdate, Token,
    )
from app.core.dependencies import get_db
from app.core.security import (
    create_access_token,
    )
from app.users.models import User
from app.users import service
from app.api.v1.deps import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


# @router.post("/", response_model=UserRead)
# async def create_user(
#         user_in: UserCreate,
#         db: AsyncSession = Depends(get_db),
#     ):
#     return await service.create_user(db, user_in)
# @router.post("/", response_model=UserRead)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        user = await service.create_user(db, user_in)

    return user



@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
    """
    OAuth2 login.

    Use:
    - username = phone number
    - password = plain password
    """

    user = await crud.authenticate_user(
        db,
        phone_number=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token}


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    target_user = await crud.get_user_by_id(db, user_id)

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return await service.read_user(
        db=db,
        target_user=target_user,
        current_user=current_user,
    )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    ):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found",
            )

    return await service.update_user(db, user, user_in)


@router.delete("/{user_id}")
async def delete_user_endpoint(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    target_user = await crud.get_user_by_id(db, user_id)

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    await service.delete_user(
        db=db,
        target_user=target_user,
        current_user=current_user,
    )
    return {"status": "user deleted"}


@router.get("/", response_model=List[UserRead])
async def list_users_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    users = await service.list_users(
        db=db,
        current_user=current_user,
        skip=skip,
        limit=limit,
    )
    return users


@router.get("/me")
async def read_me(
        current_user: User = Depends(get_current_user),
    ):
    return current_user
