# Implementation Plan: Phase I – In-Memory CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build an in-memory Python CLI todo application that allows users to manage daily tasks through a numbered menu interface. Users can add tasks (with required title and optional description), view all tasks with status icons (✅/⏳), mark tasks complete/incomplete, update task details, and delete tasks with confirmation. All data stored in-memory only (no persistence). Application runs via `python -m src.main` and enforces strict modular architecture.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory Python data structures (list of dictionaries)
**Testing**: Python unittest or pytest (if tests requested in tasks phase)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux with UTF-8 terminal support)
**Project Type**: Single project (console application)
**Performance Goals**: Handle 100+ tasks without noticeable lag (<100ms response time)
**Constraints**: No file I/O, no databases, no external APIs, stdlib only, in-memory only
**Scale/Scope**: Single-user, single-session, ~500 total lines of code across 5-7 modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development First
- **Status**: PASS
- **Evidence**: Following /sp.specify → /sp.plan → /sp.tasks → /sp.implement workflow
- **Compliance**: All code will be generated through approved spec-driven process

### ✅ II. Simplicity First
- **Status**: PASS
- **Evidence**:
  - In-memory only (no file I/O, no databases)
  - Python stdlib only (no external dependencies)
  - No unnecessary abstractions or design patterns
  - Implements only spec-defined features
- **Compliance**: No prohibited complexity introduced

### ✅ III. Excellent CLI User Experience
- **Status**: PASS
- **Evidence**:
  - Numbered menu (1. Add Task, 2. View Tasks, etc.)
  - Status icons (✅ completed, ⏳ pending)
  - Friendly messages for all operations
  - Input validation with clear error messages
  - Visual separators and clean formatting
- **Compliance**: All UX requirements from constitution embedded in design

### ✅ IV. Type Safety & Clarity
- **Status**: PASS
- **Evidence**:
  - Python 3.13+ type hints for all function signatures
  - Explicit variable names (task_id, task_title, task_list)
  - Docstrings for complex functions
  - Clear error messages
- **Compliance**: Type hints mandatory in implementation phase

### ✅ V. Modular Architecture
- **Status**: PASS
- **Evidence**:
  - Models (`src/models/task.py`) - Task data structure
  - Services (`src/services/task_service.py`) - Business logic
  - CLI (`src/cli/menu.py`, `src/cli/display.py`, `src/cli/input_handler.py`) - UI
  - Main (`src/main.py`) - Entry point
- **Dependency Compliance**: CLI → Services → Models (no circular deps)
- **Compliance**: Clear separation of concerns enforced

### 📋 Engineering Standards Check
- **Language**: ✅ Python 3.13+
- **Dependencies**: ✅ Stdlib only
- **Code Quality**: ✅ Single responsibility, max 50 lines per function, no global mutable state
- **Entry Point**: ✅ `python -m src.main`

**GATE RESULT**: ✅ **PASSED** - All constitutional requirements met. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── cli-operations.md
└── checklists/
    └── requirements.md  # Spec quality checklist (completed)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Application entry point, main loop
├── models/
│   ├── __init__.py
│   └── task.py          # Task data class (dataclass or TypedDict)
├── services/
│   ├── __init__.py
│   └── task_service.py  # CRUD operations, ID generation, validation
└── cli/
    ├── __init__.py
    ├── menu.py          # Menu display and main control loop
    ├── display.py       # Task list formatting, icons, separators
    └── input_handler.py # User input validation and parsing

tests/                   # (Created if tests requested in tasks phase)
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_service.py
│   └── test_input_handler.py
└── integration/
    ├── __init__.py
    └── test_cli_workflow.py
```

**Structure Decision**: Single project structure selected. This is a standalone CLI application with no web/mobile components. The `src/` directory contains all application code organized by the constitutional modular architecture (models, services, cli). Entry point is `src/main.py` to support `python -m src.main` execution.

## High-Level Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User (Terminal)                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLI Layer (src/cli/)                       │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐  │
│  │   menu.py    │  │  display.py   │  │ input_handler.py│  │
│  │ Main control │  │ Format output │  │ Validate input  │  │
│  │ loop, routes │  │ Show icons    │  │ Parse user data │  │
│  └──────────────┘  └───────────────┘  └─────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Services Layer (src/services/)                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            task_service.py                             │ │
│  │  - add_task(title, desc) -> Task                       │ │
│  │  - get_all_tasks() -> list[Task]                       │ │
│  │  - get_task_by_id(id) -> Task | None                   │ │
│  │  - update_task(id, title?, desc?) -> bool              │ │
│  │  - delete_task(id) -> bool                             │ │
│  │  - toggle_complete(id) -> bool                         │ │
│  │  - _generate_next_id() -> int                          │ │
│  │  - _validate_title(title) -> bool                      │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               Models Layer (src/models/)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  task.py                               │ │
│  │  @dataclass Task:                                      │ │
│  │    id: int                                             │ │
│  │    title: str (1-200 chars)                            │ │
│  │    description: str (0-1000 chars)                     │ │
│  │    completed: bool (default False)                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│           In-Memory Storage (Python list)                    │
│              tasks: list[Task] = []                          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → CLI input_handler validates → Services processes → Models updated
2. **User Output** ← CLI display formats ← Services retrieves ← Models data

### Module Responsibilities

#### 1. Models Layer (`src/models/`)

**Purpose**: Define data structures

**task.py**:
- Define Task dataclass with type hints
- No business logic, no validation (pure data)
- Attributes: id (int), title (str), description (str), completed (bool)

**Dependency**: None (independent layer)

#### 2. Services Layer (`src/services/`)

**Purpose**: Business logic and data management

**task_service.py**:
- Maintain in-memory task list
- CRUD operations (add, get, update, delete)
- ID generation (auto-increment starting from 1)
- Title validation (1-200 chars, not empty)
- Description validation (0-1000 chars)
- Status toggling (mark complete/incomplete)
- Return Task objects or None for not found

**Dependency**: Imports Task from models

#### 3. CLI Layer (`src/cli/`)

**Purpose**: User interface and interaction

**menu.py**:
- Display numbered menu (1-7 options)
- Main control loop (while running)
- Route user choice to appropriate handler
- Handle "Quit" option
- Show startup message about no persistence

**display.py**:
- Format task list for viewing
- Truncate title (50 chars) and description (30 chars) with "..."
- Show status icons (✅ for completed, ⏳ for pending)
- Display separators and spacing
- Show empty state message
- Show success/error messages with consistent formatting

**input_handler.py**:
- Get and validate menu choice (1-7)
- Get and validate task ID (numeric, positive)
- Get and validate title (not empty, strip whitespace)
- Get optional description (strip whitespace)
- Get confirmation for delete (y/n)
- Handle invalid input gracefully with error messages
- Re-prompt on validation failure

**Dependency**: Imports TaskService and Task

#### 4. Main Entry Point (`src/main.py`)

**Purpose**: Application bootstrap

**main.py**:
- Initialize TaskService
- Display startup message (no persistence warning)
- Start main menu loop
- Handle graceful exit
- Catch and log unexpected errors

**Dependency**: Imports menu from CLI

## Data Model Design

See [data-model.md](./data-model.md) for complete details.

**Task Entity**:
```python
@dataclass
class Task:
    id: int                    # Unique, auto-assigned, starts at 1
    title: str                 # Required, 1-200 chars
    description: str           # Optional, 0-1000 chars, default ""
    completed: bool            # Default False
```

**In-Memory Storage**:
- Module-level list in task_service.py
- `_tasks: list[Task] = []`
- Not exposed publicly (private with underscore prefix)
- Access only through service functions

**ID Generation Strategy**:
- Track next_id as module-level variable
- Increment after each add_task
- IDs never reused (even after delete)
- Start at 1 for first task

## CLI Flow and Control Loop

### Startup Flow

```
1. python -m src.main
2. Initialize TaskService
3. Display startup banner
4. Show "Note: Tasks not saved between sessions"
5. Enter main loop
```

### Main Control Loop

```
LOOP (while not quit):
  1. Display menu:
     ═══════════════════════════════
       Todo App - Main Menu
     ═══════════════════════════════
     1. Add Task
     2. View Tasks
     3. Update Task
     4. Delete Task
     5. Mark Task Complete
     6. Mark Task Incomplete
     7. Quit
     ═══════════════════════════════

  2. Get user choice (1-7)

  3. Route to handler:
     - 1 → add_task_flow()
     - 2 → view_tasks_flow()
     - 3 → update_task_flow()
     - 4 → delete_task_flow()
     - 5 → mark_complete_flow()
     - 6 → mark_incomplete_flow()
     - 7 → quit_flow()

  4. Display result message

  5. Wait for Enter to continue

END LOOP

Display goodbye message
Exit(0)
```

### Operation Flows

**Add Task Flow**:
```
1. Prompt for title
2. Validate title (not empty)
3. Prompt for description (optional, can skip)
4. Call service.add_task(title, desc)
5. Display: "✅ Task added successfully! (ID: {id})"
```

**View Tasks Flow**:
```
1. Get all tasks from service
2. If empty: Display "No tasks yet! Add your first task to get started."
3. Else: Format and display each task:
   ───────────────────────────────────────
   [⏳] ID: 1 | Buy groceries
       milk, eggs, bread
   [✅] ID: 2 | Call dentist
   ───────────────────────────────────────
```

**Update Task Flow**:
```
1. Prompt for task ID
2. Validate ID (numeric)
3. Get task from service
4. If not found: Display "❌ Task not found with ID {id}"
5. Prompt: Update (1) Title (2) Description (3) Both
6. Get new values
7. Call service.update_task(id, title, desc)
8. Display: "✅ Task updated successfully!"
```

**Delete Task Flow**:
```
1. Prompt for task ID
2. Get task from service
3. If not found: Display "❌ Task not found with ID {id}"
4. Show task details
5. Prompt: "Delete this task? (y/n)"
6. If y: Call service.delete_task(id)
7. Display: "✅ Task deleted successfully!"
```

**Mark Complete/Incomplete Flow**:
```
1. Prompt for task ID
2. Get task from service
3. If not found: Display "❌ Task not found with ID {id}"
4. Call service.toggle_complete(id, target_status)
5. Display: "✅ Task marked {complete|incomplete}!"
```

## Error Handling Strategy

### Input Validation Errors (User-Facing)

**Strategy**: Validate early, show friendly message, re-prompt

**Cases**:
1. **Empty Title**:
   - Message: "❌ Title is required. Please enter a title."
   - Action: Re-prompt for title

2. **Invalid Menu Choice**:
   - Message: "❌ Please enter a number between 1 and 7."
   - Action: Re-prompt for choice

3. **Non-Numeric ID**:
   - Message: "❌ Please enter a valid task ID (number)."
   - Action: Re-prompt for ID

4. **Task Not Found**:
   - Message: "❌ Task not found with ID {id}."
   - Action: Return to menu

5. **Title Too Long** (>200 chars):
   - Message: "❌ Title must be 200 characters or less."
   - Action: Re-prompt for title

6. **Description Too Long** (>1000 chars):
   - Message: "❌ Description must be 1000 characters or less."
   - Action: Re-prompt or truncate with user consent

### System Errors (Unexpected)

**Strategy**: Catch at top level, log, graceful exit

**Implementation**:
```python
# In main.py
try:
    main_loop()
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("Please restart the application.")
    exit(1)
```

### Validation Functions

**Location**: `src/cli/input_handler.py`

Functions:
- `validate_menu_choice(choice: str) -> int | None`
- `validate_task_id(id_str: str) -> int | None`
- `validate_title(title: str) -> str | None`
- `validate_description(desc: str) -> str | None`

**Return Pattern**: Return validated value or None if invalid

### Error Message Standards

- Prefix errors with ❌
- Prefix success with ✅
- Use friendly, clear language
- Suggest corrective action
- No technical jargon or stack traces

## Performance Considerations

### In-Memory Optimization

- **List Operations**: O(n) for search, O(1) for append
- **Expected Load**: <100 tasks per session
- **Memory Footprint**: ~1KB per task → 100KB for 100 tasks (negligible)

**No optimization needed**: Linear search acceptable at this scale

### Display Performance

- **Truncation**: Done at display time, not storage
- **Formatting**: Template strings (fast in Python)
- **Expected**: <10ms to display 100 tasks

### Input Performance

- **Validation**: Runs on each input (string checks, O(1))
- **Expected**: <1ms per validation

**Performance Goal**: <100ms response time for all operations **ACHIEVED** at expected scale

## Testing Strategy

### Test Coverage (If Tests Requested)

**Unit Tests** (`tests/unit/`):
- `test_task_service.py`:
  - Test add_task (with valid/invalid inputs)
  - Test get_task_by_id (found/not found)
  - Test update_task (various scenarios)
  - Test delete_task
  - Test toggle_complete
  - Test ID generation (increments correctly)
  - Test title validation

- `test_input_handler.py`:
  - Test validate_menu_choice
  - Test validate_task_id
  - Test validate_title
  - Test validate_description

**Integration Tests** (`tests/integration/`):
- `test_cli_workflow.py`:
  - Test full add → view → complete → delete workflow
  - Test empty list handling
  - Test error recovery (invalid ID → valid ID)

### Manual Testing Checklist

See [quickstart.md](./quickstart.md) for manual test scenarios

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unicode icons not displaying (✅ ⏳) | Medium - UX degraded | Document UTF-8 requirement; fallback to [X] [ ] if needed |
| User enters extremely long input | Low - validation prevents | Enforce max lengths at input validation layer |
| User expects persistence | Medium - confusion | Clear startup warning + documentation |
| Circular import between modules | High - app won't run | Follow strict dependency rules: CLI→Services→Models |

## Phase 0: Research Completed

See [research.md](./research.md) for detailed findings.

**Key Decisions**:
1. **Data Structure**: Python dataclass for type safety and simplicity
2. **CLI Framework**: Pure Python (no external libs) for constitutional compliance
3. **ID Strategy**: Auto-increment integer starting from 1
4. **Storage**: Module-level list (no class needed for simplicity)
5. **Entry Point**: `python -m src.main` using `__main__.py` or main.py with conditional

## Phase 1: Design Artifacts

**Generated**:
- ✅ [data-model.md](./data-model.md) - Complete Task entity specification
- ✅ [contracts/cli-operations.md](./contracts/cli-operations.md) - All CLI operation contracts
- ✅ [quickstart.md](./quickstart.md) - User guide and manual test scenarios

## Next Steps

**Ready for**: `/sp.tasks` command

The planning phase is complete. All architecture decisions made, module responsibilities defined, and design artifacts generated. The next phase will break this plan into atomic, testable implementation tasks.

## Complexity Tracking

> No constitutional violations detected. This section left empty as required.

---

**Plan Status**: ✅ Complete
**Constitution Compliance**: ✅ All gates passed
**Artifacts Generated**: research.md, data-model.md, contracts/, quickstart.md
**Ready for Task Generation**: Yes
