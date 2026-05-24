# src/application/use_cases/update_task.py
from datetime import datetime

from ..interfaces.task_repository import ITaskRepository
from ..dtos.task_dto import UpdateTaskDTO, TaskResponseDTO
from ...domain.exceptions import TaskNotFoundException
from ...domain.services.task_hierarchy import build_children_index, validate_reparent


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
            all_tasks = await self._repository.get_all_tasks_for_user(dto.user_id)
            tasks_by_id = {t.id: t for t in all_tasks}
            tasks_by_id[task.id] = task
            children_index = build_children_index(all_tasks)

            if dto.parent_id is not None:
                parent = tasks_by_id.get(dto.parent_id)
                if parent is None:
                    parent = await self._repository.get_by_id(dto.parent_id, dto.user_id)
                    if parent is None:
                        raise TaskNotFoundException(dto.parent_id)

            validate_reparent(task, dto.parent_id, children_index)
            task.parent_id = dto.parent_id

        task.updated_at = datetime.utcnow()
        updated = await self._repository.update(task)
        return _to_response_dto(updated)
