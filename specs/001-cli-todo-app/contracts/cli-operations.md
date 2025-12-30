# CLI Operations Contract: Phase I – In-Memory CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app
**Purpose**: Define contracts for all CLI operations and service layer functions

## Overview

This document specifies the contracts (function signatures, inputs, outputs, error conditions) for all operations in the Todo CLI application. These contracts define the interface between the CLI layer and the Services layer.

---

## Service Layer Contracts (`src/services/task_service.py`)

### 1. add_task

**Purpose**: Create a new task and add it to the in-memory list

**Signature**:
```python
def add_task(title: str, description: str = "") -> Task
```

**Inputs**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `title` | `str` | Yes | 1-200 chars, not empty | Task title |
| `description` | `str` | No | 0-1000 chars | Task description (default: "") |

**Outputs**:
| Type | Description |
|------|-------------|
| `Task` | Newly created task with auto-assigned ID and completed=False |

**Side Effects**:
- Appends task to `_tasks` list
- Increments `_next_id` counter

**Preconditions**:
- `title` is non-empty and ≤200 characters (validated by caller)
- `description` is ≤1000 characters (validated by caller)

**Postconditions**:
- New task exists in `_tasks` with unique ID
- `_next_id` incremented by 1
- Task has `completed=False`

**Example**:
```python
task = add_task("Buy groceries", "milk, eggs, bread")
# Returns: Task(id=1, title="Buy groceries", description="milk, eggs, bread", completed=False)
```

---

### 2. get_all_tasks

**Purpose**: Retrieve all tasks in the system

**Signature**:
```python
def get_all_tasks() -> list[Task]
```

**Inputs**: None

**Outputs**:
| Type | Description |
|------|-------------|
| `list[Task]` | Copy of all tasks (empty list if no tasks exist) |

**Side Effects**: None (pure read operation)

**Preconditions**: None

**Postconditions**:
- Returns copy of `_tasks` (modifications don't affect internal state)
- Order matches insertion order

**Example**:
```python
tasks = get_all_tasks()
# Returns: [Task(id=1, ...), Task(id=2, ...), Task(id=3, ...)]
# or: [] if no tasks
```

---

### 3. get_task_by_id

**Purpose**: Retrieve a specific task by its ID

**Signature**:
```python
def get_task_by_id(task_id: int) -> Task | None
```

**Inputs**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `task_id` | `int` | Yes | > 0 | ID of task to retrieve |

**Outputs**:
| Type | Description |
|------|-------------|
| `Task` | Task with matching ID |
| `None` | If no task found with that ID |

**Side Effects**: None (pure read operation)

**Preconditions**:
- `task_id` is a positive integer (validated by caller)

**Postconditions**:
- If found: returns Task object
- If not found: returns None
- No modifications to `_tasks`

**Example**:
```python
task = get_task_by_id(1)
# Returns: Task(id=1, title="Buy groceries", ...) or None
```

---

### 4. update_task

**Purpose**: Update title and/or description of an existing task

**Signature**:
```python
def update_task(task_id: int, title: str | None = None, description: str | None = None) -> bool
```

**Inputs**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `task_id` | `int` | Yes | > 0 | ID of task to update |
| `title` | `str \| None` | No | 1-200 chars if provided | New title (None = don't update) |
| `description` | `str \| None` | No | 0-1000 chars if provided | New description (None = don't update) |

**Outputs**:
| Type | Description |
|------|-------------|
| `bool` | `True` if task found and updated, `False` if task not found |

**Side Effects**:
- Modifies task in `_tasks` list if found
- Does not modify task if not found

**Preconditions**:
- `task_id` is positive integer (validated by caller)
- `title` (if provided) is non-empty and ≤200 chars (validated by caller)
- `description` (if provided) is ≤1000 chars (validated by caller)

**Postconditions**:
- If found: specified fields updated in place
- If not found: no changes to `_tasks`
- `completed` status unchanged
- ID unchanged

**Example**:
```python
success = update_task(1, title="New title")
# Returns: True (title updated, description unchanged)

success = update_task(1, description="New description")
# Returns: True (description updated, title unchanged)

success = update_task(1, title="New title", description="New desc")
# Returns: True (both updated)

success = update_task(999, title="Anything")
# Returns: False (task not found)
```

---

### 5. delete_task

**Purpose**: Delete a task from the list

**Signature**:
```python
def delete_task(task_id: int) -> bool
```

**Inputs**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `task_id` | `int` | Yes | > 0 | ID of task to delete |

**Outputs**:
| Type | Description |
|------|-------------|
| `bool` | `True` if task found and deleted, `False` if task not found |

**Side Effects**:
- Removes task from `_tasks` list if found
- Does NOT reuse the deleted ID (next ID continues incrementing)

**Preconditions**:
- `task_id` is positive integer (validated by caller)

**Postconditions**:
- If found: task removed from `_tasks`, returns True
- If not found: no changes, returns False
- `_next_id` NOT decremented (IDs never reused)

**Example**:
```python
success = delete_task(2)
# Returns: True (task with ID 2 removed)

success = delete_task(999)
# Returns: False (task not found)
```

---

### 6. toggle_complete

**Purpose**: Mark a task as complete or incomplete

**Signature**:
```python
def toggle_complete(task_id: int, target_status: bool) -> bool
```

**Inputs**:
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `task_id` | `int` | Yes | > 0 | ID of task to modify |
| `target_status` | `bool` | Yes | True or False | True=mark complete, False=mark incomplete |

**Outputs**:
| Type | Description |
|------|-------------|
| `bool` | `True` if task found and updated, `False` if task not found |

**Side Effects**:
- Sets `completed` field of task to `target_status`

**Preconditions**:
- `task_id` is positive integer (validated by caller)
- `target_status` is boolean

**Postconditions**:
- If found: `task.completed` set to `target_status`, returns True
- If not found: no changes, returns False
- Title and description unchanged

**Example**:
```python
success = toggle_complete(1, True)
# Returns: True (task 1 marked complete)

success = toggle_complete(1, False)
# Returns: True (task 1 marked incomplete)

success = toggle_complete(999, True)
# Returns: False (task not found)
```

---

## CLI Layer Contracts

### Menu Operations (`src/cli/menu.py`)

#### run_menu

**Purpose**: Main application loop

**Signature**:
```python
def run_menu() -> None
```

**Behavior**:
1. Display startup banner and persistence warning
2. Loop:
   - Display numbered menu (1-7)
   - Get user choice
   - Route to appropriate handler
   - Display result
   - Wait for Enter
3. Exit on choice 7

**Returns**: None (exits program)

---

### Display Operations (`src/cli/display.py`)

#### format_task_list

**Purpose**: Format all tasks for display

**Signature**:
```python
def format_task_list(tasks: list[Task]) -> str
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tasks` | `list[Task]` | Yes | List of tasks to format |

**Outputs**:
| Type | Description |
|------|-------------|
| `str` | Formatted string with all tasks or empty state message |

**Behavior**:
- If empty list: return "No tasks yet! Add your first task to get started."
- If non-empty: format each task with icon, ID, truncated title/description

**Example Output**:
```
───────────────────────────────────────
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread
[✅] ID: 2 | Call dentist
───────────────────────────────────────
```

#### format_single_task

**Purpose**: Format a single task for display

**Signature**:
```python
def format_single_task(task: Task) -> str
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | `Task` | Yes | Task to format |

**Outputs**:
| Type | Description |
|------|-------------|
| `str` | Formatted task string |

**Example Output**:
```
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread
```

#### get_status_icon

**Purpose**: Get icon for task status

**Signature**:
```python
def get_status_icon(completed: bool) -> str
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `completed` | `bool` | Yes | Task completion status |

**Outputs**:
| Type | Description |
|------|-------------|
| `str` | "✅" if completed=True, "⏳" if completed=False |

#### show_success

**Purpose**: Display success message

**Signature**:
```python
def show_success(message: str) -> None
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | `str` | Yes | Success message text |

**Outputs**: None (prints to stdout)

**Behavior**: Prints "✅ {message}"

#### show_error

**Purpose**: Display error message

**Signature**:
```python
def show_error(message: str) -> None
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | `str` | Yes | Error message text |

**Outputs**: None (prints to stdout)

**Behavior**: Prints "❌ {message}"

---

### Input Handling Operations (`src/cli/input_handler.py`)

#### get_menu_choice

**Purpose**: Get and validate menu choice from user

**Signature**:
```python
def get_menu_choice() -> int
```

**Inputs**: None (reads from stdin)

**Outputs**:
| Type | Description |
|------|-------------|
| `int` | Valid menu choice (1-7) |

**Behavior**:
- Prompt: "Enter choice (1-7): "
- Validate: must be integer 1-7
- Re-prompt on invalid input with error message
- Loop until valid

#### get_task_id

**Purpose**: Get and validate task ID from user

**Signature**:
```python
def get_task_id(prompt: str = "Enter task ID: ") -> int
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | `str` | No | Custom prompt text |

**Outputs**:
| Type | Description |
|------|-------------|
| `int` | Valid task ID (positive integer) |

**Behavior**:
- Display prompt
- Validate: must be positive integer
- Re-prompt on invalid input
- Loop until valid

#### get_title

**Purpose**: Get and validate task title from user

**Signature**:
```python
def get_title(prompt: str = "Enter title: ") -> str
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | `str` | No | Custom prompt text |

**Outputs**:
| Type | Description |
|------|-------------|
| `str` | Valid title (1-200 chars, stripped) |

**Behavior**:
- Display prompt
- Strip whitespace
- Validate: not empty, ≤200 chars
- Re-prompt on invalid input
- Loop until valid

#### get_description

**Purpose**: Get and validate task description from user

**Signature**:
```python
def get_description(prompt: str = "Enter description (optional, press Enter to skip): ") -> str
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | `str` | No | Custom prompt text |

**Outputs**:
| Type | Description |
|------|-------------|
| `str` | Valid description (0-1000 chars, stripped) or empty string |

**Behavior**:
- Display prompt
- Strip whitespace
- Validate: ≤1000 chars
- Allow empty (press Enter)
- Re-prompt if too long
- Loop until valid

#### get_confirmation

**Purpose**: Get yes/no confirmation from user

**Signature**:
```python
def get_confirmation(prompt: str) -> bool
```

**Inputs**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | `str` | Yes | Question to ask user |

**Outputs**:
| Type | Description |
|------|-------------|
| `bool` | True if user confirms (y/yes), False if user declines (n/no) |

**Behavior**:
- Display prompt + " (y/n): "
- Accept: y, yes, Y, YES (case-insensitive) → True
- Accept: n, no, N, NO (case-insensitive) → False
- Re-prompt on invalid input
- Loop until valid

---

## Error Handling Contracts

### Input Validation Errors

**Handled By**: CLI layer (`input_handler.py`)

| Error Condition | Error Message | Recovery |
|----------------|---------------|----------|
| Empty title | "❌ Title is required. Please enter a title." | Re-prompt |
| Title too long (>200) | "❌ Title must be 200 characters or less." | Re-prompt |
| Description too long (>1000) | "❌ Description must be 1000 characters or less." | Re-prompt |
| Invalid menu choice | "❌ Please enter a number between 1 and 7." | Re-prompt |
| Non-numeric ID | "❌ Please enter a valid task ID (number)." | Re-prompt |
| Task not found | "❌ Task not found with ID {id}." | Return to menu |

### Service Layer Errors

**Policy**: Services return `None` or `False` for not-found conditions, not exceptions

| Condition | Return Value | CLI Handling |
|-----------|--------------|--------------|
| Task not found | `None` (get) or `False` (update/delete/toggle) | Show error, return to menu |
| Empty list | Empty list `[]` | Show "No tasks yet!" message |

### System Errors

**Handled By**: Top level in `main.py`

**Strategy**: Catch-all exception handler

```python
try:
    run_menu()
except KeyboardInterrupt:
    print("\n\nGoodbye!")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("Please restart the application.")
    exit(1)
```

---

## Operation Flow Contracts

### Add Task Flow

```
1. CLI calls get_title() → validates & returns title
2. CLI calls get_description() → validates & returns description
3. CLI calls add_task(title, desc) → returns Task
4. CLI calls show_success(f"Task added successfully! (ID: {task.id})")
```

### View Tasks Flow

```
1. CLI calls get_all_tasks() → returns list[Task]
2. CLI calls format_task_list(tasks) → returns formatted string
3. CLI prints result
```

### Update Task Flow

```
1. CLI calls get_task_id() → validates & returns id
2. CLI calls get_task_by_id(id) → returns Task or None
3. If None: CLI calls show_error("Task not found"), return to menu
4. If Task: CLI displays task details
5. CLI prompts for what to update (title/desc/both)
6. CLI calls get_title() and/or get_description() as needed
7. CLI calls update_task(id, title, desc) → returns bool
8. CLI calls show_success("Task updated successfully!")
```

### Delete Task Flow

```
1. CLI calls get_task_id() → validates & returns id
2. CLI calls get_task_by_id(id) → returns Task or None
3. If None: CLI calls show_error("Task not found"), return to menu
4. If Task: CLI displays task details
5. CLI calls get_confirmation("Delete this task?") → returns bool
6. If False: CLI shows "Deletion cancelled", return to menu
7. If True: CLI calls delete_task(id) → returns bool
8. CLI calls show_success("Task deleted successfully!")
```

### Mark Complete/Incomplete Flow

```
1. CLI calls get_task_id() → validates & returns id
2. CLI calls toggle_complete(id, target_status) → returns bool
3. If False: CLI calls show_error("Task not found")
4. If True: CLI calls show_success("Task marked {complete/incomplete}!")
```

---

## Contract Summary

| Layer | Module | Functions | Responsibility |
|-------|--------|-----------|----------------|
| **Service** | `task_service.py` | 6 functions | CRUD operations, validation, storage |
| **CLI** | `menu.py` | 1 function | Main control loop, routing |
| **CLI** | `display.py` | 5 functions | Formatting, messages, icons |
| **CLI** | `input_handler.py` | 5 functions | Input validation, prompting |
| **Entry** | `main.py` | 1 function | Bootstrap, error handling |

**Total**: 18 functions across 5 modules

---

## Contract Status

✅ **Complete** - All operation contracts defined with signatures, inputs, outputs, and behaviors

**Next**: Generate quickstart.md for user manual and testing guide
