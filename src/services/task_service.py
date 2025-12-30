"""Task management service - CRUD operations and business logic"""
from typing import Optional
from src.models.task import Task


# In-memory storage
_tasks: list[Task] = []
_next_id: int = 1


def add_task(title: str, description: str = "") -> Task:
    """
    Create a new task and add it to the in-memory list.

    Args:
        title: Task title (1-200 chars, pre-validated by CLI)
        description: Optional task description (0-1000 chars)

    Returns:
        Newly created Task with auto-assigned ID and completed=False
    """
    global _next_id
    task = Task(id=_next_id, title=title, description=description, completed=False)
    _tasks.append(task)
    _next_id += 1
    return task


def get_all_tasks() -> list[Task]:
    """
    Retrieve all tasks in the system.

    Returns:
        Copy of all tasks (empty list if no tasks exist)
    """
    return _tasks.copy()


def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Retrieve a specific task by its ID.

    Args:
        task_id: ID of task to retrieve (positive integer)

    Returns:
        Task with matching ID, or None if not found
    """
    for task in _tasks:
        if task.id == task_id:
            return task
    return None


def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
    """
    Update title and/or description of an existing task.

    Args:
        task_id: ID of task to update
        title: New title (None = don't update)
        description: New description (None = don't update)

    Returns:
        True if task found and updated, False if not found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    return True


def delete_task(task_id: int) -> bool:
    """
    Delete a task from the list.

    Args:
        task_id: ID of task to delete

    Returns:
        True if task found and deleted, False if not found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    _tasks.remove(task)
    return True


def toggle_complete(task_id: int, target_status: bool) -> bool:
    """
    Mark a task as complete or incomplete.

    Args:
        task_id: ID of task to modify
        target_status: True=mark complete, False=mark incomplete

    Returns:
        True if task found and updated, False if not found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    task.completed = target_status
    return True
