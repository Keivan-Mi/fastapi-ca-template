# src/infrastructure/db/task_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from ...application.dtos.task_dto import TaskFilterDTO
from ...application.interfaces.task_repository import ITaskRepository
from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus
from .models import TaskModel
from ..mappers.task_mapper import TaskMapper


class SQLAlchemyTaskRepository(ITaskRepository):
    """Concrete implementation using SQLAlchemy

    IMPLEMENTS the interface defined in Application layer.
    This is where DIP happens - Infrastructure depends on Application!
    """

    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper = TaskMapper()

    async def create(self, task: Task) -> Task:
        """Persist task to database"""
        # Convert domain entity to ORM model
        model = self._mapper.to_model(task)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        # Convert back to domain entity
        return self._mapper.to_entity(model)

    async def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        stmt = select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._mapper.to_entity(model) if model else None

    # In SQLAlchemy implementation (Infrastructure):
    async def get_all_by_user(
            self,
            user_id: int,
            filters: TaskFilterDTO
    ) -> List[Task]:
        stmt = select(TaskModel).where(TaskModel.user_id == user_id)

        # Apply filters
        if filters.status:
            stmt = stmt.where(TaskModel.status == filters.status)
        if filters.priority:
            stmt = stmt.where(TaskModel.priority == filters.priority)
        if filters.due_before:
            stmt = stmt.where(TaskModel.due_date <= filters.due_before)

        stmt = stmt.limit(filters.limit).offset(filters.offset)

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_entity(m) for m in models]
