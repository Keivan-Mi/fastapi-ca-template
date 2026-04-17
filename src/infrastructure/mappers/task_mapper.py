# src/infrastructure/mappers/task_mapper.py
"""Maps between domain Task entity and SQLAlchemy TaskModel (Infrastructure)."""

from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus
from ...domain.value_objects.priority import Priority
from ..db.models import TaskModel


class TaskMapper:
    """Maps Task entity <-> TaskModel. Keeps domain and persistence separate."""

    def to_entity(self, model: TaskModel) -> Task:
        """ORM model -> domain entity."""
        if model is None:
            raise ValueError("TaskModel cannot be None")
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            priority=model.priority,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            due_date=model.due_date,
        )

    def to_model(self, task: Task) -> TaskModel:
        """Domain entity -> ORM model."""
        kwargs = dict(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id,
            due_date=task.due_date,
        )
        if task.id is not None:
            kwargs["id"] = task.id
        return TaskModel(**kwargs)
