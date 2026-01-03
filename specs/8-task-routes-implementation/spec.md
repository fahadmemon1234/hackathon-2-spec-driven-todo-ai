# Feature Specification: Task Routes Implementation

**Feature Branch**: `8-task-routes-implementation`
**Created**: 2025-01-07
**Status**: Draft
**Input**: User description: "# Task 4: Create & List Tasks Routes Specification + Implementation # Phase II Backend – Implement POST /api/tasks and GET /api/tasks # Current Status: Task 1, 2, 3 complete (DB connected, Task model ready, JWT verification working) You are an expert FastAPI developer with strong SQLModel skills. Goal for Task 4: Implement the two core endpoints that handle task creation and listing: - POST /api/tasks → Create a new task for the authenticated user - GET /api/tasks → List all tasks belonging only to the authenticated user with filtering and sorting Requirements: 1. Router Setup (in routes/tasks.py) - Create APIRouter with prefix="/api" - Import necessary dependencies: from fastapi import APIRouter, Depends, Query, HTTPException from sqlmodel import select, Session from typing import Optional, List from ..models import Task from ..db import get_session from ..dependencies import get_current_user_id router = APIRouter(prefix="/api") 2. POST /api/tasks – Create Task - Define Pydantic model for request body: class TaskCreate(SQLModel): title: str = Field(min_length=1, max_length=200) description: Optional[str] = Field(default=None, max_length=1000) - Endpoint: @router.post("/tasks", response_model=Task) def create_task( task_data: TaskCreate, user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session) ): new_task = Task( user_id=user_id, title=task_data.title, description=task_data.description ) session.add(new_task) session.commit() session.refresh(new_task) return new_task 3. GET /api/tasks – List Tasks with Filters - Endpoint: @router.get("/tasks", response_model=List[Task]) def list_tasks( user_id: str = Depends(get_current_user_id), status: Optional[str] = Query(None, description="all, pending, or completed"), sort: Optional[str] = Query("created", description="created or title"), session: Session = Depends(get_session) ): # Base query filtered by authenticated user only statement = select(Task).where(Task.user_id == user_id) # Status filter if status == "pending": statement = statement.where(Task.completed == False) elif status == "completed": statement = statement.where(Task.completed == True) # "all" or None → no filter # Sorting if sort == "title": statement = statement.order_by(Task.title) else: # default "created" → newest first statement = statement.order_by(Task.created_at.desc()) tasks = session.exec(statement).all() return tasks 4. Include Router in main.py - In main.py: from routes.tasks import router as tasks_router app.include_router(tasks_router) 5. Expected Behavior - POST: Creates task with correct user_id, returns full task with id, timestamps - GET: Returns only authenticated user's tasks - Supports query params: /api/tasks?status=pending&sort=title - Invalid token → 401 (from dependency) - Works seamlessly with frontend API client Refer to: @specs/features/task-crud.md @specs/api/rest-endpoints.md @backend/CLAUDE.md Now implement Task 4 exactly as specified. Create/update routes/tasks.py with the router, models, and both endpoints. Ensure clean code, proper validation, and response models. After this task, users will be able to create and view their own tasks persistently."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Tasks (Priority: P1)

An authenticated user wants to create new tasks in their personal todo list. The user submits task details through the frontend which sends a POST request to the backend API with proper authentication.

**Why this priority**: This is the fundamental functionality that allows users to add items to their todo list, which is the core value of a todo application.

**Independent Test**: Can be fully tested by sending authenticated POST requests to /api/tasks with valid task data and verifying that tasks are created with the correct user association, delivering the core value of task creation.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they send a POST request to /api/tasks with a title (and optional description), **Then** a new task is created with the user's ID and returned with all details
2. **Given** a user provides invalid task data (empty title), **When** they send a POST request to /api/tasks, **Then** a validation error is returned with appropriate status code
3. **Given** a user sends a request without a valid JWT token, **When** they try to create a task, **Then** a 401 Unauthorized response is returned
4. **Given** a user creates a task, **When** they check their task list, **Then** the newly created task appears in their list

---

### User Story 2 - View Personal Task Lists (Priority: P1)

An authenticated user wants to view all their tasks with options to filter and sort. The user sends a GET request to retrieve their tasks with optional filtering by status and sorting options.

**Why this priority**: This is the core functionality that allows users to see their tasks, which is essential for managing their todo list effectively.

**Independent Test**: Can be fully tested by sending authenticated GET requests to /api/tasks with various query parameters and verifying that only the user's tasks are returned with proper filtering and sorting, delivering the core value of task visibility.

**Acceptance Scenarios**:

1. **Given** a user has multiple tasks, **When** they send a GET request to /api/tasks, **Then** they receive only their own tasks
2. **Given** a user wants to see only pending tasks, **When** they send a GET request to /api/tasks?status=pending, **Then** only their incomplete tasks are returned
3. **Given** a user wants to see tasks sorted by title, **When** they send a GET request to /api/tasks?sort=title, **Then** their tasks are returned in alphabetical order by title
4. **Given** a user sends a request without a valid JWT token, **When** they try to access their tasks, **Then** a 401 Unauthorized response is returned

---

### User Story 3 - Filter and Sort Tasks (Priority: P2)

An authenticated user wants to efficiently find specific tasks by applying filters and sorting options. The system should provide flexible ways to view tasks based on status and ordering preferences.

**Why this priority**: This enhances user experience by making it easier to find and manage tasks, improving the overall usability of the application.

**Independent Test**: Can be fully tested by sending various combinations of query parameters to the GET /api/tasks endpoint and verifying correct filtering and sorting behavior, delivering the value of efficient task management.

**Acceptance Scenarios**:

1. **Given** a user has tasks with different completion statuses, **When** they request /api/tasks?status=completed, **Then** only completed tasks are returned
2. **Given** a user has multiple tasks, **When** they request /api/tasks?sort=created, **Then** tasks are returned in reverse chronological order (newest first)
3. **Given** a user has multiple tasks, **When** they request /api/tasks?status=pending&sort=title, **Then** only pending tasks are returned sorted alphabetically by title
4. **Given** a user sends invalid query parameters, **When** they request /api/tasks with incorrect status/sort values, **Then** appropriate error responses are returned

---

### Edge Cases

- What happens when a user tries to access another user's tasks through direct manipulation?
- How does the system handle very long task titles or descriptions near the character limits?
- What occurs when the database is temporarily unavailable during a request?
- How does the system handle concurrent task creation requests from the same user?
- What happens when a user has thousands of tasks and requests the entire list?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept POST requests to /api/tasks to create new tasks for authenticated users
- **FR-002**: System MUST validate that task title is between 1-200 characters
- **FR-003**: System MUST validate that task description is optional but limited to 1000 characters if provided
- **FR-004**: System MUST associate each created task with the authenticated user's ID
- **FR-005**: System MUST return the complete task object (with ID, timestamps) after successful creation
- **FR-006**: System MUST accept GET requests to /api/tasks to retrieve user's tasks
- **FR-007**: System MUST filter returned tasks to only include those belonging to the authenticated user
- **FR-008**: System MUST support optional status filtering (all, pending, completed) via query parameter
- **FR-009**: System MUST support optional sorting (by creation date or title) via query parameter
- **FR-010**: System MUST require valid JWT authentication for both endpoints (return 401 for invalid/missing tokens)
- **FR-011**: System MUST return appropriate HTTP status codes (200 for success, 401 for unauthorized, 422 for validation errors)
- **FR-012**: System MUST properly handle database session management for each request
- **FR-013**: System MUST return tasks in JSON format with consistent field structure
- **FR-014**: System MUST implement proper error handling with informative but secure error messages
- **FR-015**: System MUST ensure data integrity by properly associating tasks with user IDs from JWT tokens

### Key Entities

- **Task Creation Request**: Represents the data needed to create a new task (title, optional description) with validation constraints
- **Task List Response**: Represents a collection of tasks with optional filtering and sorting applied
- **Authentication Token**: Represents the JWT token that identifies the authenticated user and provides their user ID

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create new tasks with 99.9% success rate when providing valid data
- **SC-002**: Task creation endpoint responds within 200ms for 95% of requests under normal load
- **SC-003**: Users can retrieve their task lists with 99.9% success rate
- **SC-004**: Task listing endpoint responds within 300ms for 95% of requests with up to 1000 tasks
- **SC-005**: Filtering and sorting operations work correctly 100% of the time
- **SC-006**: Authentication is enforced properly with 100% accuracy (no unauthorized access)
- **SC-007**: System handles 1000 concurrent authenticated users creating tasks without degradation
- **SC-008**: Task data integrity is maintained with 100% accuracy (users only see their own tasks)
- **SC-009**: API endpoints return appropriate error codes with 100% accuracy for different failure scenarios
- **SC-010**: The implementation follows security best practices with zero vulnerabilities related to user data access