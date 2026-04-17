# src/app.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from sqlalchemy import select

from .config.dependencies import init_db
from .infrastructure.db.models import Base, UserModel
from .presentation.api.task_controller import router as tasks_router
from .presentation.api.error_handlers import setup_error_handlers

# SQLite for demo
DATABASE_URL = "sqlite+aiosqlite:///./task_manager.db"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup."""
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed default user (id=1) for demo so tasks can reference it
    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    init_db(session_factory)
    async with session_factory() as session:
        result = await session.execute(select(UserModel).limit(1))
        if result.scalar_one_or_none() is None:
            session.add(UserModel(email="demo@example.com"))
            await session.commit()
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Manager API",
        description="Sample production-ready Clean Architecture with FastAPI",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(tasks_router)
    setup_error_handlers(app)
    return app


app = create_app()
