# src/config/dependencies.py
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.db.task_repository import SQLAlchemyTaskRepository
from ..application.interfaces.task_repository import ITaskRepository
from ..application.use_cases.create_task import CreateTaskUseCase
from ..application.use_cases.get_tasks import GetTasksUseCase
from ..application.use_cases.update_task import UpdateTaskUseCase

_async_session_factory = None


def init_db(session_factory) -> None:
    global _async_session_factory
    _async_session_factory = session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_task_repository(session: AsyncSession = Depends(get_db)) -> ITaskRepository:
    return SQLAlchemyTaskRepository(session)


def get_create_task_use_case(
    task_repository: ITaskRepository = Depends(get_task_repository),
) -> CreateTaskUseCase:
    return CreateTaskUseCase(task_repository=task_repository)


def get_get_tasks_use_case(
    task_repository: ITaskRepository = Depends(get_task_repository),
) -> GetTasksUseCase:
    return GetTasksUseCase(task_repository=task_repository)


def get_update_task_use_case(
    task_repository: ITaskRepository = Depends(get_task_repository),
) -> UpdateTaskUseCase:
    return UpdateTaskUseCase(task_repository=task_repository)


def get_current_user() -> int:
    return 1
