# src/domain/value_objects/priority.py
from enum import Enum

class Priority(str, Enum):
    """Value object for priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
