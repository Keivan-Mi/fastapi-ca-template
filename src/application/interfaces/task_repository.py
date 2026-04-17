# src/application/interfaces/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from ..dtos.task_dto import TaskFilterDTO
from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus


class ITaskRepository(ABC):
    """Abstract repository interface - DIP in action!

    Application layer defines the interface it needs.
    Infrastructure layer implements it.
    This inverts the dependency - Infrastructure depends on Application.
    """

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task"""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get task by ID"""
        pass

    @abstractmethod
    async def get_all_by_user(
            self,
            user_id: int,
            filters: TaskFilterDTO,
            status: Optional[TaskStatus] = None,
            limit: int = 100,
            offset: int = 0,
    ) -> List[Task]:
        """Get all tasks for a user with optional filtering"""
        pass
