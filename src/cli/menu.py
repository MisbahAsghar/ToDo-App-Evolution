"""Main menu and CLI flow control"""
from src.services import task_service
from src.cli import display, input_handler


def display_banner() -> None:
    """Display startup banner."""
    print("\n" + "=" * 50)
    print("  TODO APPLICATION")
    print("=" * 50)


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "+" + "-" * 48 + "+")
    print("|" + " " * 19 + "MAIN MENU" + " " * 20 + "|")
    print("+" + "-" * 48 + "+")
    print("| 1. Add Task" + " " * 37 + "|")
    print("| 2. View Tasks" + " " * 35 + "|")
    print("| 3. Update Task" + " " * 34 + "|")
    print("| 4. Delete Task" + " " * 34 + "|")
    print("| 5. Mark Task Complete" + " " * 27 + "|")
    print("| 6. Mark Task Incomplete" + " " * 25 + "|")
    print("| 7. Quit" + " " * 41 + "|")
    print("+" + "-" * 48 + "+")


def add_task_flow() -> None:
    """Handle add task operation."""
    print("\nAdd Task")
    print("-" * 40)
    title = input_handler.get_title()
    description = input_handler.get_description()

    task = task_service.add_task(title, description)
    display.show_message(f"Task {task.id} added.")


def view_tasks_flow() -> None:
    """Handle view tasks operation."""
    print("\nTasks")
    print("-" * 40)
    tasks = task_service.get_all_tasks()
    print(display.format_task_table(tasks))


def update_task_flow() -> None:
    """Handle update task operation."""
    print("\nUpdate Task")
    print("-" * 40)
    task_id = input_handler.get_task_id()

    task = task_service.get_task_by_id(task_id)
    if task is None:
        display.show_message(f"Task {task_id} not found.")
        return

    print(f"\nCurrent: {task.title}")
    print("Update: (1) Title  (2) Description  (3) Both")

    while True:
        try:
            choice = int(input("Enter choice: ").strip())
            if choice in [1, 2, 3]:
                break
            else:
                print("Enter 1, 2, or 3.")
        except ValueError:
            print("Enter 1, 2, or 3.")

    new_title = None
    new_description = None

    if choice in [1, 3]:
        new_title = input_handler.get_title("New title: ")

    if choice in [2, 3]:
        new_description = input_handler.get_description("New description: ")

    task_service.update_task(task_id, new_title, new_description)
    display.show_message("Task updated.")


def delete_task_flow() -> None:
    """Handle delete task operation."""
    print("\nDelete Task")
    print("-" * 40)
    task_id = input_handler.get_task_id()

    task = task_service.get_task_by_id(task_id)
    if task is None:
        display.show_message(f"Task {task_id} not found.")
        return

    print(f"\nTask: {task.title}")

    if input_handler.get_confirmation("Delete?"):
        task_service.delete_task(task_id)
        display.show_message("Task deleted.")
    else:
        display.show_message("Cancelled.")


def mark_complete_flow() -> None:
    """Handle mark task complete operation."""
    print("\nMark Complete")
    print("-" * 40)
    task_id = input_handler.get_task_id()

    if task_service.toggle_complete(task_id, True):
        display.show_message("Task marked complete.")
    else:
        display.show_message(f"Task {task_id} not found.")


def mark_incomplete_flow() -> None:
    """Handle mark task incomplete operation."""
    print("\nMark Incomplete")
    print("-" * 40)
    task_id = input_handler.get_task_id()

    if task_service.toggle_complete(task_id, False):
        display.show_message("Task marked incomplete.")
    else:
        display.show_message(f"Task {task_id} not found.")


def run_menu() -> None:
    """Main application loop."""
    display_banner()

    running = True
    while running:
        display_menu()
        choice = input_handler.get_menu_choice()

        if choice == 1:
            add_task_flow()
        elif choice == 2:
            view_tasks_flow()
        elif choice == 3:
            update_task_flow()
        elif choice == 4:
            delete_task_flow()
        elif choice == 5:
            mark_complete_flow()
        elif choice == 6:
            mark_incomplete_flow()
        elif choice == 7:
            print("\nGoodbye.")
            running = False

        if running:
            input("\nPress Enter to continue...")
