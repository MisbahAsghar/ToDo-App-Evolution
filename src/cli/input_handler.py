"""Input validation and prompting functions"""


def get_menu_choice() -> int:
    """
    Get and validate menu choice from user.

    Returns:
        Valid menu choice (1-7)
    """
    while True:
        try:
            choice = input("Choice (1-7): ").strip()
            choice_int = int(choice)
            if 1 <= choice_int <= 7:
                return choice_int
            else:
                print("Enter a number between 1 and 7.")
        except ValueError:
            print("Enter a number between 1 and 7.")


def get_task_id(prompt: str = "Task ID: ") -> int:
    """
    Get and validate task ID from user.

    Args:
        prompt: Custom prompt text

    Returns:
        Valid task ID (positive integer)
    """
    while True:
        try:
            id_str = input(prompt).strip()
            task_id = int(id_str)
            if task_id > 0:
                return task_id
            else:
                print("Enter a valid task ID.")
        except ValueError:
            print("Enter a valid task ID.")


def get_title(prompt: str = "Title: ") -> str:
    """
    Get and validate task title from user.

    Args:
        prompt: Custom prompt text

    Returns:
        Valid title (1-200 chars, stripped)
    """
    while True:
        title = input(prompt).strip()
        if not title:
            print("Title is required.")
        elif len(title) > 200:
            print("Title must be 200 characters or less.")
        else:
            return title


def get_description(prompt: str = "Description (optional): ") -> str:
    """
    Get and validate task description from user.

    Args:
        prompt: Custom prompt text

    Returns:
        Valid description (0-1000 chars, stripped) or empty string
    """
    while True:
        description = input(prompt).strip()
        if len(description) > 1000:
            print("Description must be 1000 characters or less.")
        else:
            return description


def get_confirmation(prompt: str) -> bool:
    """
    Get yes/no confirmation from user.

    Args:
        prompt: Question to ask user

    Returns:
        True if user confirms (y/yes), False if user declines (n/no)
    """
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Enter 'y' or 'n'.")
