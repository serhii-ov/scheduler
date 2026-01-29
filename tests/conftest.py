import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.base import Base
from app.core.dependencies import get_db
from app.core.security import get_password_hash as hash_password
from app.core.config import settings
from app.users.models import User
from app.users.roles import UserRole


# EVENT LOOP (required for pytest + asyncio on some platforms)
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


TEST_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="session")
async def async_session_maker(engine):
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


# DB SESSION (ROLLBACK AFTER EACH TEST)
@pytest.fixture
async def db(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.rollback()
            


# DEPENDENCY OVERRIDE
@pytest.fixture(autouse=True)
async def override_get_db(db: AsyncSession):
    async def _get_db_override():
        yield db

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


# HTTP CLIENT
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


# USERS
@pytest.fixture
async def user(db: AsyncSession) -> User:
    user = User(
        name="Test User",
        phone_number="+380501111111",
        email="user@test.com",
        hashed_password=hash_password("password"),
        role=UserRole.ELECTRICIAN,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    return user


@pytest.fixture
async def admin(db: AsyncSession) -> User:
    admin = User(
        name="Admin",
        phone_number="+380502222222",
        email="admin@test.com",
        hashed_password=hash_password("password"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(admin)
    await db.flush()
    return admin


# AUTH TOKENS
@pytest.fixture
async def user_token(client: AsyncClient, user: User) -> str:
    response = await client.post(
        "/api/v1/users/users/login",
        data={
            "username": user.phone_number,
            "password": "password",
        },
    )
    return response.json()["access_token"]


@pytest.fixture
async def admin_token(client: AsyncClient, admin: User) -> str:
    response = await client.post(
        "/api/v1/users/users/login",
        data={
            "username": admin.phone_number,
            "password": "password",
        },
    )
    return response.json()["access_token"]


# AUTH HEADERS
@pytest.fixture
def user_headers(user_token: str):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token: str):
    return {"Authorization": f"Bearer {admin_token}"}
