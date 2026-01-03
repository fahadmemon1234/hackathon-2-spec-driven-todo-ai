# Tasks: JWT Verification Dependency

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

- [X] T001 [P] Install required dependencies: python-jose[cryptography], python-dotenv, pyjwt[cryptography]
- [X] T002 [P] Update requirements.txt with new dependencies
- [X] T003 Create/update dependencies.py file for JWT verification function
- [X] T004 Verify BETTER_AUTH_SECRET environment variable configuration in .env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Implement JWT verification function in dependencies.py with proper imports
- [X] T006 [P] Add proper error handling for invalid/missing tokens in dependencies.py
- [X] T007 [P] Add BETTER_AUTH_SECRET validation from environment variables
- [X] T008 Test JWT function with different payload structures (user.id vs id)
- [X] T009 Create helper functions for token validation in dependencies.py
- [X] T010 Update main.py to include necessary imports for authentication

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure API Access (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to access protected API endpoints by sending JWT tokens in Authorization header

**Independent Test**: Can be fully tested by sending requests with valid and invalid JWT tokens and verifying that only valid tokens grant access to protected resources, delivering the core value of secure API access.

### Implementation for User Story 1

- [X] T011 [P] [US1] Create protected route example in main.py to test JWT verification
- [X] T012 [P] [US1] Implement Authorization header parsing in the JWT verification function
- [X] T013 [US1] Add 401 Unauthorized responses for invalid/missing tokens
- [X] T014 [US1] Test token validation with valid JWT from Better Auth
- [X] T015 [US1] Test rejection of invalid/expired tokens with proper 401 response
- [X] T016 [US1] Test rejection of requests without Authorization header

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Identity Extraction (Priority: P1)

**Goal**: Enable API endpoints to identify which user is making the request to enforce proper data isolation

**Independent Test**: Can be fully tested by sending requests with valid JWT tokens and verifying that the correct user ID is extracted from the token payload, delivering the core value of user-specific data access.

### Implementation for User Story 2

- [X] T017 [P] [US2] Enhance JWT verification to extract user ID from "user.id" payload structure
- [X] T018 [P] [US2] Enhance JWT verification to extract user ID from "id" payload structure
- [X] T019 [US2] Add validation to ensure extracted user ID is a valid string
- [X] T020 [US2] Test user ID extraction with different JWT payload structures
- [X] T021 [US2] Implement proper error handling when user ID is missing from payload
- [X] T022 [US2] Validate that extracted user ID matches UUID format

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Token Validation Robustness (Priority: P2)

**Goal**: Handle various token validation scenarios gracefully to maintain security and provide appropriate feedback

**Independent Test**: Can be fully tested by sending various types of invalid tokens and verifying appropriate rejection with secure error messages, delivering the value of resilient authentication.

### Implementation for User Story 3

- [X] T023 [P] [US3] Add validation for proper Bearer token format in Authorization header
- [X] T024 [P] [US3] Implement error handling for tokens with wrong signature
- [X] T025 [US3] Add validation for supported JWT algorithms (HS256 only)
- [X] T026 [US3] Test rejection of malformed JWT tokens
- [X] T027 [US3] Implement secure error messaging that doesn't expose sensitive information
- [X] T028 [US3] Test behavior when BETTER_AUTH_SECRET environment variable is not set

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Integration with Task Routes

**Goal**: Integrate JWT verification dependency with existing task management endpoints

### Implementation for Integration

- [X] T029 [P] Update routes/tasks.py to use JWT verification dependency
- [X] T030 [P] Modify GET /api/tasks to filter by authenticated user's ID
- [X] T031 Add user_id to task creation in POST /api/tasks endpoint
- [X] T032 Update other task endpoints (GET, PUT, DELETE, PATCH) to verify user ownership
- [X] T033 Test that users can only access their own tasks after authentication
- [X] T034 Implement user isolation enforcement across all task operations

---

## Phase 7: Security Enhancement & Error Handling

**Goal**: Strengthen security and reliability with comprehensive error handling

### Implementation for Security Enhancement

- [X] T035 [P] Add comprehensive error handling for all authentication scenarios
- [X] T036 [P] Implement token expiration validation
- [X] T037 Add proper HTTP status codes (401, 403) for different failure cases
- [X] T038 Enhance security by preventing timing attacks in token validation
- [X] T039 Test edge cases like extremely long tokens or unusual header formats

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T040 [P] Update README.md with JWT authentication requirements and setup
- [X] T041 [P] Add documentation for the new authentication dependency
- [X] T042 Perform security review of JWT implementation
- [X] T043 Test complete authentication flow with frontend JWT tokens
- [X] T044 Run specification compliance check to ensure all requirements are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Integration (Phase 6)**: Depends on foundational and user stories completion
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
Task: "Create protected route example in main.py to test JWT verification in main.py"
Task: "Implement Authorization header parsing in the JWT verification function in dependencies.py"
Task: "Add 401 Unauthorized responses for invalid/missing tokens in dependencies.py"
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
5. Add Integration → Test → Deploy/Demo
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