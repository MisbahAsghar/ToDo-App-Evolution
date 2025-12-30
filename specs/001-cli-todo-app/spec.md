# Feature Specification: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Feature: Phase I – In-Memory CLI Todo Application"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)

As a terminal user, I want to add tasks with titles and optional descriptions, then view them in a clear list, so I can track what I need to do.

**Why this priority**: Core functionality that enables the most basic todo list workflow. Without the ability to add and view tasks, the application provides no value.

**Independent Test**: Can be fully tested by launching the app, adding 2-3 tasks with various title/description combinations, viewing the list, and verifying all tasks appear with correct IDs and status icons. Delivers a minimal but functional todo list.

**Acceptance Scenarios**:

1. **Given** the app is running and no tasks exist, **When** I select "Add Task" and enter title "Buy groceries" with description "milk, eggs, bread", **Then** a new task is created with ID 1, incomplete status (⏳), and both title and description are stored
2. **Given** I have added one task, **When** I select "View Tasks", **Then** I see a formatted list showing task ID, title, truncated description, and status icon (⏳ for incomplete)
3. **Given** the app is running and no tasks exist, **When** I select "View Tasks", **Then** I see a friendly message like "No tasks yet! Add your first task to get started."
4. **Given** I'm on the "Add Task" screen, **When** I enter only a title "Call dentist" without a description, **Then** the task is created successfully with just the title
5. **Given** I'm on the "Add Task" screen, **When** I try to submit without entering a title, **Then** I see an error message "Title is required" and the task is not created

---

### User Story 2 - Mark Tasks Complete (Priority: P2)

As a terminal user, I want to mark tasks as complete or incomplete, so I can track my progress and see what's finished.

**Why this priority**: This adds basic task management beyond just creating and viewing. It's the second most important feature for a todo list, but the app is still usable without it.

**Independent Test**: Can be fully tested by adding 2-3 tasks, marking some complete (verify ✅ icon appears), marking some incomplete again (verify ⏳ icon returns), and viewing the list to confirm status changes persist during the session.

**Acceptance Scenarios**:

1. **Given** I have an incomplete task with ID 2, **When** I select "Mark Complete" and enter ID 2, **Then** the task status changes to complete (✅) and I see a success message
2. **Given** I have a completed task with ID 2, **When** I select "Mark Incomplete" and enter ID 2, **Then** the task status changes to incomplete (⏳) and I see a success message
3. **Given** I select "Mark Complete", **When** I enter an ID that doesn't exist (e.g., 999), **Then** I see an error message "Task not found with ID 999" and no changes are made
4. **Given** I select "Mark Complete", **When** I enter invalid input like "abc", **Then** I see an error message "Please enter a valid task ID (number)" and I'm prompted to try again

---

### User Story 3 - Update Task Details (Priority: P3)

As a terminal user, I want to update the title or description of existing tasks, so I can fix mistakes or add more information.

**Why this priority**: Nice to have for fixing errors, but users can work around this by deleting and recreating tasks. Less critical than core add/view/complete functionality.

**Independent Test**: Can be fully tested by adding a task, updating its title only, updating its description only, updating both, and verifying changes appear in the task list. The app remains functional even without this feature.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1 (title: "Old title", description: "Old desc"), **When** I select "Update Task", enter ID 1, and provide new title "New title", **Then** the task title is updated and I see a confirmation message
2. **Given** I have a task with ID 1, **When** I select "Update Task", enter ID 1, choose to update description, and enter "New description", **Then** only the description is updated
3. **Given** I have a task with ID 1, **When** I select "Update Task", enter ID 1, and update both title and description, **Then** both fields are updated and displayed correctly in the task list
4. **Given** I select "Update Task", **When** I enter a task ID that doesn't exist, **Then** I see an error message "Task not found" and no changes are made
5. **Given** I'm updating a task, **When** I try to set the title to empty, **Then** I see an error "Title cannot be empty" and the update is not applied

---

### User Story 4 - Delete Tasks (Priority: P4)

As a terminal user, I want to delete tasks I no longer need, so I can keep my list clean and focused.

**Why this priority**: Useful for list maintenance, but not critical for basic todo functionality. Users can simply ignore completed or unwanted tasks.

**Independent Test**: Can be fully tested by adding 3 tasks, deleting one by ID, confirming the task is removed from the list, and verifying the deletion confirmation prompt works correctly. The app delivers full value without this feature.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 3, **When** I select "Delete Task", enter ID 3, and confirm deletion, **Then** the task is permanently removed from the list
2. **Given** I select "Delete Task" and enter a valid ID, **When** the confirmation prompt appears and I choose "No" or "Cancel", **Then** the task is NOT deleted and remains in the list
3. **Given** I select "Delete Task", **When** I enter an ID that doesn't exist, **Then** I see an error message "Task not found with ID [ID]" and no deletion occurs
4. **Given** I have 3 tasks with IDs 1, 2, 3, **When** I delete task 2, **Then** tasks 1 and 3 remain with their original IDs (IDs are not reassigned)

---

### Edge Cases

- What happens when the task list is empty and user tries to mark complete, update, or delete?
  - System should display a friendly message like "No tasks available. Add a task first."
- How does the system handle very long titles or descriptions?
  - Titles display up to 50 characters in list view, descriptions up to 30 characters, both with "..." truncation if longer
- What happens when user enters non-numeric input for task IDs?
  - System validates input and shows error: "Please enter a valid task ID (number)"
- How does the system handle maximum task capacity?
  - In-memory storage has no enforced limit for Phase I; Python list can grow as needed within system memory
- What happens when user quits and restarts the app?
  - All tasks are lost (in-memory only, no persistence). User should be informed on first startup: "Note: Tasks are not saved between sessions"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new tasks with a required title (string, 1-200 characters)
- **FR-002**: System MUST allow users to optionally add a description to tasks (string, 0-1000 characters)
- **FR-003**: System MUST assign a unique, auto-incrementing numeric ID to each task (starting from 1)
- **FR-004**: System MUST store all tasks in memory during the session
- **FR-005**: System MUST display all tasks in a formatted list showing ID, title (truncated to 50 chars if needed), description preview (truncated to 30 chars if needed), and status icon
- **FR-006**: System MUST use ✅ icon to indicate completed tasks and ⏳ icon to indicate incomplete tasks
- **FR-007**: System MUST allow users to mark any task as complete or incomplete by its ID
- **FR-008**: System MUST allow users to update the title and/or description of any task by its ID
- **FR-009**: System MUST allow users to delete any task by its ID
- **FR-010**: System MUST show a confirmation prompt before deleting a task
- **FR-011**: System MUST display friendly error messages for invalid inputs (empty title, non-existent ID, non-numeric ID)
- **FR-012**: System MUST show a friendly message when viewing an empty task list
- **FR-013**: System MUST present a numbered menu of operations (Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete, Quit)
- **FR-014**: System MUST validate all user inputs before processing
- **FR-015**: System MUST run via the command `python -m src.main`
- **FR-016**: System MUST clear/discard all tasks when the application exits (no persistence)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item with attributes:
  - ID (unique numeric identifier, auto-assigned)
  - Title (required text, 1-200 characters)
  - Description (optional text, 0-1000 characters)
  - Status (boolean: complete or incomplete, defaults to incomplete)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 10 seconds (from menu selection to confirmation)
- **SC-002**: Users can view their complete task list in under 2 seconds
- **SC-003**: The task list displays with clear visual distinction between complete (✅) and incomplete (⏳) tasks
- **SC-004**: 100% of invalid inputs (empty title, non-existent ID, non-numeric ID) result in clear, helpful error messages
- **SC-005**: Users receive confirmation messages for all successful operations (add, update, delete, mark complete/incomplete)
- **SC-006**: The menu is numbered and self-explanatory, requiring no external documentation
- **SC-007**: The application can handle at least 100 tasks in memory without noticeable performance degradation
- **SC-008**: Users can complete the full workflow (add task → view tasks → mark complete → delete task) in under 1 minute on first use

## Assumptions

- Users have Python 3.13+ installed and can run command-line applications
- Users understand that in-memory storage means tasks will be lost on exit (this is acceptable for Phase I)
- Users are comfortable with keyboard input and numbered menu selection
- Users will run the application in a terminal with UTF-8 support (for status icons ✅ ⏳)
- Tasks are personal/single-user; no multi-user or sharing requirements
- No authentication or authorization required for Phase I
- No networking or external API integrations required
- Application runs on a single machine (localhost only)

## Out of Scope

- Task priorities or importance levels
- Tags, categories, or labels
- Due dates, reminders, or time tracking
- File storage or database persistence
- Web interface or API
- AI features or natural language processing
- Multi-user support or task sharing
- Search or filter functionality
- Task sorting (beyond display order by ID)
- Export/import functionality
- Undo/redo operations
- Task history or audit trail
