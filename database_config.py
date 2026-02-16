from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL= "postgresql+asyncpg://postgres:admin@localhost:5432/keells"

engine = create_async_engine(
    DATABASE_URL,
    echo=False, #Set true if you need to see sql statements by orm
    pool_pre_pinf=True, #verify the connection pool before using them
    future=True
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()