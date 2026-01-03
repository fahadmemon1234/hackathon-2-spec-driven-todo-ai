# Tasks: Database Connection & Task Model

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

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 [P] Install dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, python-dotenv, pyjwt[cryptography]
- [X] T003 [P] Create basic project files: main.py, db.py, models.py, dependencies.py, routes/tasks.py, .env
- [X] T004 Create requirements.txt with all required packages

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database connection with Neon PostgreSQL in db.py
- [X] T006 [P] Create Task model in models.py with SQLModel
- [X] T007 Create JWT verification dependency in dependencies.py
- [X] T008 Setup CORS middleware in main.py to allow http://localhost:3000
- [X] T009 Create health endpoint GET /health in main.py
- [X] T010 Setup APIRouter for tasks in routes/tasks.py and include in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Persistent Task Storage (Priority: P1) 🎯 MVP

**Goal**: Enable users to store tasks that persist across application restarts using Neon PostgreSQL

**Independent Test**: Can be fully tested by creating tasks, restarting the server, and verifying that tasks still exist, delivering the core value of persistent task management.

### Implementation for User Story 1

- [X] T011 [P] [US1] Update main.py to import models and create tables on startup
- [X] T012 [P] [US1] Implement database session dependency in db.py
- [X] T013 [US1] Add environment variable loading with python-dotenv in main.py
- [X] T014 [US1] Create database engine with Neon PostgreSQL settings in db.py
- [X] T015 [US1] Test database connection and table creation functionality

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Multi-User Data Isolation (Priority: P1)

**Goal**: Ensure users can only access tasks associated with their Better Auth user account

**Independent Test**: Can be fully tested by creating tasks with multiple user accounts and verifying that each user only sees their own tasks, delivering the core value of secure multi-user functionality.

### Implementation for User Story 2

- [X] T016 [P] [US2] Enhance Task model with user_id foreign key to Better Auth users
- [X] T017 [P] [US2] Implement user_id validation in Task model
- [X] T018 [US2] Add ownership checks to task endpoints in routes/tasks.py
- [X] T019 [US2] Update JWT verification to extract user_id from token
- [X] T020 [US2] Test multi-user isolation with different authentication tokens

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Database Connection Reliability (Priority: P2)

**Goal**: Maintain stable connection to Neon PostgreSQL database for consistent task data availability

**Independent Test**: Can be fully tested by establishing a connection to Neon PostgreSQL and performing multiple operations without disconnection, delivering the value of reliable task management.

### Implementation for User Story 3

- [X] T021 [P] [US3] Configure database connection pooling in db.py
- [X] T022 [P] [US3] Implement connection error handling and retry logic
- [X] T023 [US3] Add database health check endpoint
- [X] T024 [US3] Test connection stability under load
- [X] T025 [US3] Document database connection best practices

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Additional Task Operations

**Goal**: Implement full CRUD operations for tasks with proper validation

### Implementation for Additional Operations

- [X] T026 [P] Create GET /api/tasks endpoint to list user's tasks
- [X] T027 [P] Create POST /api/tasks endpoint to create new task
- [X] T028 Create GET /api/tasks/{id} endpoint to retrieve single task
- [X] T029 Create PUT /api/tasks/{id} endpoint to update task
- [X] T030 Create DELETE /api/tasks/{id} endpoint to delete task
- [X] T031 Create PATCH /api/tasks/{id}/complete endpoint to toggle completion
- [X] T032 Add input validation for title (1-200 chars) and description (0-1000 chars)
- [X] T033 Add proper error handling with appropriate HTTP status codes

---

## Phase 7: Security & Error Handling Enhancement

**Goal**: Strengthen security and reliability with proper error handling

### Implementation for Security Enhancement

- [X] T034 [P] Ensure every task operation enforces task.user_id == current_user_id
- [X] T035 [P] Add 403 Forbidden responses when user tries to access others' tasks
- [X] T036 Add 404 Not Found responses when task doesn't exist
- [X] T037 Add database error handling
- [X] T038 Add comprehensive error responses that don't leak sensitive information

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Update README.md with setup instructions and environment variables
- [X] T040 [P] Ensure OpenAPI documentation works at /docs
- [X] T041 Add auto timestamps to Task model
- [X] T042 Add input validation with Pydantic models
- [X] T043 Add proper status codes to all endpoints
- [X] T044 Run quickstart.md validation to ensure all features work as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Additional Operations (Phase 6)**: Depends on foundational and user stories
- **Security Enhancement (Phase 7)**: Depends on all previous phases
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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
Task: "Update main.py to import models and create tables on startup in main.py"
Task: "Implement database session dependency in db.py"
Task: "Add environment variable loading with python-dotenv in main.py"
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
5. Add Additional Operations → Test → Deploy/Demo
6. Add Security Enhancement → Test → Deploy/Demo
7. Polish and finalize → Deploy/Demo
8. Each story adds value without breaking previous stories

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