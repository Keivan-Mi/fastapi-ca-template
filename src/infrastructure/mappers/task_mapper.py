# src/infrastructure/mappers/task_mapper.py
from ...domain.entities.task import Task
from ..db.models import TaskModel


class TaskMapper:
    def to_entity(self, model: TaskModel) -> Task:
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
            estimated_time=model.estimated_time,
            parent_id=model.parent_id,
        )

    def to_model(self, task: Task) -> TaskModel:
        kwargs = dict(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=task.user_id,
            due_date=task.due_date,
            estimated_time=task.estimated_time,
            parent_id=task.parent_id,
        )
        if task.id is not None:
            kwargs["id"] = task.id
        return TaskModel(**kwargs)
