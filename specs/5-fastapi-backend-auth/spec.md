# Feature Specification: FastAPI Backend with Better Auth Integration

**Feature Branch**: `5-fastapi-backend-auth`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Phase II: FastAPI Backend Specification & Implementation Prompt (Latest Better Auth Compatible) # Frontend: Complete with Better Auth + Manual JWT Bearer Token in API Calls # Date: December 31, 2025 – Better Auth v1.4+ (JWT Plugin or CookieCache JWT Strategy Enabled) You are an expert FastAPI developer with expertise in secure JWT auth, SQLModel, Neon PostgreSQL, and integrating with Better Auth. Project Goal: Implement the /backend folder as a secure, persistent, multi-user Todo API that seamlessly connects with the existing Phase II frontend. - All 5 basic features (Add, View, Update, Delete, Mark Complete) now persistent and user-isolated - Authentication via JWT Bearer token sent by frontend in Authorization header Key Facts from Better Auth (v1.4+): - Frontend configured for stateless mode (JWT strategy via cookieCache or JWT plugin) - After login, frontend manually extracts JWT and sends in Authorization: Bearer <token> - JWT signed with BETTER_AUTH_SECRET using HS256 algorithm - Payload contains user data, including user.id (string UUID) – use this as user_id - Better Auth auto-creates "user" table in DB on first signup API Endpoints (User from JWT – no user_id in path): Base: /api - GET /api/tasks → List authenticated user's tasks (?status=all|pending|completed &sort=created|title) - POST /api/tasks → Create task {title: required, description: optional} - GET /api/tasks/{id} → Get task (ownership check) - PUT /api/tasks/{id} → Update task - DELETE /api/tasks/{id} → Delete task - PATCH /api/tasks/{id}/complete → Toggle completed Security: - Every request must have valid Authorization: Bearer <jwt_token> - Verify token with PyJWT: jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"]) - Extract user_id = payload.get("user", {}).get("id") or payload.get("id") # Better Auth structure - All task operations filter/enforce task.user_id == extracted_user_id - 401 Unauthorized: missing/invalid/expired token - 403 Forbidden: task not owned by user - 404 Not Found: task doesn't exist Tech Stack: - FastAPI (async preferred) - SQLModel (models + ORM) - Neon Serverless PostgreSQL (DATABASE_URL env) - PyJWT for verification (pip install pyjwt[cryptography]) - python-dotenv Structure (/backend): - main.py → app, routers, CORS (allow http://localhost:3000) - db.py → engine, get_session() - models.py → Task model (user_id: str FK to "user.id") - dependencies.py → get_current_user_id() dependency (JWT verify → return str user_id) - routes/tasks.py → APIRouter with all endpoints - .env → DATABASE_URL & BETTER_AUTH_SECRET (EXACT SAME as frontend!) Task Model Details: class Task(SQLModel, table=True): id: Optional[int] = Field(default=None, primary_key=True) user_id: str = Field(foreign_key="user.id", index=True) title: str description: Optional[str] = None completed: bool = False created_at: datetime = Field(default_factory=datetime.utcnow) updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) Features: - Auto timestamps - Filtering & sorting on list - Input validation (Pydantic) - Ownership enforced on every operation - Health endpoint /health - OpenAPI /docs Refer Specs: @specs/features/task-crud.md @specs/features/authentication.md @specs/api/rest-endpoints.md (update paths to /api/tasks) @specs/database/schema.md @backend/CLAUDE.md Task: Implement the complete backend exactly as specified. 1. Setup project, DB connection, models (tables auto-create) 2. JWT verification dependency (HS256 + BETTER_AUTH_SECRET) 3. Full CRUD routes with strict user isolation 4. CORS + polish 5. Update README: env vars (same secret!), run command 6. Suggest spec updates for endpoint simplification Result: Phase 1 in-memory → Phase 2 persistent multi-user full-stack with luxury frontend! Secure, production-ready, and perfectly integrated."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

An authenticated user wants to manage their personal tasks through a secure API. The user sends JWT tokens in the Authorization header and expects to perform all CRUD operations on their own tasks only.

**Why this priority**: This is the core functionality of the todo application - without secure task management, the application has no value.

**Independent Test**: Can be fully tested by sending authenticated requests to all task endpoints and verifying that users can only access their own tasks, delivering the core value of personal task management.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token, **When** they send a POST request to /api/tasks with a title, **Then** a new task is created for that user
2. **Given** a user has created tasks, **When** they send a GET request to /api/tasks, **Then** they receive only their own tasks
3. **Given** a user has a task, **When** they send a PUT request to /api/tasks/{id} with updated data, **Then** only their task is updated
4. **Given** a user has a task, **When** they send a DELETE request to /api/tasks/{id}, **Then** only their task is deleted

---

### User Story 2 - JWT Authentication Verification (Priority: P1)

An API consumer needs to authenticate using JWT tokens generated by Better Auth. The system must verify the token signature using the shared secret and extract the user identity.

**Why this priority**: Without proper authentication, the system cannot ensure data isolation between users, which is a critical security requirement.

**Independent Test**: Can be fully tested by sending requests with valid and invalid JWT tokens and verifying that only valid tokens grant access, delivering the core security value.

**Acceptance Scenarios**:

1. **Given** a request with a valid JWT token, **When** the API verifies the token, **Then** the user identity is extracted and the request proceeds
2. **Given** a request with an invalid JWT token, **When** the API verifies the token, **Then** a 401 Unauthorized response is returned
3. **Given** a request without an Authorization header, **When** the API checks for authentication, **Then** a 401 Unauthorized response is returned

---

### User Story 3 - Task Filtering and Sorting (Priority: P2)

An authenticated user wants to filter and sort their tasks to find specific items quickly. The user can filter by completion status and sort by creation date or title.

**Why this priority**: This enhances user experience by making it easier to find and manage tasks, improving the overall usability of the application.

**Independent Test**: Can be fully tested by making authenticated requests to GET /api/tasks with different query parameters and verifying the results are filtered and sorted correctly.

**Acceptance Scenarios**:

1. **Given** a user has tasks with different completion statuses, **When** they request /api/tasks?status=completed, **Then** only completed tasks are returned
2. **Given** a user has multiple tasks, **When** they request /api/tasks?sort=created, **Then** tasks are returned sorted by creation date
3. **Given** a user has multiple tasks, **When** they request /api/tasks?sort=title, **Then** tasks are returned sorted alphabetically by title

---

### Edge Cases

- What happens when a user tries to access a task that doesn't belong to them?
- How does the system handle expired JWT tokens?
- What occurs when the database connection fails during a request?
- How does the system handle very long task titles or descriptions?
- What happens when a user tries to update a task that no longer exists?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens using the shared BETTER_AUTH_SECRET with HS256 algorithm
- **FR-002**: System MUST extract user_id from JWT payload to enforce ownership
- **FR-003**: System MUST allow authenticated users to create tasks with title and optional description
- **FR-004**: System MUST allow authenticated users to retrieve their own tasks with filtering and sorting
- **FR-005**: System MUST allow authenticated users to update their own tasks
- **FR-006**: System MUST allow authenticated users to delete their own tasks
- **FR-007**: System MUST allow authenticated users to toggle task completion status
- **FR-008**: System MUST return 401 error for invalid/missing JWT tokens
- **FR-009**: System MUST return 404 error when requested task doesn't exist
- **FR-010**: System MUST return 403 error when user tries to access another user's task
- **FR-011**: System MUST connect to PostgreSQL database using DATABASE_URL environment variable
- **FR-012**: System MUST store tasks with auto-generated IDs, user_id foreign key, title, description, completion status, and timestamps
- **FR-013**: System MUST support filtering tasks by status (all|pending|completed)
- **FR-014**: System MUST support sorting tasks by creation date or title
- **FR-015**: System MUST automatically manage created_at and updated_at timestamps
- **FR-016**: System MUST implement CORS policy allowing frontend origin (http://localhost:3000)
- **FR-017**: System MUST provide health check endpoint at /health
- **FR-018**: System MUST provide OpenAPI documentation at /docs

### Key Entities

- **Task**: Represents a user's todo item with ID, user_id (foreign key to Better Auth users), title, description, completion status, and timestamps
- **User**: Represents an authenticated user managed by Better Auth with UUID identifier
- **JWT Token**: Represents an authentication token containing user identity information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, read, update, and delete tasks with 99% success rate
- **SC-002**: API correctly authenticates requests with JWT tokens in 99.9% of cases
- **SC-003**: Users can only access their own tasks with 100% enforcement rate
- **SC-004**: API handles 1000 concurrent authenticated users without degradation
- **SC-005**: Task filtering and sorting operations complete in under 100ms for datasets up to 10,000 tasks
- **SC-006**: All API endpoints return appropriate error codes (401, 403, 404) with 100% accuracy
- **SC-007**: Database operations complete successfully 99.5% of the time under normal load
- **SC-008**: API maintains 99.9% uptime during normal operation
- **SC-009**: API correctly implements CORS policy allowing frontend access
- **SC-010**: Health check endpoint responds within 100ms