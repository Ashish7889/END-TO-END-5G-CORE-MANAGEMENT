from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings
from .models_base import Base

settings = get_settings()

async_engine = create_async_engine(
    settings.database_url_async,
    echo=False,
)
async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

sync_engine = None
sync_session_factory: sessionmaker[Session] | None = None


def get_sync_engine():
    global sync_engine
    if sync_engine is None:
        from sqlalchemy import create_engine

        connect_args = {"check_same_thread": False} if settings.database_url_sync.startswith("sqlite") else {}
        sync_engine = create_engine(settings.database_url_sync, echo=False, connect_args=connect_args)
    return sync_engine


def get_sync_session() -> Session:
    global sync_session_factory
    engine = get_sync_engine()
    if sync_session_factory is None:
        sync_session_factory = sessionmaker(bind=engine)
    return sync_session_factory()


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
