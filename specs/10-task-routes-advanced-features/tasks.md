# Tasks: Task Routes with Advanced Features

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Constitution Compliance**: All tasks must adhere to AI-centric development and spec-driven approach

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure per implementation plan
- [ ] T002 [P] Install dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, python-dotenv, pyjwt[cryptography], better-auth
- [ ] T003 [P] Create basic project files: main.py, db.py, models.py, dependencies.py, routes/tasks.py
- [ ] T004 Create requirements.txt with all required packages

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Update Task model in models.py with priority and category fields
- [X] T006 [P] Update TaskCreate request model in routes/tasks.py
- [X] T007 [P] Update TaskUpdate request model in routes/tasks.py
- [X] T008 Update database migration to include new fields (SQLModel auto-migration)
- [X] T009 Verify JWT authentication dependency works correctly
- [X] T010 Update main.py to include the tasks router

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Prioritization and Categorization (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to assign priority levels (High, Medium, Low) and categories to their tasks

**Independent Test**: Can be fully tested by creating tasks with different priority levels and categories, then viewing them to confirm the data is stored, retrieved, and displayed correctly with proper visual indicators.

### Implementation for User Story 1

- [X] T011 [P] [US1] Update POST /api/tasks endpoint to accept priority and category in routes/tasks.py
- [X] T012 [P] [US1] Update PUT /api/tasks/{id} endpoint to accept priority and category updates in routes/tasks.py
- [X] T013 [US1] Update GET /api/tasks endpoint to return priority and category in response in routes/tasks.py
- [X] T014 [US1] Add validation for priority field (high, medium, low) in models.py
- [X] T015 [US1] Add validation for category field (max 50 characters) in models.py
- [X] T016 [US1] Test task creation with priority and category values
- [X] T017 [US1] Test task updates with priority and category changes

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Advanced Search and Filtering (Priority: P1)

**Goal**: Enable authenticated users with many tasks to search and filter by keyword, status, priority, and category

**Independent Test**: Can be fully tested by creating tasks with various attributes, then using search and filter functionality to verify that only matching tasks are returned.

### Implementation for User Story 2

- [X] T018 [P] [US2] Update GET /api/tasks endpoint to support search query parameter in routes/tasks.py
- [X] T019 [P] [US2] Update GET /api/tasks endpoint to support priority filter in routes/tasks.py
- [X] T020 [P] [US2] Update GET /api/tasks endpoint to support category filter in routes/tasks.py
- [X] T021 [US2] Implement LIKE search functionality for title and description in routes/tasks.py
- [X] T022 [US2] Implement proper filtering logic for status, priority, and category in routes/tasks.py
- [X] T023 [US2] Test search functionality with various keywords
- [X] T024 [US2] Test filtering by different criteria (status, priority, category)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Sorting Capabilities (Priority: P2)

**Goal**: Enable authenticated users to sort their tasks by different criteria (creation date, title, priority, category)

**Independent Test**: Can be fully tested by creating tasks with different attributes, then using sort functionality to verify that tasks are displayed in the correct order.

### Implementation for User Story 3

- [X] T025 [P] [US3] Update GET /api/tasks endpoint to support sort query parameter in routes/tasks.py
- [X] T026 [P] [US3] Implement sorting by creation date in GET /api/tasks endpoint
- [X] T027 [US3] Implement sorting by title in GET /api/tasks endpoint
- [X] T028 [US3] Implement sorting by priority (high > medium > low) in GET /api/tasks endpoint
- [X] T029 [US3] Implement sorting by category in GET /api/tasks endpoint
- [X] T030 [US3] Test sorting by different criteria
- [X] T031 [US3] Verify priority sort order (high first, then medium, then low)

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Enhanced UI/UX with Professional Polish (Priority: P2)

**Goal**: Provide a polished, professional interface that clearly displays task information (priority, category, status) with visual cues

**Independent Test**: Can be fully tested by creating tasks with various attributes and verifying that the UI displays all information clearly with appropriate visual styling.

### Implementation for User Story 4

- [X] T032 [P] [US4] Update TaskCard component to show priority indicators in frontend/components/TaskCard.tsx
- [X] T033 [P] [US4] Update TaskCard component to show category tags in frontend/components/TaskCard.tsx
- [X] T034 [US4] Add priority color stripe to TaskCard left border in frontend/components/TaskCard.tsx
- [X] T035 [US4] Add visual indicators for completed tasks (muted colors, strikethrough) in frontend/components/TaskCard.tsx
- [X] T036 [US4] Update TaskFormModal to include priority dropdown in frontend/components/TaskFormModal.tsx
- [X] T037 [US4] Update TaskFormModal to include category input in frontend/components/TaskFormModal.tsx
- [X] T038 [US4] Test UI elements display correctly with different task attributes

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Frontend Integration & Dashboard Features

**Goal**: Integrate all new features into the frontend dashboard with search, filter, and sort controls

### Implementation for Integration

- [X] T039 [P] Add search bar to tasks dashboard in frontend/app/tasks/page.tsx
- [X] T040 [P] Add filter controls (status, priority, category) to tasks dashboard
- [X] T041 [P] Add sort controls to tasks dashboard
- [X] T042 Update API client to send query parameters for search, filter, sort
- [X] T043 Implement dashboard statistics (total, pending, completed, high priority counts)
- [X] T044 Update empty state to include category suggestions
- [X] T045 Test complete frontend integration with all new features

---

## Phase 8: Security Enhancement & Error Handling

**Goal**: Strengthen security and reliability with comprehensive error handling

### Implementation for Security Enhancement

- [X] T046 [P] Ensure all endpoints properly enforce user isolation (user_id matching)
- [X] T047 [P] Add comprehensive error handling for all new functionality
- [X] T048 Add proper HTTP status codes (401, 403, 404) for different failure cases
- [X] T049 Add input validation for all new fields and parameters
- [X] T050 Test error scenarios (invalid tokens, unauthorized access, etc.)
- [X] T051 Ensure security best practices are followed for all new endpoints

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T052 [P] Update README.md with documentation for new features
- [X] T053 [P] Add API documentation for new endpoints and parameters
- [X] T054 Perform security review of all new functionality
- [X] T055 Test complete authentication flow with frontend and backend integration
- [X] T056 Run specification compliance check to ensure all requirements are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2)
- **Integration (Phase 7)**: Depends on foundational and user stories completion
- **Security Enhancement (Phase 8)**: Depends on all previous phases
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs priority/category data) but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All components within a user story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Update POST /api/tasks endpoint to accept priority and category in routes/tasks.py"
Task: "Update PUT /api/tasks/{id} endpoint to accept priority and category updates in routes/tasks.py"
Task: "Update GET /api/tasks endpoint to return priority and category in response in routes/tasks.py"
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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add Integration → Test → Deploy/Demo
7. Add Security Enhancement → Test → Deploy/Demo
8. Polish and finalize → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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