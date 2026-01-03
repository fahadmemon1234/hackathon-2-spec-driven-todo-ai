# Implementation Tasks: Todo App Intermediate Features

## Feature Overview

**Feature**: Intermediate Level Features for Todo In-Memory Python Console App (Phase I Extension)
**Branch**: 2-todo-intermediate-features
**Spec**: specs/2-todo-intermediate-features/spec.md
**Project**: In-memory CLI todo application with enhanced organization and usability features

## Dependencies

- Python 3.13+
- Standard library only (no external dependencies)
- UV for package management
- Existing basic todo app features (Add, Delete, Update, View, Mark Complete)

## Implementation Strategy

This implementation will follow an incremental delivery approach, starting with the most critical user story (Enhanced Task Creation with Priority and Tags) and building up to the complete feature set. Each user story will be implemented as a complete, independently testable increment.

## Phase 1: Setup

### Goal
Initialize project structure and ensure development environment is ready for implementation.

- [X] T001 Create src directory if it doesn't exist
- [X] T002 Set up pyproject.toml with project metadata and dependencies
- [X] T003 Create basic directory structure (src/models, src/managers, src/cli)
- [X] T004 Verify Python 3.13+ compatibility
- [X] T005 [P] Create initial README.md with project overview

## Phase 2: Foundational

### Goal
Implement the core data model and manager that will support all user stories.

- [X] T006 [P] [US1] Create Task model with priority and tags fields in src/models/task.py
- [X] T007 [P] [US1] Define priority constants and validation in src/models/priority.py
- [X] T008 [US1] Update TodoManager to handle priority and tags in src/managers/todo_manager.py
- [X] T009 [US1] Implement validation logic for priority and tags in src/utils/validators.py
- [X] T010 [US1] Create CLI argument parser for new options in src/cli/argument_parser.py

## Phase 3: User Story 1 - Enhanced Task Creation with Priority and Tags (P1)

### Goal
Enable users to assign priority levels (High, Medium, Low) and tags to tasks during creation or update.

**Independent Test**: Can be fully tested by creating tasks with different priority levels and tags, then viewing them to confirm the data is stored and displayed correctly.

- [X] T011 [US1] Update add_task method to accept priority and tags in src/managers/todo_manager.py
- [X] T012 [US1] Update CLI to handle --priority and --tags options for add command in src/cli/main.py
- [X] T013 [US1] Implement validation for priority values in src/managers/todo_manager.py
- [X] T014 [US1] Implement validation for tags format in src/managers/todo_manager.py
- [X] T015 [US1] Update Task model initialization to include priority and tags in src/models/task.py
- [X] T016 [US1] Test creating tasks with priority and tags in src/test/test_us1.py

## Phase 4: User Story 2 - Enhanced Task Update with Priority and Tags (P2)

### Goal
Allow users to update priority and tags of existing tasks.

**Independent Test**: Can be fully tested by creating tasks with initial priority and tags, then updating them to verify changes are saved correctly.

- [X] T017 [US2] Update update_task method to handle priority and tags in src/managers/todo_manager.py
- [X] T018 [US2] Update CLI to handle --priority and --tags options for update command in src/cli/main.py
- [X] T019 [US2] Implement partial update logic (allow updating only priority or only tags) in src/managers/todo_manager.py
- [X] T020 [US2] Test updating task priority and tags in src/test/test_us2.py

## Phase 5: User Story 3 - Enhanced Task View (P3)

### Goal
Display additional information (priority, tags, status indicators) clearly when viewing the task list.

**Independent Test**: Can be fully tested by creating tasks with various attributes, then viewing the enhanced list to confirm all information is displayed clearly.

- [X] T021 [US3] Update task display format to show priority and tags in src/cli/main.py
- [X] T022 [US3] Implement enhanced task display with priority, tags, and status indicators in src/cli/display.py
- [X] T023 [US3] Update list command to show all new information in src/cli/main.py
- [X] T024 [US3] Test enhanced task display in src/test/test_us3.py

## Phase 6: User Story 4 - Search Tasks (P4)

### Goal
Support searching tasks by keyword in title, description, and tags.

**Independent Test**: Can be fully tested by creating tasks with different attributes, then using search command to verify that only tasks containing the keyword are returned.

- [X] T025 [US4] Implement search functionality in TodoManager in src/managers/todo_manager.py
- [X] T026 [US4] Add search command to CLI in src/cli/main.py
- [X] T027 [US4] Implement keyword matching logic for title, description, and tags in src/managers/todo_manager.py
- [X] T028 [US4] Handle case-insensitive search in src/managers/todo_manager.py
- [X] T029 [US4] Test search functionality in src/test/test_us4.py

## Phase 7: User Story 5 - Filter Tasks (P5)

### Goal
Support filtering tasks by status (complete/incomplete), priority, or specific tag.

**Independent Test**: Can be fully tested by creating tasks with different attributes, then using filter command to verify that only tasks matching the filter criteria are returned.

- [X] T030 [US5] Implement filter functionality in TodoManager in src/managers/todo_manager.py
- [X] T031 [US5] Add filter options to list command in src/cli/main.py
- [X] T032 [US5] Implement filtering by status in src/managers/todo_manager.py
- [X] T033 [US5] Implement filtering by priority in src/managers/todo_manager.py
- [X] T034 [US5] Implement filtering by tag in src/managers/todo_manager.py
- [X] T035 [US5] Test filter functionality in src/test/test_us5.py

## Phase 8: User Story 6 - Sort Tasks (P6)

### Goal
Support sorting tasks by priority (High → Low), completion status, or alphabetically by title.

**Independent Test**: Can be fully tested by creating tasks with different priorities and titles, then using sort commands to verify that tasks are displayed in the correct order.

- [X] T036 [US6] Implement sort functionality in TodoManager in src/managers/todo_manager.py
- [X] T037 [US6] Add sort options to list command in src/cli/main.py
- [X] T038 [US6] Implement sorting by priority (High → Low) in src/managers/todo_manager.py
- [X] T039 [US6] Implement sorting by completion status in src/managers/todo_manager.py
- [X] T040 [US6] Implement sorting by title alphabetically in src/managers/todo_manager.py
- [X] T041 [US6] Test sort functionality in src/test/test_us6.py

## Phase 9: User Story 7 - CLI Enhancement and Integration (P7)

### Goal
Integrate all new features into a cohesive CLI experience with proper command structure.

- [X] T042 [US7] Update list command with combined sort, filter, and search options in src/cli/main.py
- [X] T043 [US7] Implement comprehensive argument validation in src/cli/argument_parser.py
- [X] T044 [US7] Add help text for new commands and options in src/cli/main.py
- [X] T045 [US7] Test combined functionality (search + filter + sort) in src/test/test_us7.py

## Phase 10: User Story 8 - Error Handling and Validation (P8)

### Goal
Implement comprehensive error handling and validation for all new features.

- [X] T046 [US8] Add validation for invalid priority values in src/managers/todo_manager.py
- [X] T047 [US8] Add validation for empty or invalid tags in src/managers/todo_manager.py
- [X] T048 [US8] Handle edge cases for search with no results in src/managers/todo_manager.py
- [X] T049 [US8] Handle edge cases for filtering with no results in src/managers/todo_manager.py
- [X] T050 [US8] Add appropriate error messages for all validation failures in src/cli/main.py
- [X] T051 [US8] Test error handling scenarios in src/test/test_us8.py

## Phase 11: Polish & Cross-Cutting Concerns

### Goal
Finalize the implementation with documentation, testing, and quality improvements.

- [X] T052 [P] Add docstrings to all new functions and classes in all files
- [X] T053 [P] Add type hints to all new functions and classes in all files
- [X] T054 [P] Update README.md with new feature documentation
- [X] T055 [P] Create usage examples in quickstart guide
- [X] T056 [P] Run full test suite to ensure backward compatibility
- [X] T057 [P] Perform final code review and refactoring
- [X] T058 [P] Update pyproject.toml with final project metadata

## Dependencies

### User Story Completion Order
1. US1 (P1) - Enhanced Task Creation: Must be completed first as it provides the foundational data model
2. US2 (P2) - Enhanced Task Update: Depends on US1 (needs priority/tags in Task model)
3. US3 (P3) - Enhanced Task View: Depends on US1 (needs priority/tags in Task model)
4. US4 (P4) - Search Tasks: Depends on US1 (needs priority/tags in Task model)
5. US5 (P5) - Filter Tasks: Depends on US1 (needs priority/tags in Task model)
6. US6 (P6) - Sort Tasks: Depends on US1 (needs priority in Task model)
7. US7 (P7) - CLI Enhancement: Depends on US1-US6 (integrates all features)
8. US8 (P8) - Error Handling: Can be implemented in parallel with other stories but should be validated last

### Parallel Execution Examples
- T006-T007: Can be done in parallel as they work on different files
- T025-T030: Search and filter implementation can be done in parallel
- T036-T041: Sort functionality can be developed in parallel with search/filter
- T052-T055: Documentation tasks can be done in parallel

## MVP Scope

The MVP (Minimum Viable Product) for this feature would include:
- US1: Enhanced Task Creation with Priority and Tags (T011-T016)
- US2: Enhanced Task Update with Priority and Tags (T017-T020)
- US3: Enhanced Task View (T021-T024)

This would provide the core functionality of creating, updating, and viewing tasks with priority and tags, which is the foundation for all other features.