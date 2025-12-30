# Quickstart Guide: Phase I – In-Memory CLI Todo Application

**Date**: 2025-12-31
**Feature**: 001-cli-todo-app
**Purpose**: User guide and manual testing scenarios

## Overview

The Phase I Todo CLI is an in-memory task management application for terminal users. This guide will help you run, use, and test the application.

---

## Prerequisites

### System Requirements

- **Python**: 3.13 or higher
- **Terminal**: UTF-8 support (for status icons ✅ ⏳)
- **Operating System**: Windows, macOS, or Linux

### Check Python Version

```bash
python --version
# Should output: Python 3.13.x or higher
```

If you don't have Python 3.13+, download it from [python.org](https://www.python.org/downloads/)

---

## Installation

### Clone Repository (if applicable)

```bash
cd path/to/hackathon-2
```

### Verify Project Structure

```bash
ls -la src/
# Should show: models/, services/, cli/, main.py
```

---

## Running the Application

### Start the App

```bash
python -m src.main
```

**Expected Output**:
```
═══════════════════════════════════════
  Welcome to Phase I Todo App!
═══════════════════════════════════════

⚠️  Note: Tasks are not saved between sessions.
    All data will be lost when you quit.

═══════════════════════════════════════
  Todo App - Main Menu
═══════════════════════════════════════
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Quit
═══════════════════════════════════════
Enter choice (1-7):
```

### Exit the App

- Select option `7. Quit` from the menu
- Or press `Ctrl+C` at any time

---

## User Guide

### 1. Add a Task

**Purpose**: Create a new task with title and optional description

**Steps**:
1. Select `1` from main menu
2. Enter task title (required, 1-200 characters)
3. Enter description (optional, press Enter to skip, max 1000 characters)
4. Task created with unique ID and incomplete status (⏳)

**Example**:
```
Enter choice (1-7): 1

Enter title: Buy groceries
Enter description (optional, press Enter to skip): milk, eggs, bread

✅ Task added successfully! (ID: 1)

Press Enter to continue...
```

**Tips**:
- Title cannot be empty
- Leading/trailing spaces are automatically removed
- If title or description is too long, you'll be prompted to re-enter

---

### 2. View All Tasks

**Purpose**: See all your tasks with their status

**Steps**:
1. Select `2` from main menu
2. View formatted task list

**Example (with tasks)**:
```
Enter choice (1-7): 2

───────────────────────────────────────
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread
[✅] ID: 2 | Call dentist
[⏳] ID: 3 | Research Python dataclasses
    For the todo app project
───────────────────────────────────────

Press Enter to continue...
```

**Example (empty list)**:
```
Enter choice (1-7): 2

No tasks yet! Add your first task to get started.

Press Enter to continue...
```

**Status Icons**:
- ⏳ = Incomplete (pending)
- ✅ = Complete (done)

**Truncation**:
- Titles longer than 50 characters display with "..."
- Descriptions longer than 30 characters display with "..."
- Full text is preserved and can be viewed during updates

---

### 3. Update a Task

**Purpose**: Change the title or description of an existing task

**Steps**:
1. Select `3` from main menu
2. Enter task ID
3. Choose what to update:
   - `1` = Title only
   - `2` = Description only
   - `3` = Both title and description
4. Enter new values
5. Task updated

**Example**:
```
Enter choice (1-7): 3

Enter task ID: 1

Current task:
[⏳] ID: 1 | Buy groceries
    milk, eggs, bread

Update: (1) Title  (2) Description  (3) Both
Enter choice: 1

Enter new title: Buy groceries and household items

✅ Task updated successfully!

Press Enter to continue...
```

**Error Handling**:
- If ID doesn't exist: "❌ Task not found with ID {id}"
- If new title is empty: "❌ Title is required"
- If new values are too long: "❌ Title/Description must be X characters or less"

---

### 4. Delete a Task

**Purpose**: Remove a task you no longer need

**Steps**:
1. Select `4` from main menu
2. Enter task ID
3. Review task details
4. Confirm deletion (y/n)
5. Task deleted if confirmed

**Example**:
```
Enter choice (1-7): 4

Enter task ID: 2

You are about to delete:
[✅] ID: 2 | Call dentist

Delete this task? (y/n): y

✅ Task deleted successfully!

Press Enter to continue...
```

**Cancellation**:
```
Delete this task? (y/n): n

Deletion cancelled.

Press Enter to continue...
```

**Important**: Deleted task IDs are never reused. If you delete task #2, the next new task will get the next available ID (e.g., #4 if #3 exists).

---

### 5. Mark Task Complete

**Purpose**: Mark a task as done

**Steps**:
1. Select `5` from main menu
2. Enter task ID
3. Task marked complete (✅)

**Example**:
```
Enter choice (1-7): 5

Enter task ID: 1

✅ Task marked complete!

Press Enter to continue...
```

**Effect**: Task icon changes from ⏳ to ✅ in task list

---

### 6. Mark Task Incomplete

**Purpose**: Mark a completed task as not done (undo completion)

**Steps**:
1. Select `6` from main menu
2. Enter task ID
3. Task marked incomplete (⏳)

**Example**:
```
Enter choice (1-7): 6

Enter task ID: 1

✅ Task marked incomplete!

Press Enter to continue...
```

**Effect**: Task icon changes from ✅ to ⏳ in task list

---

### 7. Quit

**Purpose**: Exit the application

**Steps**:
1. Select `7` from main menu
2. Application exits

**Example**:
```
Enter choice (1-7): 7

Thank you for using Phase I Todo App!
All tasks have been cleared.
Goodbye!
```

**Warning**: All tasks are lost when you quit (no persistence in Phase I)

---

## Manual Testing Scenarios

### Test Scenario 1: Basic Add and View Workflow

**Objective**: Verify basic task creation and viewing

**Steps**:
1. Start app: `python -m src.main`
2. Add task: title="Buy milk", description="2% or whole"
3. Add task: title="Call dentist", description=""
4. View tasks
5. Verify both tasks appear with correct IDs and ⏳ icons

**Expected Result**:
```
[⏳] ID: 1 | Buy milk
    2% or whole
[⏳] ID: 2 | Call dentist
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 2: Mark Task Complete

**Objective**: Verify task completion status change

**Steps**:
1. (Continuing from Scenario 1)
2. Mark task 1 complete
3. View tasks
4. Verify task 1 shows ✅ icon

**Expected Result**:
```
[✅] ID: 1 | Buy milk
    2% or whole
[⏳] ID: 2 | Call dentist
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 3: Update Task

**Objective**: Verify task updates work correctly

**Steps**:
1. (Continuing from previous)
2. Update task 2: change title to "Call dentist for appointment"
3. View tasks
4. Verify task 2 has new title

**Expected Result**:
```
[✅] ID: 1 | Buy milk
    2% or whole
[⏳] ID: 2 | Call dentist for appointment
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 4: Delete Task

**Objective**: Verify task deletion works correctly

**Steps**:
1. (Continuing from previous)
2. Delete task 1 (confirm with 'y')
3. View tasks
4. Verify only task 2 remains
5. Add new task: title="Test ID increment"
6. Verify new task gets ID 3 (not reusing ID 1)

**Expected Result**:
```
[⏳] ID: 2 | Call dentist for appointment
[⏳] ID: 3 | Test ID increment
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 5: Mark Incomplete

**Objective**: Verify completed tasks can be marked incomplete

**Steps**:
1. Mark task 2 complete
2. View tasks (verify ✅)
3. Mark task 2 incomplete
4. View tasks (verify ⏳)

**Expected Result**: Task 2 icon changes from ✅ to ⏳

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 6: Empty List Handling

**Objective**: Verify empty list shows friendly message

**Steps**:
1. Start fresh app (or delete all tasks)
2. Select "View Tasks"
3. Verify friendly empty state message

**Expected Result**:
```
No tasks yet! Add your first task to get started.
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 7: Input Validation - Empty Title

**Objective**: Verify empty titles are rejected

**Steps**:
1. Select "Add Task"
2. Press Enter without entering title
3. Verify error message
4. Enter valid title
5. Verify task created

**Expected Result**: Error "❌ Title is required. Please enter a title." then re-prompt

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 8: Input Validation - Invalid Task ID

**Objective**: Verify invalid task IDs are handled

**Steps**:
1. Select "Update Task"
2. Enter ID "abc" (non-numeric)
3. Verify error message
4. Enter ID 999 (doesn't exist)
5. Verify error message

**Expected Results**:
- Non-numeric: "❌ Please enter a valid task ID (number)."
- Not found: "❌ Task not found with ID 999."

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 9: Long Title Truncation

**Objective**: Verify long titles are truncated in display

**Steps**:
1. Add task with title: "This is an extremely long title that definitely exceeds the fifty character limit for display"
2. View tasks
3. Verify title is truncated to 50 chars with "..."

**Expected Result**:
```
[⏳] ID: X | This is an extremely long title that definitely...
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 10: Long Description Truncation

**Objective**: Verify long descriptions are truncated in display

**Steps**:
1. Add task with description: "This is a very long description that will exceed thirty characters"
2. View tasks
3. Verify description is truncated to 30 chars with "..."

**Expected Result**:
```
[⏳] ID: X | Task title
    This is a very long descript...
```

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 11: Delete Confirmation Cancel

**Objective**: Verify deletion can be cancelled

**Steps**:
1. Add a task
2. Select "Delete Task"
3. Enter task ID
4. Enter 'n' when asked to confirm
5. View tasks
6. Verify task still exists

**Expected Result**: "Deletion cancelled." and task remains in list

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 12: Invalid Menu Choice

**Objective**: Verify invalid menu choices are rejected

**Steps**:
1. At main menu, enter "0"
2. Verify error message
3. At main menu, enter "8"
4. Verify error message
5. At main menu, enter "abc"
6. Verify error message

**Expected Result**: "❌ Please enter a number between 1 and 7." for all cases

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 13: Full Workflow (MVP)

**Objective**: Complete end-to-end test of all features

**Steps**:
1. Start app
2. Add 3 tasks
3. View tasks
4. Mark task 2 complete
5. Update task 1 (title)
6. Delete task 3
7. Mark task 2 incomplete
8. View tasks
9. Quit

**Expected Result**: All operations succeed, final list shows tasks 1 and 2

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 14: Title Length Validation (200 chars)

**Objective**: Verify 200 char title limit

**Steps**:
1. Add task with exactly 200 char title (generate programmatically or count)
2. Verify task created successfully
3. Add task with 201 char title
4. Verify error message and re-prompt

**Expected Result**: 200 chars accepted, 201 chars rejected

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

### Test Scenario 15: Description Length Validation (1000 chars)

**Objective**: Verify 1000 char description limit

**Steps**:
1. Add task with exactly 1000 char description
2. Verify task created successfully
3. Add task with 1001 char description
4. Verify error message and re-prompt

**Expected Result**: 1000 chars accepted, 1001 chars rejected

**Status**: ⬜ Not Tested | ⬜ Pass | ⬜ Fail

---

## Troubleshooting

### Icons Not Displaying Correctly

**Problem**: ✅ and ⏳ appear as boxes or question marks

**Solution**:
1. Verify terminal supports UTF-8:
   ```bash
   echo $LANG  # Should include UTF-8
   ```
2. Try a different terminal (iTerm2, Windows Terminal, GNOME Terminal)
3. Update terminal font to one with emoji support

**Workaround**: Future phase can add ASCII fallback ([X] and [ ])

---

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
1. Ensure you're in the project root directory (hackathon-2/)
2. Verify `src/__init__.py` exists
3. Run with `-m` flag: `python -m src.main` (NOT `python src/main.py`)

---

### Python Version Too Old

**Problem**: `SyntaxError` or type hint errors

**Solution**:
1. Check Python version: `python --version`
2. Install Python 3.13+ from python.org
3. Use specific Python version: `python3.13 -m src.main`

---

### Unexpected Crash

**Problem**: App exits with error message

**Solution**:
1. Note the error message
2. Restart the app: `python -m src.main`
3. If error persists, report issue with steps to reproduce

---

## Performance Expectations

Based on spec requirements:

| Operation | Expected Time | Performance Goal |
|-----------|---------------|------------------|
| Add task | < 10 seconds | SC-001 |
| View tasks | < 2 seconds | SC-002 |
| Update task | < 15 seconds | (not specified) |
| Delete task | < 15 seconds | (not specified) |
| Mark complete | < 5 seconds | (not specified) |
| Full workflow | < 1 minute | SC-008 |

**Scale**: App should handle 100+ tasks without lag (SC-007)

---

## Known Limitations (By Design)

1. **No Persistence**: Tasks are lost when app closes (per spec FR-016)
2. **Single User**: No multi-user or sharing features
3. **No Priorities**: All tasks have equal priority
4. **No Due Dates**: No deadline tracking
5. **No Search**: Must view all tasks to find specific one
6. **No Sorting**: Tasks displayed in ID order only
7. **No Undo**: Deletions and updates are permanent (for the session)

These are Phase I constraints per the constitution (Principle II: Simplicity First)

---

## Next Steps

After completing manual testing:
- Proceed to `/sp.tasks` to generate implementation tasks
- Execute `/sp.implement` to build the application
- Re-run these test scenarios to verify implementation

---

## Support

For issues or questions:
- Review [plan.md](./plan.md) for architecture details
- Review [data-model.md](./data-model.md) for entity definitions
- Review [contracts/cli-operations.md](./contracts/cli-operations.md) for operation specs

---

**Quickstart Guide Status**: ✅ Complete

**Ready for**: Task generation (`/sp.tasks`)
