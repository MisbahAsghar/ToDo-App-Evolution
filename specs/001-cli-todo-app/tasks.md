---
description: "Task list for Phase I CLI Todo Application implementation"
---

# Tasks: Phase I – In-Memory CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Not requested in feature specification - tasks below focus on implementation only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create src/ directory structure (src/models/, src/services/, src/cli/)
- [x] T002 [P] Create src/__init__.py to make src a package
- [x] T003 [P] Create src/models/__init__.py
- [x] T004 [P] Create src/services/__init__.py
- [x] T005 [P] Create src/cli/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create Task dataclass in src/models/task.py with id, title, description, completed fields
- [x] T007 Initialize in-memory storage in src/services/task_service.py (_tasks list, _next_id counter)
- [x] T008 [P] Implement add_task(title, description) function in src/services/task_service.py
- [x] T009 [P] Implement get_all_tasks() function in src/services/task_service.py
- [x] T010 [P] Implement get_task_by_id(task_id) function in src/services/task_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and description, then view them in a formatted list

**Independent Test**: Launch app, add 2-3 tasks with various title/description combinations, view list, verify all tasks appear with correct IDs and status icons (⏳)

### Implementation for User Story 1

- [x] T011 [P] [US1] Create get_status_icon(completed) function in src/cli/display.py
- [x] T012 [P] [US1] Create format_single_task(task) function in src/cli/display.py
- [x] T013 [US1] Create format_task_list(tasks) function in src/cli/display.py (depends on T011, T012)
- [x] T014 [P] [US1] Create show_success(message) function in src/cli/display.py
- [x] T015 [P] [US1] Create show_error(message) function in src/cli/display.py
- [x] T016 [P] [US1] Create get_title(prompt) validation function in src/cli/input_handler.py
- [x] T017 [P] [US1] Create get_description(prompt) validation function in src/cli/input_handler.py
- [x] T018 [US1] Implement add_task_flow() in src/cli/menu.py using input_handler and task_service
- [x] T019 [US1] Implement view_tasks_flow() in src/cli/menu.py using display and task_service
- [x] T020 [US1] Create display_menu() function in src/cli/menu.py
- [x] T021 [US1] Create get_menu_choice() function in src/cli/input_handler.py
- [x] T022 [US1] Implement run_menu() main loop in src/cli/menu.py with routing for options 1, 2, and 7
- [x] T023 [US1] Create main() function in src/main.py with startup banner and error handling
- [x] T024 [US1] Add if __name__ == "__main__": main() guard to src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP delivered!)

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Add 2-3 tasks, mark some complete (verify ✅ icon), mark some incomplete (verify ⏳ icon), view list to confirm status changes persist

### Implementation for User Story 2

- [x] T025 [P] [US2] Implement toggle_complete(task_id, target_status) function in src/services/task_service.py
- [x] T026 [P] [US2] Create get_task_id(prompt) validation function in src/cli/input_handler.py
- [x] T027 [US2] Implement mark_complete_flow() in src/cli/menu.py using input_handler and task_service
- [x] T028 [US2] Implement mark_incomplete_flow() in src/cli/menu.py using input_handler and task_service
- [x] T029 [US2] Add routing for menu options 5 and 6 to run_menu() in src/cli/menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update title or description of existing tasks to fix mistakes or add information

**Independent Test**: Add a task, update its title only, update its description only, update both, verify changes appear in task list

### Implementation for User Story 3

- [x] T030 [P] [US3] Implement update_task(task_id, title, description) function in src/services/task_service.py
- [x] T031 [US3] Implement update_task_flow() in src/cli/menu.py with sub-menu for title/desc/both options
- [x] T032 [US3] Add routing for menu option 3 to run_menu() in src/cli/menu.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks they no longer need to keep list clean

**Independent Test**: Add 3 tasks, delete one by ID, confirm task removed from list, verify deletion confirmation prompt works

### Implementation for User Story 4

- [x] T033 [P] [US4] Implement delete_task(task_id) function in src/services/task_service.py
- [x] T034 [P] [US4] Create get_confirmation(prompt) function in src/cli/input_handler.py
- [x] T035 [US4] Implement delete_task_flow() in src/cli/menu.py with confirmation prompt
- [x] T036 [US4] Add routing for menu option 4 to run_menu() in src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 Add visual separators (═══) to menu display in src/cli/menu.py
- [x] T038 Add "Tasks not saved between sessions" warning to startup banner in src/main.py
- [x] T039 Add "Press Enter to continue..." prompts after each operation in src/cli/menu.py
- [x] T040 Add goodbye message to quit flow in src/cli/menu.py
- [x] T041 Verify title truncation (50 chars) in format_single_task() in src/cli/display.py
- [x] T042 Verify description truncation (30 chars) in format_single_task() in src/cli/display.py
- [x] T043 Add empty list message handling in format_task_list() in src/cli/display.py
- [x] T044 Test full application flow per quickstart.md manual test scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 foundation but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses same input/display functions as US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independently testable

**Note**: While US2, US3, US4 build on the CLI framework established in US1, each provides independent value and can be tested standalone.

### Within Each User Story

- Tasks marked [P] can run in parallel (different files, no dependencies)
- Non-parallel tasks must run sequentially in order shown
- Display functions before CLI flows
- Input validators before flows that use them
- Service functions before CLI flows that call them

### Parallel Opportunities

- **Setup (Phase 1)**: All __init__.py files (T002-T005) can be created in parallel
- **Foundational (Phase 2)**: Task model (T006) parallel with service initialization (T007); add/get functions (T008-T010) parallel
- **User Story 1**: Display functions (T011, T012, T014, T015) and input functions (T016, T017) can run in parallel
- **User Story 2**: toggle_complete (T025) and get_task_id (T026) can run in parallel
- **User Story 3**: update_task (T030) is standalone (can start immediately after Foundational)
- **User Story 4**: delete_task (T033) and get_confirmation (T034) can run in parallel
- **Different user stories**: US2, US3, US4 can be worked on in parallel by different team members after US1 establishes CLI framework

---

## Parallel Example: Foundational Phase

```bash
# Launch these tasks together:
Task: "Create Task dataclass in src/models/task.py" (T006)
Task: "Initialize storage in src/services/task_service.py" (T007)

# Then launch these together:
Task: "Implement add_task() in src/services/task_service.py" (T008)
Task: "Implement get_all_tasks() in src/services/task_service.py" (T009)
Task: "Implement get_task_by_id() in src/services/task_service.py" (T010)
```

---

## Parallel Example: User Story 1

```bash
# Launch all display functions together:
Task: "Create get_status_icon() in src/cli/display.py" (T011)
Task: "Create format_single_task() in src/cli/display.py" (T012)
Task: "Create show_success() in src/cli/display.py" (T014)
Task: "Create show_error() in src/cli/display.py" (T015)

# Launch all input validators together:
Task: "Create get_title() in src/cli/input_handler.py" (T016)
Task: "Create get_description() in src/cli/input_handler.py" (T017)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T010) - CRITICAL BLOCKING PHASE
3. Complete Phase 3: User Story 1 (T011-T024)
4. **STOP and VALIDATE**: Test User Story 1 independently per quickstart.md scenarios
5. Run the app: `python -m src.main`
6. Verify: Add tasks, view tasks, quit
7. **MVP DELIVERED** - Basic working todo app!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T011-T024) → Test independently → **MVP DELIVERED**
3. Add User Story 2 (T025-T029) → Test independently → Mark complete/incomplete works
4. Add User Story 3 (T030-T032) → Test independently → Update functionality works
5. Add User Story 4 (T033-T036) → Test independently → Delete functionality works
6. Add Polish (T037-T044) → Full feature set complete
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T010)
2. Once Foundational is done:
   - Developer A: User Story 1 (T011-T024)
   - Developer B: User Story 2 (T025-T029) - can start after US1 establishes CLI framework
   - Developer C: User Story 3 (T030-T032) - can start after US1 establishes CLI framework
   - Developer D: User Story 4 (T033-T036) - can start after US1 establishes CLI framework
3. Stories complete and integrate independently
4. Team completes Polish together (T037-T044)

**Note**: In practice, US1 should complete first to establish the CLI framework (menu, display, input patterns) that US2-4 build upon.

---

## Task Summary

**Total Tasks**: 44

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 5 tasks
- Phase 3 (US1 - Add/View): 14 tasks
- Phase 4 (US2 - Mark Complete): 5 tasks
- Phase 5 (US3 - Update): 3 tasks
- Phase 6 (US4 - Delete): 4 tasks
- Phase 7 (Polish): 8 tasks

**By User Story**:
- US1 (Add and View Tasks - P1): 14 tasks → **MVP**
- US2 (Mark Tasks Complete - P2): 5 tasks
- US3 (Update Task Details - P3): 3 tasks
- US4 (Delete Tasks - P4): 4 tasks
- Infrastructure (Setup + Foundational): 10 tasks
- Polish (Cross-cutting): 8 tasks

**Parallel Opportunities**:
- Setup: 4 parallel tasks (all __init__.py files)
- Foundational: 4 parallel tasks (model + 3 service functions)
- US1: 6 parallel tasks (display + input functions)
- US2: 2 parallel tasks (service + validator)
- US4: 2 parallel tasks (service + validator)
- **Total**: ~18 tasks can run in parallel across the project

**MVP Scope** (Recommended First Delivery):
- Phase 1: Setup (5 tasks)
- Phase 2: Foundational (5 tasks)
- Phase 3: User Story 1 (14 tasks)
- **Total for MVP**: 24 tasks

This delivers a working todo app where users can add, view, and quit - enough to provide value and get feedback.

---

## File Creation Checklist

By the end of implementation, these files must exist:

**Models**:
- [ ] src/models/__init__.py
- [ ] src/models/task.py

**Services**:
- [ ] src/services/__init__.py
- [ ] src/services/task_service.py

**CLI**:
- [ ] src/cli/__init__.py
- [ ] src/cli/menu.py
- [ ] src/cli/display.py
- [ ] src/cli/input_handler.py

**Main**:
- [ ] src/__init__.py
- [ ] src/main.py

**Total**: 10 Python files

---

## Execution Notes

- Each task is atomic and can be completed independently within its phase
- Tasks marked [P] can be parallelized for faster completion
- [Story] labels indicate which user story the task belongs to for traceability
- File paths are explicit to avoid ambiguity
- All tasks follow constitutional principles (simplicity, modularity, type safety)
- No tests included (not requested in spec) - focus is on implementation
- Validation through manual testing per quickstart.md after each user story

---

## Ready for Implementation

**Command**: `/sp.implement`

This task list is ready for execution. Start with Phase 1 (Setup), proceed through Foundational (blocking), then implement user stories in priority order (P1 → P2 → P3 → P4).

**Suggested First Session**: Complete through User Story 1 (T001-T024) for MVP delivery.
