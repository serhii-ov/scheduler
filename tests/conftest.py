import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
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
from tests.factories.user import create_user
from tests.utils.auth import get_auth_headers


TEST_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture(scope="session")
async def engine():
    """Create engine(session-scoped)"""
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
    """Create session maker to rollback after each test"""
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
async def db(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
            

@pytest.fixture(autouse=True)
def override_get_db(db: AsyncSession):
    """Override get_db dependency to use the same session for all tests."""
    async def _override():
        yield db

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_factory(db):
    async def _factory(**kwargs):
        return await create_user(db, **kwargs)
    return _factory


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


@pytest.fixture
async def user_headers(async_client, user):
    
    return await get_auth_headers(
        async_client,
        user.phone_number,
        "password",
    )


@pytest.fixture
async def admin_headers(async_client, admin):
    from tests.utils.auth import get_auth_headers
    return await get_auth_headers(
        async_client,
        admin.phone_number,
        "password",
    )
