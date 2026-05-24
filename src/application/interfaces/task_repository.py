# src/application/interfaces/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from ..dtos.task_dto import TaskFilterDTO
from ...domain.entities.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_max_group_name(self, user_id: int) -> int:
        pass

    @abstractmethod
    async def get_all_by_user(
            self,
            user_id: int,
            filters: TaskFilterDTO,
    ) -> List[Task]:
        pass
