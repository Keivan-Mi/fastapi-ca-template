# src/application/use_cases/get_tasks.py
from typing import List

from ..interfaces.task_repository import ITaskRepository
from ..dtos.task_dto import TaskFilterDTO, TaskResponseDTO


class GetTasksUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    async def execute(self, user_id: int, filters: TaskFilterDTO) -> List[TaskResponseDTO]:
        tasks = await self._repository.get_all_by_user(user_id=user_id, filters=filters)
        return [
            TaskResponseDTO(
                id=t.id,
                title=t.title,
                description=t.description,
                status=t.status,
                priority=t.priority,
                created_at=t.created_at,
                updated_at=t.updated_at,
                due_date=t.due_date,
                estimated_time=t.estimated_time,
                parent_id=t.parent_id,
            )
            for t in tasks
        ]
