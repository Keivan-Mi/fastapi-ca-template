# src/domain/value_objects/task_status.py
from enum import Enum

class TaskStatus(str, Enum):
    """Value object for task status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
