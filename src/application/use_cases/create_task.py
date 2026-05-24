# src/application/use_cases/create_task.py
from datetime import datetime
from ..interfaces.task_repository import ITaskRepository
from ..dtos.task_dto import CreateTaskDTO, TaskResponseDTO
from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus
from ...domain.exceptions import TaskNotFoundException


def _to_response_dto(task: Task) -> TaskResponseDTO:
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


class CreateTaskUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    async def execute(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        parent_id = dto.parent_id
        if parent_id is not None:
            parent = await self._repository.get_by_id(parent_id, dto.user_id)
            if parent is None:
                raise TaskNotFoundException(parent_id)

        task = Task(
            id=None,
            title=dto.title,
            description=dto.description,
            status=TaskStatus.TODO,
            priority=dto.priority,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            user_id=dto.user_id,
            due_date=dto.due_date,
            estimated_time=dto.estimated_time,
            parent_id=parent_id,
        )

        created_task = await self._repository.create(task)
        return _to_response_dto(created_task)
