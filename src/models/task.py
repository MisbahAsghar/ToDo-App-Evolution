"""Task data model"""
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique numeric identifier (auto-assigned)
        title: Task title (1-200 characters)
        description: Optional task details (0-1000 characters)
        completed: Completion status (True = done, False = pending)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
