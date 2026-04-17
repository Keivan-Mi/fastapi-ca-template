# src/application/use_cases/create_task.py
from datetime import datetime
from ..interfaces.task_repository import ITaskRepository
from ..dtos.task_dto import CreateTaskDTO, TaskResponseDTO
from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus


class CreateTaskUseCase:
    """Use case for creating a new task

    Notice: Depends on ITaskRepository (interface), not concrete implementation!
    """

    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    async def execute(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        """Execute the use case"""
        # Create domain entity
        task = Task(
            id=None,
            title=dto.title,
            description=dto.description,
            status=TaskStatus.TODO,
            priority=dto.priority,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            user_id=dto.user_id,
            due_date=dto.due_date
        )

        # Persist using repository
        created_task = await self._repository.create(task)

        # Return DTO
        return TaskResponseDTO(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            status=created_task.status,
            priority=created_task.priority,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at,
            due_date=created_task.due_date,
        )
