# Tasks: Single Task Operations

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

- [X] T001 [P] Verify routes/tasks.py file exists with APIRouter
- [X] T002 [P] Confirm dependencies (FastAPI, SQLModel, python-jose, PyJWT) are available
- [X] T003 [P] Verify models.py contains Task entity with proper fields
- [X] T004 [P] Confirm dependencies.py has get_current_user_id function

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create TaskUpdate request model in routes/tasks.py
- [X] T006 [P] Implement get_task_or_404 helper function in routes/tasks.py
- [X] T007 [P] Add necessary imports to routes/tasks.py (Response, Field, etc.)
- [X] T008 Verify JWT authentication dependency works correctly

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Retrieve Individual Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to view details of specific tasks from their collection

**Independent Test**: Can be fully tested by sending authenticated GET requests to /api/tasks/{id} and verifying that users can only retrieve their own tasks, delivering the core value of detailed task access.

### Implementation for User Story 1

- [X] T009 [P] [US1] Implement GET /api/tasks/{id} endpoint in routes/tasks.py
- [X] T010 [P] [US1] Add path parameter validation for task ID in GET endpoint
- [X] T011 [US1] Implement ownership verification for single task retrieval
- [X] T012 [US1] Test GET endpoint with valid task ID and authentication
- [X] T013 [US1] Test 404 response for non-existent task IDs
- [X] T014 [US1] Test 403 response when accessing another user's task

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update Task Details (Priority: P1)

**Goal**: Allow authenticated users to modify the details of existing tasks (title or description)

**Independent Test**: Can be fully tested by sending authenticated PUT requests to /api/tasks/{id} with updated task data and verifying that only the task owner can update their tasks, delivering the core value of task modification.

### Implementation for User Story 2

- [X] T015 [P] [US2] Implement PUT /api/tasks/{id} endpoint in routes/tasks.py
- [X] T016 [P] [US2] Add request body validation with TaskUpdate model
- [X] T017 [US2] Implement partial update logic (only update provided fields)
- [X] T018 [US2] Add ownership verification for task updates
- [X] T019 [US2] Test PUT endpoint with valid data and authentication
- [X] T020 [US2] Test 404 response for non-existent task IDs
- [X] T021 [US2] Test 403 response when updating another user's task
- [X] T022 [US2] Test validation for title length (1-200 chars) and description (0-1000 chars)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P1)

**Goal**: Enable authenticated users to remove tasks they no longer need from their collection

**Independent Test**: Can be fully tested by sending authenticated DELETE requests to /api/tasks/{id} and verifying that only the task owner can delete their tasks, delivering the core value of task removal.

### Implementation for User Story 3

- [X] T023 [P] [US3] Implement DELETE /api/tasks/{id} endpoint in routes/tasks.py
- [X] T024 [P] [US3] Add ownership verification for task deletion
- [X] T025 [US3] Implement proper response (204 No Content) for successful deletion
- [X] T026 [US3] Test DELETE endpoint with valid task ID and authentication
- [X] T027 [US3] Test 404 response for non-existent task IDs
- [X] T028 [US3] Test 403 response when deleting another user's task
- [X] T029 [US3] Verify task is actually removed from database after deletion

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P1)

**Goal**: Allow authenticated users to mark tasks as complete or incomplete

**Independent Test**: Can be fully tested by sending authenticated PATCH requests to /api/tasks/{id}/complete and verifying that only the task owner can toggle completion status, delivering the core value of task status management.

### Implementation for User Story 4

- [X] T030 [P] [US4] Implement PATCH /api/tasks/{id}/complete endpoint in routes/tasks.py
- [X] T031 [P] [US4] Add ownership verification for completion toggling
- [X] T032 [US4] Implement toggle logic for completion status
- [X] T033 [US4] Ensure updated_at timestamp is updated on toggle
- [X] T034 [US4] Test PATCH endpoint with valid task ID and authentication
- [X] T035 [US4] Test 404 response for non-existent task IDs
- [X] T036 [US4] Test 403 response when toggling another user's task
- [X] T037 [US4] Verify completion status properly toggles between true/false

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Integration & Validation

**Goal**: Ensure all endpoints work together and with the existing system

### Implementation for Integration

- [X] T038 [P] Test complete workflow: create → retrieve → update → toggle → delete
- [X] T039 [P] Verify all endpoints properly enforce user isolation
- [X] T040 Test error scenarios (invalid tokens, malformed requests)
- [X] T041 Validate API responses match contract specifications
- [X] T042 Test with multiple concurrent users
- [X] T043 Test edge cases like very long titles or descriptions

---

## Phase 8: Security Enhancement & Error Handling

**Goal**: Strengthen security and reliability with comprehensive error handling

### Implementation for Security Enhancement

- [X] T044 [P] Add comprehensive error handling for all authentication scenarios
- [X] T045 [P] Implement proper HTTP status codes (401, 403, 404) for different failure cases
- [X] T046 Add input sanitization for task titles and descriptions
- [X] T047 Enhance security by preventing timing attacks in ownership checks
- [X] T048 Test edge cases like extremely long inputs or unusual request formats

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T049 [P] Update README.md with documentation for new endpoints
- [X] T050 [P] Add API documentation for the new endpoints
- [X] T051 Perform security review of all task operations
- [X] T052 Test complete authentication flow with frontend API client
- [X] T053 Run specification compliance check to ensure all requirements are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P1)
- **Integration (Phase 7)**: Depends on foundational and user stories completion
- **Security Enhancement (Phase 8)**: Depends on all previous phases
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

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
Task: "Implement GET /api/tasks/{id} endpoint in routes/tasks.py"
Task: "Add path parameter validation for task ID in GET endpoint in routes/tasks.py"
Task: "Implement ownership verification for single task retrieval in routes/tasks.py"
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