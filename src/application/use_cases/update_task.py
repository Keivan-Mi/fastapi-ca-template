# src/application/use_cases/update_task.py
from datetime import datetime

from ..interfaces.task_repository import ITaskRepository
from ..dtos.task_dto import UpdateTaskDTO, TaskResponseDTO
from ...domain.exceptions import TaskNotFoundException, InvalidParentException


def _to_response_dto(task) -> TaskResponseDTO:
    return TaskResponseDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        created_at=task.created_at,
        updated_at=task.updated_at,
        due_date=task.due_date,
        estimated_time=task.estimated_time,
        parent_id=task.parent_id,
        group_name=task.group_name,
        level=task.level,
    )


class UpdateTaskUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    async def execute(self, dto: UpdateTaskDTO) -> TaskResponseDTO:
        task = await self._repository.get_by_id(dto.task_id, dto.user_id)
        if task is None:
            raise TaskNotFoundException(dto.task_id)

        if dto.title is not None:
            task.title = dto.title
        if dto.description is not None:
            task.description = dto.description
        if dto.priority is not None:
            task.priority = dto.priority
        if dto.due_date is not None:
            task.due_date = dto.due_date
        if dto.status is not None:
            task.status = dto.status
        if dto.estimated_time is not None:
            task.estimated_time = dto.estimated_time

        if dto.update_parent:
            await self._validate_parent(task, dto.parent_id, dto.user_id)
            task.parent_id = dto.parent_id

        task.updated_at = datetime.utcnow()
        updated = await self._repository.update(task)
        return _to_response_dto(updated)

    async def _validate_parent(
            self,
            task,
            parent_id: int | None,
            user_id: int,
    ) -> None:
        if parent_id is None:
            return

        if parent_id == task.id:
            raise InvalidParentException("A task cannot be its own parent")

        parent = await self._repository.get_by_id(parent_id, user_id)
        if parent is None:
            raise TaskNotFoundException(parent_id)

        if parent.group_name != task.group_name:
            raise InvalidParentException(
                "Parent must belong to the same group as the task"
            )

        if parent.level > task.level:
            raise InvalidParentException(
                "Parent must have a lower level than the task"
            )
