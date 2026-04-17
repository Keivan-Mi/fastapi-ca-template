# src/domain/exceptions.py

class DomainException(Exception):
    """Base exception for domain layer"""
    pass

class TaskNotFoundException(DomainException):
    """Raised when a task is not found"""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")

class UnauthorizedAccessException(DomainException):
    """Raised when user tries to access unauthorized resource"""
    def __init__(self, user_id: int, resource_id: int):
        self.user_id = user_id
        self.resource_id = resource_id
        super().__init__(
            f"User {user_id} is not authorized to access resource {resource_id}"
        )

class InvalidTaskStateException(DomainException):
    """Raised when task state transition is invalid"""
    pass
