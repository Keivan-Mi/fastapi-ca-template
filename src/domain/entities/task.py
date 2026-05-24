# src/domain/entities/task.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.task_status import TaskStatus
from ..value_objects.priority import Priority


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    created_at: datetime
    updated_at: datetime
    user_id: int
    due_date: datetime | None
    estimated_time: int | None
    parent_id: int | None
    group_name: int
    level: int

    def mark_as_completed(self) -> None:
        """Business rule: mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def is_overdue(self, current_date: datetime) -> bool:
        """Business logic for checking overdue status"""
        if self.due_date and self.status != TaskStatus.COMPLETED:
            return current_date > self.due_date
        return False
