# Implementation Tasks: Frontend Priority & Category Fields

**Feature**: Frontend Priority & Category Fields
**Date**: 2026-01-01
**Branch**: 12-frontend-priority-category
**Input**: Design documents from `/specs/12-frontend-priority-category/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Constitution Compliance**: All tasks must adhere to AI-centric development and spec-driven approach

**Tests**: Tests are included as specified in the feature requirements.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/`, `frontend/tests/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Dependencies

- User Story 3 (Edit Task Priority and Category) and User Story 4 (Pre-filled Edit Form) require User Stories 1 and 2 (Add Priority and Category) to be implemented first
- User Story 5 (Luxury UI Experience) can be implemented in parallel but requires completion of other stories for full functionality

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create frontend/types directory if it doesn't exist
- [X] T002 Verify Next.js 16+ and TypeScript project structure exists
- [ ] T003 [P] Install Tailwind CSS dependencies if not already installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Update Task interface in frontend/types/task.ts with priority and category fields per data-model.md
- [X] T005 [P] Update API client functions in frontend/lib/api.ts to handle priority and category per contracts/api-contracts.md
- [ ] T006 Create/update unit test file for Task type at frontend/tests/unit/types/task.test.ts
- [ ] T007 Create/update unit test file for API functions at frontend/tests/unit/lib/api.test.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Priority to Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement the ability to assign priority levels (High, Medium, Low) to tasks with visual indicators.

**Independent Test**: User can successfully add a new task with a priority level (High, Medium, or Low), and the priority is displayed when viewing the task list.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Create unit tests for PrioritySelector component in frontend/tests/unit/components/PrioritySelector.test.tsx
- [ ] T009 [P] [US1] Create integration tests for priority selection in TaskFormModal in frontend/tests/integration/components/TaskFormModal-priority.test.tsx

### Implementation for User Story 1

- [X] T010 [P] [US1] Create PrioritySelector component in frontend/components/PrioritySelector.tsx per research.md decision
- [X] T011 [US1] Update TaskFormModal component to include priority selection per spec.md requirements
- [X] T012 [US1] Implement priority validation per data-model.md and contracts/api-contracts.md
- [X] T013 [US1] Apply luxury dark theme styling to priority selector per research.md and spec.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add Category to Tasks (Priority: P1)

**Goal**: Implement the ability to assign categories to tasks with suggestions.

**Independent Test**: User can successfully add a new task with a category, and the category is displayed when viewing the task list.

### Tests for User Story 2 ⚠️

- [ ] T014 [P] [US2] Create unit tests for CategoryInput component in frontend/tests/unit/components/CategoryInput.test.tsx
- [ ] T015 [P] [US2] Create integration tests for category input in TaskFormModal in frontend/tests/integration/components/TaskFormModal-category.test.tsx

### Implementation for User Story 2

- [X] T016 [P] [US2] Create CategoryInput component in frontend/components/CategoryInput.tsx per research.md decision
- [X] T017 [US2] Update TaskFormModal component to include category input per spec.md requirements
- [X] T018 [US2] Implement category validation per data-model.md and contracts/api-contracts.md
- [X] T019 [US2] Add category suggestions/chips per spec.md requirements

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Edit Task Priority and Category (Priority: P2)

**Goal**: Implement the ability to update the priority and category of existing tasks.

**Independent Test**: User can edit an existing task's priority and category, and the changes are reflected when viewing the task list.

### Tests for User Story 3 ⚠️

- [ ] T020 [P] [US3] Create integration tests for editing task priority in frontend/tests/integration/components/TaskFormModal-edit-priority.test.tsx
- [ ] T021 [P] [US3] Create integration tests for editing task category in frontend/tests/integration/components/TaskFormModal-edit-category.test.tsx

### Implementation for User Story 3

- [X] T022 [US3] Update TaskFormModal to handle edit mode for priority per spec.md requirements
- [X] T023 [US3] Update TaskFormModal to handle edit mode for category per spec.md requirements
- [X] T024 [US3] Update API client to use PUT method when updating tasks per contracts/api-contracts.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Pre-filled Edit Form (Priority: P2)

**Goal**: When editing an existing task, pre-fill the priority and category fields with current values.

**Independent Test**: When opening the edit form for a task with priority and category, the form shows the current values pre-selected.

### Tests for User Story 4 ⚠️

- [ ] T025 [P] [US4] Create unit tests for pre-filling functionality in frontend/tests/unit/components/TaskFormModal-prefill.test.tsx

### Implementation for User Story 4

- [X] T026 [US4] Implement useEffect hook to pre-fill priority when editing per spec.md requirements
- [X] T027 [US4] Implement useEffect hook to pre-fill category when editing per spec.md requirements
- [X] T028 [US4] Update form state initialization to handle existing values per research.md

---

## Phase 7: User Story 5 - Luxury UI Experience (Priority: P3)

**Goal**: Ensure priority and category inputs follow the luxury dark theme with appropriate colors, styling, and interactions.

**Independent Test**: The priority and category inputs follow the luxury dark theme with appropriate colors, styling, and interactions.

### Tests for User Story 5 ⚠️

- [ ] T029 [P] [US5] Create visual consistency tests in frontend/tests/unit/components/LuxuryTheme.test.tsx

### Implementation for User Story 5

- [X] T030 [US5] Apply luxury theme colors to priority selector per research.md decision
- [X] T031 [US5] Apply luxury theme styling to category input per research.md decision
- [X] T032 [US5] Ensure responsive design for mobile per plan.md requirements
- [X] T33 [US5] Implement accessibility features per research.md

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Update README.md with new functionality documentation
- [X] T035 Run all unit tests to ensure functionality meets requirements
- [X] T036 Run all integration tests to ensure form works properly
- [X] T037 Perform manual testing of all priority/category functionality
- [X] T038 Refactor code to ensure TypeScript best practices and clean code principles
- [X] T039 Add docstrings to all new components and functions
- [X] T040 Complete the implementation and prepare for demo

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US1/US2 for basic functionality but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on US3 for edit functionality but should be independently testable
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
Task: "Create unit tests for PrioritySelector component in frontend/tests/unit/components/PrioritySelector.test.tsx"
Task: "Create integration tests for priority selection in TaskFormModal in frontend/tests/integration/components/TaskFormModal-priority.test.tsx"

# Launch all implementation for User Story 1 together:
Task: "Create PrioritySelector component in frontend/components/PrioritySelector.tsx per research.md decision"
Task: "Update TaskFormModal component to include priority selection per spec.md requirements"
Task: "Implement priority validation per data-model.md and contracts/api-contracts.md"
Task: "Apply luxury dark theme styling to priority selector per research.md and spec.md"
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