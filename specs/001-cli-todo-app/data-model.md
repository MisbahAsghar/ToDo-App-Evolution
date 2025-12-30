# Data Model: Phase I – In-Memory CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app
**Purpose**: Define data structures, validation rules, and relationships

## Overview

The Phase I Todo App has a single entity: **Task**. This document defines the Task structure, validation rules, state transitions, and in-memory storage strategy.

---

## Entity: Task

### Definition

A Task represents a single todo item that a user wants to track. It contains all information needed to display, update, and manage the task throughout the application session.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | `int` | Yes | Auto-assigned | > 0, unique | Unique identifier, auto-incrementing |
| `title` | `str` | Yes | (none) | 1-200 chars, not empty | Task title, displayed in list |
| `description` | `str` | No | `""` | 0-1000 chars | Optional details about the task |
| `completed` | `bool` | Yes | `False` | True or False | Task completion status |

### Python Implementation

```python
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
```

**Why dataclass**: Provides automatic `__init__`, `__repr__`, `__eq__`, and type hints support. Aligns with constitutional requirements for type safety (Principle IV) and simplicity (Principle II).

---

## Validation Rules

### Title Validation

| Rule | Description | Error Message |
|------|-------------|---------------|
| **Not Empty** | Title must contain at least 1 non-whitespace character | "❌ Title is required. Please enter a title." |
| **Max Length** | Title must be 200 characters or less | "❌ Title must be 200 characters or less." |
| **Whitespace Handling** | Leading/trailing whitespace is stripped before validation | (auto-corrected) |

**Validation Location**: `src/cli/input_handler.py` (UI layer)

**Service Layer**: Assumes title is valid (pre-validated by CLI)

### Description Validation

| Rule | Description | Error Message |
|------|-------------|---------------|
| **Optional** | Description can be empty string | (none - allowed) |
| **Max Length** | Description must be 1000 characters or less | "❌ Description must be 1000 characters or less." |
| **Whitespace Handling** | Leading/trailing whitespace is stripped | (auto-corrected) |

**Validation Location**: `src/cli/input_handler.py` (UI layer)

**Service Layer**: Assumes description is valid or empty

### ID Validation

| Rule | Description | Error Message |
|------|-------------|---------------|
| **Numeric** | Must be a valid integer | "❌ Please enter a valid task ID (number)." |
| **Positive** | Must be > 0 | "❌ Please enter a valid task ID (number)." |
| **Exists** | Must match an existing task ID | "❌ Task not found with ID {id}." |

**Validation Location**:
- Numeric/Positive: `src/cli/input_handler.py`
- Exists: `src/services/task_service.py` (via get_task_by_id)

### Completed Validation

| Rule | Description |
|------|-------------|
| **Type** | Must be boolean (True/False) |
| **No User Input** | Set by application only (user doesn't input boolean) |

**Note**: User never directly inputs boolean - they select "Mark Complete" or "Mark Incomplete" from menu.

---

## State Transitions

### Task Lifecycle

```
┌─────────────┐
│   Created   │
│ (completed: │
│   False)    │
└──────┬──────┘
       │
       │ User selects "Add Task"
       │
       ▼
┌─────────────┐
│  Incomplete │◄─────────────┐
│     ⏳      │              │
└──────┬──────┘              │
       │                     │
       │ User: "Mark         │ User: "Mark
       │  Complete"          │  Incomplete"
       │                     │
       ▼                     │
┌─────────────┐              │
│  Complete   ├──────────────┘
│     ✅      │
└──────┬──────┘
       │
       │ User: "Delete Task"
       │
       ▼
┌─────────────┐
│   Deleted   │
│ (removed    │
│  from list) │
└─────────────┘
```

### Valid State Transitions

| From State | To State | Trigger | Notes |
|------------|----------|---------|-------|
| (none) | Incomplete | `add_task()` | New task created with completed=False |
| Incomplete | Complete | `toggle_complete(id)` | User marks task done |
| Complete | Incomplete | `toggle_complete(id)` | User marks task undone |
| Incomplete | Deleted | `delete_task(id)` | User deletes incomplete task |
| Complete | Deleted | `delete_task(id)` | User deletes complete task |
| Any | (updated) | `update_task(id, ...)` | Title/description changed, status unchanged |

**No Invalid Transitions**: All state changes are user-initiated and validated.

---

## Relationships

### Task Relationships

**None** - Tasks are independent entities with no relationships to other tasks in Phase I.

**Out of Scope** (from spec):
- Parent/child task hierarchies
- Task dependencies
- Task categories or tags
- Task assignments (multi-user)

---

## In-Memory Storage

### Storage Structure

**Location**: `src/services/task_service.py` (module-level)

**Data Structure**:
```python
_tasks: list[Task] = []
_next_id: int = 1
```

**Access Pattern**:
- **Private**: Variables prefixed with `_` (not exported from module)
- **Public API**: Access only through service functions
- **Isolation**: CLI and other layers cannot directly access storage

### Storage Operations

| Operation | Function | Complexity | Description |
|-----------|----------|------------|-------------|
| Create | `add_task()` | O(1) | Append to list |
| Read (all) | `get_all_tasks()` | O(n) | Return copy of list |
| Read (one) | `get_task_by_id()` | O(n) | Linear search by ID |
| Update | `update_task()` | O(n) | Find + modify in place |
| Delete | `delete_task()` | O(n) | Find + remove from list |
| Toggle status | `toggle_complete()` | O(n) | Find + modify completed field |

**Performance Note**: O(n) operations are acceptable given expected scale (<100 tasks per session, per spec SC-007)

### ID Generation Strategy

**Algorithm**: Auto-increment integer counter

**Implementation**:
```python
_next_id: int = 1

def add_task(title: str, description: str = "") -> Task:
    global _next_id
    task = Task(id=_next_id, title=title, description=description)
    _tasks.append(task)
    _next_id += 1
    return task
```

**Properties**:
- IDs start at 1
- IDs increment by 1 for each new task
- IDs are never reused (even after deletion)
- IDs are sequential and predictable

**Rationale**: Simple, user-friendly, meets spec requirement FR-003 ("unique, auto-incrementing numeric ID")

### Storage Lifetime

**Session-Based**: Storage exists only for the duration of the application run

**Characteristics**:
- Initialized empty when app starts
- Grows as tasks are added
- Cleared when app exits
- No persistence between runs (per spec FR-016)

---

## Data Flow

### Task Creation Flow

```
1. User enters title and optional description (CLI)
2. CLI validates input (input_handler.py)
3. CLI calls add_task(title, desc) (task_service.py)
4. Service creates Task with next available ID
5. Service appends Task to _tasks list
6. Service increments _next_id
7. Service returns Task object
8. CLI displays success message with ID
```

### Task Retrieval Flow

```
1. User selects "View Tasks" (CLI)
2. CLI calls get_all_tasks() (task_service.py)
3. Service returns copy of _tasks list
4. CLI formats and displays each task (display.py)
```

### Task Update Flow

```
1. User enters task ID (CLI)
2. CLI validates ID is numeric (input_handler.py)
3. CLI calls get_task_by_id(id) (task_service.py)
4. Service searches _tasks for matching ID
5. If not found: return None → CLI shows error
6. If found: return Task → CLI prompts for updates
7. User enters new values (CLI)
8. CLI calls update_task(id, new_values) (task_service.py)
9. Service finds task and modifies in place
10. CLI displays success message
```

### Task Deletion Flow

```
1. User enters task ID (CLI)
2. CLI calls get_task_by_id(id) for confirmation display
3. User confirms deletion (CLI)
4. CLI calls delete_task(id) (task_service.py)
5. Service finds task in _tasks list
6. Service removes task from list
7. CLI displays success message
```

**Note**: Deleted task IDs are not reused. If tasks 1, 2, 3 exist and task 2 is deleted, next new task gets ID 4 (not 2).

---

## Display Formatting

### List View Format

**Full Task** (when not truncated):
```
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread
```

**Truncated Title** (>50 chars):
```
[⏳] ID: 2 | This is a very long title that exceeds the max...
    description here
```

**Truncated Description** (>30 chars):
```
[✅] ID: 3 | Short title
    This is a long description...
```

**No Description**:
```
[⏳] ID: 4 | Call dentist
```

### Truncation Rules

**Implemented in**: `src/cli/display.py`

| Field | Max Display Length | Truncation Suffix | Storage Impact |
|-------|-------------------|-------------------|----------------|
| Title | 50 characters | `"..."` | None (display only) |
| Description | 30 characters | `"..."` | None (display only) |

**Important**: Truncation is display-only. Full values are stored and can be viewed in detail views or updated.

### Icon Mapping

| Status | Boolean Value | Icon | Display Text |
|--------|---------------|------|--------------|
| Incomplete | `False` | ⏳ | "incomplete" |
| Complete | `True` | ✅ | "complete" |

**Implemented in**: `src/cli/display.py`

---

## Examples

### Example 1: Basic Task

```python
task = Task(
    id=1,
    title="Buy groceries",
    description="milk, eggs, bread",
    completed=False
)
```

**Display**:
```
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread
```

### Example 2: Completed Task

```python
task = Task(
    id=2,
    title="Call dentist",
    description="",
    completed=True
)
```

**Display**:
```
[✅] ID: 2 | Call dentist
```

### Example 3: Task with Long Title

```python
task = Task(
    id=3,
    title="Research and compare different health insurance plans for next year's enrollment period",
    description="Focus on deductibles and coverage",
    completed=False
)
```

**Display** (title truncated to 50 chars):
```
[⏳] ID: 3 | Research and compare different health insuran...
    Focus on deductibles and c...
```

**Note**: Full title and description remain in storage, accessible via update or detail views.

---

## Data Model Constraints Summary

| Constraint | Rule | Enforced By |
|------------|------|-------------|
| Unique IDs | Each task has unique ID | task_service.py (auto-increment) |
| ID >= 1 | All IDs are positive integers | task_service.py (_next_id starts at 1) |
| Title required | Cannot be empty | input_handler.py (validation) |
| Title max 200 | Length limit | input_handler.py (validation) |
| Description max 1000 | Length limit | input_handler.py (validation) |
| Boolean status | True or False only | Python type system (bool) |
| In-memory only | No persistence | Architecture (no file/DB operations) |

---

## Testing Considerations

### Data Model Tests

**Unit Tests** (`tests/unit/test_task_service.py`):
- Test task creation with valid data
- Test ID auto-increment (1, 2, 3...)
- Test ID uniqueness across adds/deletes
- Test empty description default
- Test completed default (False)
- Test task equality (dataclass __eq__)

**Invalid Data Tests**:
- Title validation (empty, too long)
- Description validation (too long)
- ID validation (negative, zero, non-numeric)

**Edge Cases**:
- Task with exactly 200 char title
- Task with exactly 1000 char description
- Task with exactly 50 char title (no truncation)
- Task with exactly 51 char title (truncation triggered)
- Adding 100+ tasks (performance test per SC-007)

---

## Data Model Status

✅ **Complete** - All entity definitions, validation rules, and storage strategies defined

**Next**: Generate contracts for CLI operations (contracts/cli-operations.md)
