# src/config/dependencies.py
"""
Composition root: wires Application + Infrastructure using FastAPI's DI.
This is the only place that knows about concrete implementations (e.g. SQLAlchemyTaskRepository).
"""
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.db.task_repository import SQLAlchemyTaskRepository
from ..application.interfaces.task_repository import ITaskRepository
from ..application.use_cases.create_task import CreateTaskUseCase
from ..application.use_cases.get_tasks import GetTasksUseCase

_async_session_factory = None


def init_db(session_factory) -> None:
    """Called from app factory to inject the DB session factory."""
    global _async_session_factory
    _async_session_factory = session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields a DB session per request."""
    async with _async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_task_repository(session: AsyncSession = Depends(get_db)) -> ITaskRepository:
    """Provide task repository (implementation from Infrastructure)."""
    return SQLAlchemyTaskRepository(session)


def get_create_task_use_case(
    task_repository: ITaskRepository = Depends(get_task_repository),
) -> CreateTaskUseCase:
    """Provide CreateTaskUseCase (Application layer)."""
    return CreateTaskUseCase(task_repository=task_repository)


def get_get_tasks_use_case(
    task_repository: ITaskRepository = Depends(get_task_repository),
) -> GetTasksUseCase:
    """Provide GetTasksUseCase (Application layer)."""
    return GetTasksUseCase(task_repository=task_repository)


def get_current_user() -> int:
    """Stub: return current user id. Replace with real auth (JWT, etc.) in production."""
    return 1
