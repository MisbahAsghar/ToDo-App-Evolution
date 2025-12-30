# Research: Phase I – In-Memory CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app
**Purpose**: Technical research and decision-making for implementation approach

## Research Questions

Based on Technical Context unknowns and architectural decisions needed:

1. What Python data structure should we use for the Task entity?
2. How should we structure the CLI application (framework vs pure Python)?
3. What's the best strategy for ID generation in-memory?
4. How should we organize in-memory storage (class vs module-level)?
5. How should we implement `python -m src.main` entry point?

---

## Research Finding 1: Task Entity Data Structure

### Question
What Python data structure should we use for the Task entity?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Dictionary** | Simple, no imports | No type safety, error-prone |
| **NamedTuple** | Lightweight, immutable | Immutable (bad for updates) |
| **@dataclass** | Type hints, mutable, clean | Requires Python 3.7+ (we have 3.13+) |
| **TypedDict** | Type hints, dict-like | No runtime validation |
| **Custom class** | Full control | Overengineering for simple data |

### Decision

**Selected**: `@dataclass` from Python's `dataclasses` module

### Rationale

1. **Type Safety**: Enforces type hints at IDE/linter level (constitutional requirement IV)
2. **Simplicity**: Auto-generates `__init__`, `__repr__`, `__eq__` (constitutional requirement II)
3. **Mutability**: Supports updates to title/description/status
4. **Standard Library**: No external dependencies (constitutional requirement)
5. **Readability**: Clean, declarative syntax

Example:
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

### Alternatives Rejected

- **Dictionary**: Lacks type safety (fails constitutional requirement IV)
- **NamedTuple**: Immutability prevents updates (violates FR-008)
- **Custom class**: Unnecessary boilerplate (violates simplicity principle II)

---

## Research Finding 2: CLI Application Structure

### Question
How should we structure the CLI application (framework vs pure Python)?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Click** | Rich features, widely used | External dependency |
| **Typer** | Modern, type-safe | External dependency |
| **argparse** | Stdlib, mature | Not menu-driven (arg-based) |
| **cmd module** | Stdlib, REPL-style | Different UX pattern |
| **Pure Python (input/print)** | No dependencies, full control | Manual work |

### Decision

**Selected**: Pure Python with `input()` and `print()` (stdlib)

### Rationale

1. **Constitutional Compliance**: No external dependencies allowed (principle II, engineering standards)
2. **Full Control**: Numbered menu implementation as specified (principle III)
3. **Simplicity**: Straightforward for Phase I scope (principle II)
4. **Learning Value**: Clear understanding of CLI mechanics
5. **Spec Alignment**: Menu-driven interface (FR-013) not argument-based

Implementation approach:
```python
def display_menu():
    print("═══════════════════════════════")
    print("  Todo App - Main Menu")
    print("═══════════════════════════════")
    print("1. Add Task")
    # ... etc

choice = input("Enter choice (1-7): ")
```

### Alternatives Rejected

- **Click/Typer**: External dependencies (constitutional violation)
- **argparse**: Argument-based, not menu-driven (doesn't match spec UX)
- **cmd module**: REPL pattern doesn't match numbered menu requirement

---

## Research Finding 3: ID Generation Strategy

### Question
What's the best strategy for generating unique task IDs in-memory?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Auto-increment counter** | Simple, predictable | None for in-memory |
| **UUID** | Globally unique | Overkill, not user-friendly (spec says numeric) |
| **Hash-based** | Deterministic | Complex, unnecessary |
| **Timestamp** | No collision tracking | Not user-friendly as ID |

### Decision

**Selected**: Auto-increment integer counter starting from 1

### Rationale

1. **Spec Compliance**: FR-003 specifies "unique, auto-incrementing numeric ID"
2. **User-Friendly**: Simple sequential numbers (1, 2, 3...)
3. **Simplicity**: Single integer counter (principle II)
4. **No Persistence**: No need for globally unique IDs since in-memory only
5. **Performance**: O(1) generation time

Implementation approach:
```python
# In task_service.py (module level)
_next_id: int = 1
_tasks: list[Task] = []

def add_task(title: str, description: str = "") -> Task:
    global _next_id
    task = Task(id=_next_id, title=title, description=description)
    _tasks.append(task)
    _next_id += 1
    return task
```

**ID Reuse Policy**: IDs are never reused, even after deletion (maintains stability for user references during session)

### Alternatives Rejected

- **UUID**: Not numeric, overkill for in-memory (spec violation)
- **Hash-based**: Complex, violates simplicity principle
- **Timestamp**: Not sequential, poor UX for small lists

---

## Research Finding 4: In-Memory Storage Organization

### Question
How should we organize in-memory storage (class vs module-level)?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Module-level list** | Simple, direct access | Global state |
| **TaskManager class** | Encapsulation, testable | Adds abstraction layer |
| **Singleton class** | OOP pattern | Overengineering for Phase I |
| **Service functions + module state** | Balance of simplicity & structure | "Hybrid" approach |

### Decision

**Selected**: Service functions with module-level private state

### Rationale

1. **Simplicity**: No unnecessary class abstraction (principle II)
2. **Encapsulation**: Private module variables (`_tasks`, `_next_id`) not exported
3. **Functional API**: Public functions provide clean interface
4. **Testable**: Can test functions in isolation
5. **Constitutional Compliance**: Avoids overengineering (principle II)

Implementation approach:
```python
# task_service.py
_tasks: list[Task] = []
_next_id: int = 1

def add_task(title: str, description: str = "") -> Task:
    # ... implementation

def get_all_tasks() -> list[Task]:
    return _tasks.copy()  # Return copy to prevent external mutation

def get_task_by_id(task_id: int) -> Task | None:
    # ... implementation
```

**Why not a class**: For Phase I, we have single-session, single-user storage. A class would add ceremony without benefit. Module-level state is simpler and sufficient.

### Alternatives Rejected

- **TaskManager class**: Unnecessary abstraction (violates principle II)
- **Singleton**: Design pattern overkill (violates principle II)
- **Bare module list**: Lacks encapsulation (poor API design)

---

## Research Finding 5: Entry Point Implementation

### Question
How should we implement `python -m src.main` entry point?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **`if __name__ == "__main__"` in main.py** | Standard, simple | Requires `python src/main.py` (wrong path) |
| **`__main__.py` in src/** | Proper `-m` support | Extra file |
| **main() function + __main__ check** | Standard pattern | Need to handle both cases |

### Decision

**Selected**: `main()` function in `src/main.py` with `if __name__ == "__main__"` guard

### Rationale

1. **Spec Compliance**: FR-015 requires `python -m src.main`
2. **Standard Pattern**: Widely used Python convention
3. **Simplicity**: Single file, no `__main__.py` needed
4. **Package Support**: Works when src is treated as package

Implementation:
```python
# src/main.py
from cli.menu import run_menu

def main() -> None:
    """Application entry point."""
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please restart the application.")
        exit(1)

if __name__ == "__main__":
    main()
```

**Package structure requirement**: Requires `src/__init__.py` to treat `src/` as a package.

**How it works**: When running `python -m src.main`, Python:
1. Treats `src` as a package (finds `src/__init__.py`)
2. Imports `src.main` module
3. Runs `if __name__ == "__main__"` block (since `-m` sets `__name__` to `"__main__"`)

### Alternatives Rejected

- **`__main__.py`**: Adds extra file without clear benefit
- **Direct script**: Doesn't support `-m` flag as specified

---

## Additional Technical Decisions

### Unicode Support

**Decision**: Use UTF-8 emoji icons (✅ ⏳) directly in strings

**Rationale**:
- Modern terminals support UTF-8 by default
- Assumption in spec: "UTF-8 terminal support"
- Simpler than ASCII fallback logic for Phase I
- Document requirement in quickstart.md

**Risk Mitigation**: If icons don't display, document fallback to `[X]` `[ ]` in future phases

### Input Validation Approach

**Decision**: Validate in CLI layer (`input_handler.py`), not in service layer

**Rationale**:
- Separation of concerns: UI handles UI validation, services handle business rules
- Error messages are UI concern (principle V: modular architecture)
- Services trust CLI to send valid data
- Simplifies service layer (principle II)

**Service-level validation**: Only critical business rules (title length, ID existence)

### Error Message Format

**Decision**: Standardize on emoji prefixes (✅ success, ❌ error)

**Rationale**:
- Visual consistency (principle III: excellent CLI UX)
- Quick visual scanning
- Friendly, approachable (principle III)

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.13+ | Constitutional requirement |
| Data Structure | @dataclass | Type safety + simplicity |
| CLI Framework | Pure Python (input/print) | No dependencies, full control |
| Storage | Module-level list | Simple, sufficient for Phase I |
| ID Generation | Auto-increment int | User-friendly, spec-compliant |
| Entry Point | `python -m src.main` | Spec requirement |
| Type Hints | Full coverage | Constitutional requirement IV |
| Testing | unittest/pytest | stdlib or common tool (TBD in tasks) |

---

## Dependencies

**External**: None (stdlib only)

**Python Modules Used** (all stdlib):
- `dataclasses` - Task entity
- `typing` - Type hints (e.g., `list[Task]`, `| None`)
- `sys` - Exit codes (if needed)

---

## Open Questions

None - all technical unknowns resolved.

---

## Research Status

✅ **Complete** - All architectural decisions made, ready for Phase 1 (design artifacts)

**Next Phase**: Generate data-model.md, contracts/, and quickstart.md
