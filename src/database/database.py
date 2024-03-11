from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.model import Base

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        await self._engine.dispose()

    async def remove_database(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> SessionFactory:
        try:
            async with self._session_factory() as session:
                yield session
        except Exception as e:
            print(f"Session rollback because of exception {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
