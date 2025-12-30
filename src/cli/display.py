"""Display formatting and output functions"""
from src.models.task import Task


def get_status_text(completed: bool) -> str:
    """
    Get status text for task.

    Args:
        completed: Task completion status

    Returns:
        "DONE" if completed=True, "TODO" if completed=False
    """
    return "DONE" if completed else "TODO"


def format_task_table(tasks: list[Task]) -> str:
    """
    Format all tasks as a table.

    Args:
        tasks: List of tasks to format

    Returns:
        Formatted table string with headers and rows
    """
    if not tasks:
        return "No tasks found."

    # Calculate column widths
    id_width = max(len("ID"), max(len(str(t.id)) for t in tasks))
    title_width = max(len("TITLE"), max(len(t.title[:50]) for t in tasks))
    status_width = 6  # "STATUS"

    # Build header
    header = f"{'ID':<{id_width}}  {'TITLE':<{title_width}}  STATUS"
    separator = "-" * len(header)

    lines = [separator, header, separator]

    # Build rows
    for task in tasks:
        task_id = str(task.id)
        title = task.title[:50]
        status = get_status_text(task.completed)

        lines.append(f"{task_id:<{id_width}}  {title:<{title_width}}  {status}")

    lines.append(separator)

    return "\n".join(lines)


def show_message(message: str) -> None:
    """
    Display neutral message.

    Args:
        message: Message text
    """
    print(message)
