# src/infrastructure/db/task_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from ...application.dtos.task_dto import TaskFilterDTO
from ...application.interfaces.task_repository import ITaskRepository
from ...domain.entities.task import Task
from .models import TaskModel
from ..mappers.task_mapper import TaskMapper


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper = TaskMapper()

    async def create(self, task: Task) -> Task:
        model = self._mapper.to_model(task)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._mapper.to_entity(model)

    async def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        stmt = select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._mapper.to_entity(model) if model else None

    async def update(self, task: Task) -> Task:
        stmt = select(TaskModel).where(
            TaskModel.id == task.id,
            TaskModel.user_id == task.user_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()

        model.title = task.title
        model.description = task.description
        model.status = task.status
        model.priority = task.priority
        model.updated_at = task.updated_at
        model.due_date = task.due_date
        model.estimated_time = task.estimated_time
        model.parent_id = task.parent_id
        model.group_name = task.group_name
        model.level = task.level

        await self._session.commit()
        await self._session.refresh(model)
        return self._mapper.to_entity(model)

    async def get_max_group_name(self, user_id: int) -> int:
        stmt = select(func.max(TaskModel.group_name)).where(
            TaskModel.user_id == user_id
        )
        result = await self._session.execute(stmt)
        value = result.scalar_one_or_none()
        return value or 0

    async def get_all_by_user(
            self,
            user_id: int,
            filters: TaskFilterDTO
    ) -> List[Task]:
        stmt = select(TaskModel).where(TaskModel.user_id == user_id)

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
