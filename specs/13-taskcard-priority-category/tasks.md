# Implementation Tasks: TaskCard Priority & Category Visual Display

**Feature**: TaskCard Priority & Category Visual Display
**Date**: 2026-01-02
**Branch**: 13-taskcard-priority-category
**Input**: Design documents from `/specs/13-taskcard-priority-category/`
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

- User Story 3 (Completed Task Styling) requires User Story 1 (Visual Priority Indicators) and User Story 2 (Category Display) to be implemented first
- User Story 4 (Luxury Dark Theme Consistency) can be implemented in parallel but requires completion of other stories for full functionality
- User Story 5 (Responsive Design) depends on the completion of other stories to ensure proper responsiveness

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify Next.js 16+ and TypeScript project structure exists
- [X] T002 Verify Tailwind CSS is properly configured per plan.md requirements
- [ ] T003 [P] Install any additional dependencies if needed for luxury UI components

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Verify Task interface includes priority and category fields per data-model.md
- [X] T005 [P] Create/update unit test file for TaskCard component at frontend/tests/unit/components/TaskCard.test.tsx
- [X] T006 [P] Create/update integration test file for TaskCard at frontend/tests/integration/components/TaskCard.test.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Visual Priority Indicators (Priority: P1) 🎯 MVP

**Goal**: Implement visual indicators for task priority levels (High, Medium, Low) on each task card with colored left stripes and priority badges.

**Independent Test**: User can visually identify the priority level of a task by looking at the colored left stripe and priority badge on the task card.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Create unit tests for priority stripe display in frontend/tests/unit/components/TaskCard-priority-stripe.test.tsx
- [X] T008 [P] [US1] Create unit tests for priority badge display in frontend/tests/unit/components/TaskCard-priority-badge.test.tsx

### Implementation for User Story 1

- [X] T009 [US1] Update TaskCard component to include left priority stripe per research.md decision
- [X] T010 [US1] Implement priority stripe with colors: High=#d90429, Medium=#f6d72d, Low=#666666 per spec.md requirements
- [X] T011 [US1] Update TaskCard component to include priority badge per research.md decision
- [X] T012 [US1] Implement priority badge with uppercase text and matching background colors per spec.md requirements
- [X] T013 [US1] Apply luxury dark theme styling to priority indicators per research.md and spec.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Category Display (Priority: P1)

**Goal**: Implement category tags on task cards that display when a category is present.

**Independent Test**: User can visually identify the category of a task by looking at the category tag on the task card.

### Tests for User Story 2 ⚠️

- [X] T014 [P] [US2] Create unit tests for category tag display in frontend/tests/unit/components/TaskCard-category.test.tsx

### Implementation for User Story 2

- [X] T015 [US2] Update TaskCard component to include conditional category tag per research.md decision
- [X] T016 [US2] Implement category tag as rounded pill with subtle background per spec.md requirements
- [X] T017 [US2] Add logic to hide category tag when no category is present per spec.md requirements
- [X] T018 [US2] Apply luxury dark theme styling to category tag per research.md and spec.md

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Completed Task Styling (Priority: P2)

**Goal**: Implement distinct styling for completed tasks that includes strikethrough titles and reduced opacity while keeping priority indicators visible.

**Independent Test**: User can distinguish completed tasks from pending tasks by their styling while still seeing priority and category information.

### Tests for User Story 3 ⚠️

- [X] T019 [P] [US3] Create unit tests for completed task styling in frontend/tests/unit/components/TaskCard-completed.test.tsx

### Implementation for User Story 3

- [X] T020 [US3] Update TaskCard component to apply strikethrough styling to completed task titles per spec.md requirements
- [X] T021 [US3] Implement reduced opacity for completed task cards while keeping priority stripes fully visible per spec.md requirements
- [X] T022 [US3] Apply slightly faded styling to badges and tags for completed tasks per spec.md requirements

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Luxury Dark Theme Consistency (Priority: P2)

**Goal**: Ensure priority and category displays follow the luxury dark theme with appropriate colors, styling, and interactions.

**Independent Test**: The priority and category displays follow the luxury dark theme with appropriate colors, styling, and interactions.

### Tests for User Story 4 ⚠️

- [X] T023 [P] [US4] Create visual consistency tests in frontend/tests/unit/components/TaskCard-theme.test.tsx

### Implementation for User Story 4

- [X] T024 [US4] Apply luxury theme colors to all priority and category elements per research.md decision
- [X] T025 [US4] Implement subtle hover effects with gold accent color per spec.md requirements
- [X] T026 [US4] Ensure proper contrast ratios and accessibility per research.md
- [X] T027 [US4] Add smooth transitions for interactive elements per research.md

---

## Phase 7: User Story 5 - Responsive Design (Priority: P3)

**Goal**: Ensure priority and category displays work well on mobile devices with priority stripe remaining visible and tags stacking appropriately.

**Independent Test**: The priority and category displays are properly visible and usable on mobile devices.

### Tests for User Story 5 ⚠️

- [X] T028 [P] [US5] Create responsive design tests in frontend/tests/unit/components/TaskCard-responsive.test.tsx

### Implementation for User Story 5

- [X] T029 [US5] Ensure priority stripe remains visible on mobile per spec.md requirements
- [X] T030 [US5] Implement category tag stacking on mobile per research.md decision
- [X] T031 [US5] Test layout on various screen sizes per research.md
- [X] T032 [US5] Optimize touch targets for mobile devices per research.md

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T033 [P] Update README.md with new functionality documentation
- [X] T034 Run all unit tests to ensure functionality meets requirements
- [X] T035 Run all integration tests to ensure TaskCard works properly
- [X] T036 Perform manual testing of all priority/category functionality on different devices
- [X] T037 Refactor code to ensure TypeScript best practices and clean code principles
- [X] T038 Add docstrings to all new components and functions
- [X] T039 Finalize error messages to be user-friendly per research.md
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
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on completion of other stories to ensure proper responsive behavior

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
Task: "Create unit tests for priority stripe display in frontend/tests/unit/components/TaskCard-priority-stripe.test.tsx"
Task: "Create unit tests for priority badge display in frontend/tests/unit/components/TaskCard-priority-badge.test.tsx"

# Launch all implementation for User Story 1 together:
Task: "Update TaskCard component to include left priority stripe per research.md decision"
Task: "Implement priority stripe with colors: High=#d90429, Medium=#f6d72d, Low=#666666 per spec.md requirements"
Task: "Update TaskCard component to include priority badge per research.md decision"
Task: "Implement priority badge with uppercase text and matching background colors per spec.md requirements"
Task: "Apply luxury dark theme styling to priority indicators per research.md and spec.md"
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