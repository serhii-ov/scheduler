from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker,
    )
from .config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=30,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
