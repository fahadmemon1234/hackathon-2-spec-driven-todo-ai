# Implementation Tasks: Todo CLI App

**Feature**: Todo CLI App
**Date**: 2025-01-02
**Branch**: 1-todo-cli-app
**Input**: Design documents from `/specs/1-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Constitution Compliance**: All tasks must adhere to AI-centric development and spec-driven approach

**Tests**: Tests are included as specified in the feature requirements.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Dependencies

- User Story 2 (View All Tasks) requires User Story 1 (Add New Tasks) to be implemented first as viewing tasks requires having tasks to view
- User Stories 3, 4, and 5 (Mark, Update, Delete) all require the foundational Task model and basic task management functionality from Stories 1 and 2

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure following the plan.md specification
- [X] T002 Initialize Python project with UV dependencies (Python 3.13+, pytest)
- [X] T003 [P] Configure linting and formatting tools (PEP 8 compliance)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task data model in src/models/task.py following data-model.md specification
- [X] T005 [P] Create TodoManager service in src/services/todo_manager.py with basic functionality
- [X] T006 [P] Create main CLI application structure in src/cli/main.py
- [X] T007 Implement ID generation strategy in TodoManager as per research.md
- [X] T008 Create custom exception classes for error handling as per research.md
- [X] T009 [P] Write unit tests for Task model in tests/unit/test_task.py
- [X] T010 [P] Write unit tests for TodoManager in tests/unit/test_todo_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement the ability to add new tasks with title and description, assigning unique IDs and default incomplete status.

**Independent Test**: User can successfully add a new task with title and description, and the task appears in the task list with a unique ID and "incomplete" status.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Unit tests for add_task functionality in tests/unit/test_todo_manager.py
- [X] T012 [P] [US1] Integration tests for 'add' CLI command in tests/integration/test_cli.py

### Implementation for User Story 1

- [X] T013 [US1] Implement add_task method in TodoManager with validation per data-model.md
- [X] T014 [US1] Add CLI command handling for 'add' command per contracts/cli-contracts.md
- [X] T015 [US1] Implement input validation for title and description lengths per data-model.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Implement the ability to view all tasks with their status indicators.

**Independent Test**: User can view a list of all tasks with their IDs, titles, descriptions, and completion status clearly displayed.

### Tests for User Story 2 ⚠️

- [X] T016 [P] [US2] Unit tests for get_all_tasks functionality in tests/unit/test_todo_manager.py
- [X] T017 [P] [US2] Integration tests for 'list' CLI command in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T018 [US2] Implement get_all_tasks method in TodoManager per spec.md requirements
- [X] T019 [US2] Add CLI command handling for 'list' command per contracts/cli-contracts.md
- [X] T020 [US2] Implement proper display formatting for tasks with ID, title, description, and status

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Implement the ability to mark tasks as complete or incomplete by ID.

**Independent Test**: User can change the completion status of a task by ID, and the change is reflected when viewing the task list.

### Tests for User Story 3 ⚠️

- [X] T021 [P] [US3] Unit tests for mark_complete/mark_incomplete functionality in tests/unit/test_todo_manager.py
- [X] T022 [P] [US3] Integration tests for 'complete' and 'incomplete' CLI commands in tests/integration/test_cli.py

### Implementation for User Story 3

- [X] T023 [US3] Implement mark_complete and mark_incomplete methods in TodoManager per data-model.md
- [X] T024 [US3] Add CLI command handling for 'complete' command per contracts/cli-contracts.md
- [X] T025 [US3] Add CLI command handling for 'incomplete' command per contracts/cli-contracts.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Implement the ability to update task details by ID.

**Independent Test**: User can update the title or description of a task by ID, and the changes are reflected when viewing the task list.

### Tests for User Story 4 ⚠️

- [X] T026 [P] [US4] Unit tests for update_task functionality in tests/unit/test_todo_manager.py
- [X] T027 [P] [US4] Integration tests for 'update' CLI command in tests/integration/test_cli.py

### Implementation for User Story 4

- [X] T028 [US4] Implement update_task method in TodoManager per spec.md requirements
- [X] T029 [US4] Add CLI command handling for 'update' command per contracts/cli-contracts.md
- [X] T030 [US4] Implement input validation for updated title and description per data-model.md

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Implement the ability to delete tasks by ID.

**Independent Test**: User can delete a task by ID, and the task no longer appears in the task list.

### Tests for User Story 5 ⚠️

- [X] T031 [P] [US5] Unit tests for delete_task functionality in tests/unit/test_todo_manager.py
- [X] T032 [P] [US5] Integration tests for 'delete' CLI command in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T033 [US5] Implement delete_task method in TodoManager per spec.md requirements
- [X] T034 [US5] Add CLI command handling for 'delete' command per contracts/cli-contracts.md
- [X] T035 [US5] Implement proper error handling for non-existent task IDs

---

## Phase 8: Error Handling and Help Commands

**Goal**: Implement proper error handling and help functionality as specified in contracts/cli-contracts.md.

- [X] T036 Implement help command to display available commands per contracts/cli-contracts.md
- [X] T037 Implement quit/exit commands to terminate the application per contracts/cli-contracts.md
- [X] T038 Implement error handling for invalid commands per contracts/cli-contracts.md
- [X] T039 Implement error handling for invalid task IDs per contracts/cli-contracts.md
- [X] T040 Implement error handling for invalid parameters per contracts/cli-contracts.md
- [X] T041 Implement error handling for input validation errors per contracts/cli-contracts.md

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Update README.md with complete usage instructions from quickstart.md
- [X] T043 Run all unit tests to ensure functionality meets requirements
- [X] T044 Run all integration tests to ensure CLI works properly
- [X] T045 Perform manual testing of all commands with various inputs
- [X] T046 Refactor code to ensure PEP 8 compliance and clean code principles
- [X] T047 Add docstrings to all classes and methods
- [X] T048 Finalize error messages to be user-friendly per contracts/cli-contracts.md
- [X] T049 Complete the implementation and prepare for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit tests for add_task functionality in tests/unit/test_todo_manager.py"
Task: "Integration tests for 'add' CLI command in tests/integration/test_cli.py"

# Launch all implementation for User Story 1 together:
Task: "Implement add_task method in TodoManager with validation per data-model.md"
Task: "Add CLI command handling for 'add' command per contracts/cli-contracts.md"
Task: "Implement input validation for title and description lengths per data-model.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence